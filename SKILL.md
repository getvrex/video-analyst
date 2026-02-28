# video-analyst

Analyze videos from YouTube or TikTok and produce structured AI reproduction plans with Veo 3 video prompts, Nano Banana 2 image prompts, and natural voiceover text.

## Trigger

When the user asks to analyze a video, reproduce a video, or uses `/video-analyst`.

## Instructions

1. Parse the user's request to extract:
   - **URL** (required): YouTube or TikTok video URL
   - **Mode**: "summary" for quick analysis or "full" for comprehensive (default: full)
   - **Language**: Target language for voiceover and title (default: en). Examples: vi (Vietnamese), ja (Japanese), ko (Korean), zh (Chinese), es (Spanish)
   - **Format**: "json" or "markdown" (default: markdown for display)

2. Ensure the tool is installed. If not:
   ```bash
   cd /Users/quocs/Projects/video-analyst && uv venv && uv pip install -e .
   ```

3. Ensure `GEMINI_API_KEY` is set in the environment.

4. Run the analysis:
   ```bash
   cd /Users/quocs/Projects/video-analyst && source .venv/bin/activate && video-analyst analyze "<URL>" --mode <mode> --lang <lang> --format markdown
   ```

5. Present the output to the user. If the output is JSON, format it as readable markdown.

## Examples

- `/video-analyst https://www.tiktok.com/@user/video/123` — full analysis in English
- `/video-analyst https://youtube.com/shorts/abc --summary --lang vi` — summary in Vietnamese
- `Analyze this video: https://youtu.be/xyz` — triggers automatically

## Requirements

- Python 3.11+
- `GEMINI_API_KEY` environment variable
- `yt-dlp` and `ffmpeg` available in PATH
