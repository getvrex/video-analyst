"""CLI entry point for video-analyst."""

from __future__ import annotations

import sys
from importlib.metadata import version
from pathlib import Path

import click

from .config import Config
from .downloader import download_video
from .analyzer import analyze_video
from .formatter import format_output
from .styles import STYLE_NAMES, list_styles


class StyleChoice(click.ParamType):
    """Click type that validates style names and supports 'list' to show options."""

    name = "style"

    def convert(self, value, param, ctx):
        if value == "list":
            click.echo("Available styles:\n" + list_styles(), err=True)
            ctx.exit(0)
        if value not in STYLE_NAMES:
            self.fail(
                f"Unknown style '{value}'. Use --style list to see options.",
                param,
                ctx,
            )
        return value


@click.group()
@click.version_option(version=version("video-analyst"), prog_name="video-analyst")
def main() -> None:
    """Video Analyst - Analyze videos and produce AI reproduction plans."""
    pass


@main.command()
@click.argument("url")
@click.option(
    "--mode", "-m",
    type=click.Choice(["summary", "highlights", "full"]),
    default="full",
    help="Analysis mode: summary (condensed), highlights (50-70% duration), or full (comprehensive).",
)
@click.option(
    "--lang", "-l",
    default="en",
    help="Target language for voiceover (e.g. en, vi, ja).",
)
@click.option(
    "--style", "-s",
    type=StyleChoice(),
    default="realistic",
    help="Visual style for prompts. Use --style list to see options.",
)
@click.option(
    "--format", "-f", "fmt",
    type=click.Choice(["json", "markdown"]),
    default="json",
    help="Output format.",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Output file path (default: stdout).",
)
@click.option("--keep-video", is_flag=True, help="Keep downloaded video after analysis.")
@click.option("--model", default=None, help="Override Gemini model name.")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
def analyze(
    url: str,
    mode: str,
    lang: str,
    style: str,
    fmt: str,
    output: str | None,
    keep_video: bool,
    model: str | None,
    verbose: bool,
) -> None:
    """Analyze a video URL and produce a reproduction plan."""

    # Load config
    config = Config.from_env()
    if model:
        config.model_name = model

    video_path: Path | None = None

    try:
        # Step 1: Download
        print(f"[1/4] Downloading video... ({url})", file=sys.stderr)
        result = download_video(
            url=url,
            output_dir=config.download_dir,
            verbose=verbose,
        )
        video_path = result.video_path

        if verbose:
            print(
                f"  Downloaded: {result.title} ({result.duration}s) -> {video_path}",
                file=sys.stderr,
            )

        # Step 2-4: Analyze
        analysis = analyze_video(
            video_path=video_path,
            mode=mode,
            target_language=lang,
            video_metadata={
                "title": result.title,
                "duration": result.duration,
                "description": result.description,
                "platform": result.platform,
            },
            config=config,
            style=style,
            verbose=verbose,
        )

        plan = analysis.plan
        tokens = analysis.token_usage

        # Format output
        formatted = format_output(plan, fmt, style=style)

        # Token cost summary
        cost = tokens.cost_usd(config.model_name)
        token_summary = (
            f"Tokens — prompt: {tokens.prompt_tokens:,}, "
            f"completion: {tokens.completion_tokens:,}, "
            f"total: {tokens.total_tokens:,} | "
            f"Cost: ${cost:.4f} USD"
        )
        if tokens.attempts > 1:
            token_summary += f" ({tokens.attempts} attempts)"

        # Write output
        if output:
            Path(output).write_text(formatted, encoding="utf-8")
            print(
                f"\nDone! Plan saved to {output} "
                f"({len(plan.scenes)} scenes, {plan.total_duration_seconds}s total)",
                file=sys.stderr,
            )
        else:
            click.echo(formatted)
            print(
                f"\nDone! {len(plan.scenes)} scenes, "
                f"{plan.total_duration_seconds}s total",
                file=sys.stderr,
            )

        print(token_summary, file=sys.stderr)

    except RuntimeError as e:
        print(f"\nError: {e}", file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        raise SystemExit(130)
    finally:
        # Cleanup downloaded video
        if video_path and video_path.exists() and not keep_video:
            video_path.unlink(missing_ok=True)
            if verbose:
                print(f"  Cleaned up: {video_path}", file=sys.stderr)


@main.command(name="styles")
def list_styles_cmd() -> None:
    """List all available visual styles."""
    click.echo("Available styles:\n" + list_styles())
