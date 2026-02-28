"""Configuration loading from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    gemini_api_key: str
    model_name: str = "gemini-2.5-flash"
    download_dir: Path = Path("downloads")
    max_video_size_mb: int = 200

    @classmethod
    def from_env(cls) -> "Config":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise SystemExit(
                "Error: GEMINI_API_KEY environment variable is required.\n"
                "Set it with: export GEMINI_API_KEY=your_key_here"
            )

        return cls(
            gemini_api_key=api_key,
            model_name=os.environ.get("VIDEO_ANALYST_MODEL", "gemini-2.5-flash"),
            download_dir=Path(os.environ.get("VIDEO_ANALYST_DOWNLOAD_DIR", "downloads")),
            max_video_size_mb=int(os.environ.get("VIDEO_ANALYST_MAX_VIDEO_SIZE_MB", "200")),
        )
