"""Video download via yt-dlp for YouTube and TikTok."""

from __future__ import annotations

import glob as globmod
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yt_dlp


@dataclass
class DownloadResult:
    video_path: Path
    title: str
    duration: int | None
    description: str
    platform: str
    original_url: str


def _detect_platform(url: str) -> str:
    url_lower = url.lower()
    if "tiktok.com" in url_lower:
        return "tiktok"
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    return "unknown"


def _find_downloaded_file(output_dir: Path, video_id: str) -> Path | None:
    """Find the downloaded MP4 file by video ID, handling merge outputs."""
    # Check direct mp4 first
    direct = output_dir / f"{video_id}.mp4"
    if direct.exists():
        return direct

    # Check for any file matching the video ID
    for pattern in [f"{video_id}.*mp4", f"{video_id}.*"]:
        matches = globmod.glob(str(output_dir / pattern))
        if matches:
            return Path(matches[0])

    return None


# Format preference: 360p MP4 keeps file size small for fast Gemini upload/processing.
# Gemini samples frames at ~1fps anyway — 360p is sufficient for scene analysis.
# A post-download ffmpeg pass further reduces size via CRF 35 + 15fps cap.
_FORMAT_STRING = (
    "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/"
    "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/"
    "best[height<=360][ext=mp4]/"
    "best[height<=480][ext=mp4]/"
    "best[ext=mp4]/"
    "best"
)


def _transcode_for_upload(src: Path, verbose: bool = False) -> Path:
    """Re-encode video to minimize upload size: 360p cap, 15fps, CRF 35, 64kbps audio.

    Gemini's video understanding samples ~1fps, so high frame rate and bitrate are wasted.
    Saves significant time on upload + Gemini processing for longer videos.
    Returns path to transcoded file (replaces original on success).
    """
    dst = src.with_stem(src.stem + "_upload")
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-vf", "scale='min(640,iw)':-2:flags=lanczos,fps=15",
        "-c:v", "libx264", "-crf", "35", "-preset", "fast",
        "-c:a", "aac", "-b:a", "64k",
        "-movflags", "+faststart",
        str(dst),
    ]
    if verbose:
        print(f"  Transcoding for upload: {src.name} → {dst.name}", file=sys.stderr)
        subprocess.run(cmd, check=True)
    else:
        subprocess.run(cmd, check=True, capture_output=True)

    before_mb = src.stat().st_size / (1024 * 1024)
    after_mb = dst.stat().st_size / (1024 * 1024)
    print(
        f"  Transcoded: {before_mb:.1f} MB → {after_mb:.1f} MB "
        f"({100 - after_mb / before_mb * 100:.0f}% smaller)",
        file=sys.stderr,
    )
    src.unlink()
    dst.rename(src)
    return src


def download_video(
    url: str,
    output_dir: Path,
    max_size_mb: int = 500,
    verbose: bool = False,
    transcode: bool = True,
) -> DownloadResult:
    """Download video from URL as MP4, return path and metadata."""
    output_dir.mkdir(parents=True, exist_ok=True)
    platform = _detect_platform(url)

    progress_hook_state = {"started": False}

    def _progress_hook(d: dict) -> None:
        if d["status"] == "downloading" and not progress_hook_state["started"]:
            progress_hook_state["started"] = True
            if not verbose:
                print("  Downloading...", file=sys.stderr)
        elif d["status"] == "finished":
            if not verbose:
                print("  Download complete, processing...", file=sys.stderr)

    ydl_opts: dict = {
        "format": _FORMAT_STRING,
        "merge_output_format": "mp4",
        "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
        "quiet": not verbose,
        "no_warnings": not verbose,
        "progress_hooks": [_progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise RuntimeError(f"Failed to extract info from: {url}")

            video_id = info.get("id", "unknown")
            video_path = _find_downloaded_file(output_dir, video_id)

            if video_path is None:
                # Fallback: try prepare_filename
                filename = ydl.prepare_filename(info)
                video_path = Path(filename).with_suffix(".mp4")
                if not video_path.exists():
                    video_path = Path(filename)
                    if not video_path.exists():
                        raise RuntimeError(
                            f"Downloaded file not found for video ID: {video_id}"
                        )

            if transcode:
                video_path = _transcode_for_upload(video_path, verbose=verbose)

            size_mb = video_path.stat().st_size / (1024 * 1024)
            if verbose:
                print(f"  File size: {size_mb:.1f} MB", file=sys.stderr)

            return DownloadResult(
                video_path=video_path,
                title=info.get("title", "Untitled"),
                duration=info.get("duration"),
                description=info.get("description", ""),
                platform=platform,
                original_url=url,
            )

    except yt_dlp.utils.DownloadError as e:
        raise RuntimeError(f"Download failed: {e}") from e
