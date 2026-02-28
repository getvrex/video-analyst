"""User prompt templates for Gemini video analysis."""

from __future__ import annotations

from ..styles import get_style


def get_user_prompt(
    mode: str, target_language: str, video_metadata: dict, style: str = "realistic"
) -> str:
    """Build the user prompt with video context."""

    style_def = get_style(style)

    metadata_section = ""
    if video_metadata:
        desc = video_metadata.get("description", "")
        if desc and len(desc) > 500:
            desc = desc[:500] + "..."

        metadata_section = f"""
## Source Video Metadata
- Title: {video_metadata.get("title", "Unknown")}
- Duration: {video_metadata.get("duration", "Unknown")} seconds
- Platform: {video_metadata.get("platform", "Unknown")}
- Description: {desc or "N/A"}
"""

    return f"""Analyze the attached video and produce a complete reproduction plan.
{metadata_section}
## Task

Watch the entire video carefully. Then produce a VideoReproductionPlan that allows someone to recreate this video using AI generation tools (Veo 3 for video, Nano Banana 2 for images).

Analysis mode: {mode}
Target language for voiceover and title: {target_language}
Visual style: {style} — {style_def['description']}

IMPORTANT RULES:
1. SKIP all advertising, sponsorship segments, end cards, subscribe/follow callouts, and promotional content. Only reproduce the substantive content.
2. If a scene contains ANY character (human, animal, creature), it MUST use generation_method "t2i_i2v" with a t2i_prompt. Only pure environmental/atmospheric scenes without characters use "t2v".
3. Apply the {style} visual style consistently to every prompt.
4. Voiceover in {target_language}, sounding natural and human.
5. Character descriptions must be identical word-for-word across all scenes.

Output the structured JSON response."""
