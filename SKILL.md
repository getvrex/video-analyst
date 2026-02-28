# video-analyst

Analyze videos from YouTube or TikTok and produce structured AI reproduction plans with Veo 3 video prompts, Nano Banana 2 image prompts, and natural voiceover text.

## Trigger

When the user asks to analyze a video, reproduce a video, or uses `/video-analyst`.

## Instructions

1. Parse the user's request to extract:
   - **URL** (required): YouTube or TikTok video URL
   - **Mode**: "summary" for quick analysis or "full" for comprehensive (default: full)
   - **Language**: Target language for voiceover and title (default: en). Examples: vi (Vietnamese), ja (Japanese), ko (Korean), zh (Chinese), es (Spanish)
   - **Style**: Visual style preset (default: realistic). Options: realistic, cinematic, ghibli, wes-anderson, noir, cyberpunk, vintage-film, anime, watercolor, documentary
   - **Format**: "json" or "markdown" (default: markdown for display)

2. Find the installation directory. Check these locations in order:
   ```bash
   SKILL_DIR=$([ -d "$HOME/.claude/skills/video-analyst" ] && echo "$HOME/.claude/skills/video-analyst" || echo "$(dirname "$(realpath "$0")")")
   ```

3. Ensure the tool is installed. If the venv doesn't exist:
   ```bash
   cd "$SKILL_DIR" && uv venv && uv pip install -e .
   ```

4. Ensure `GEMINI_API_KEY` is set in the environment.

5. Run the analysis:
   ```bash
   cd "$SKILL_DIR" && source .venv/bin/activate && video-analyst analyze "<URL>" --mode <mode> --lang <lang> --style <style> --format markdown
   ```

6. Present the output to the user. If the output is JSON, format it as readable markdown.

## Examples

- `/video-analyst https://www.tiktok.com/@user/video/123` — full analysis in English
- `/video-analyst https://youtube.com/shorts/abc --summary --lang vi` — summary in Vietnamese
- `/video-analyst https://youtu.be/xyz --style cyberpunk` — cyberpunk style
- `Analyze this video: https://youtu.be/xyz` — triggers automatically

## Requirements

- Python 3.11+
- `GEMINI_API_KEY` environment variable
- `ffmpeg` available in PATH
