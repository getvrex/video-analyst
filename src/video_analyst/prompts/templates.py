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
6. CRITICAL: video_prompt, video_extend_prompt, and t2i_prompt must contain ZERO text content — no voiceover, no dialogue, no "Character says:", no on-screen text descriptions, no titles, no captions, no speech bubbles. These fields describe ONLY visuals, camera, and ambient sound. All spoken words go in voiceover_text. All on-screen text goes in title_card_text.

Output the structured JSON response."""


def get_thinking_user_prompt(
    mode: str,
    target_language: str,
    video_metadata: dict,
    style: str = "realistic",
    channel_profile: dict | None = None,
) -> str:
    """Build the user prompt for thinking mode — enhance, don't reproduce."""

    style_def = get_style(style)
    channel_name = (channel_profile or {}).get("name", "Generic")

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

    return f"""Use the attached video as SOURCE MATERIAL. Your goal is NOT to reproduce it but to create a BETTER, more engaging version for the channel "{channel_name}".
{metadata_section}
## Task

Watch the entire source video carefully. Then:

1. **Extract** the most interesting ideas, facts, and angles from the source
2. **Enhance** — add context, depth, facts, and insights the source missed or glossed over
3. **Restructure** — organize the content for maximum engagement with YOUR audience
4. **Create** — produce a VideoReproductionPlan that represents YOUR enhanced version, not a copy

Think of the source video as research notes. You're the expert creator who turns research into compelling content.

Analysis mode: {mode}
Target language for voiceover and title: {target_language}
Visual style: {style} — {style_def['description']}

IMPORTANT RULES:
1. DO NOT reproduce the source video shot-for-shot. Use it as inspiration and source material only.
2. Add value: include facts, context, and analysis that go beyond the source.
3. Write voiceover in the channel's voice and personality, not in the source's style.
4. If a scene contains ANY character (human, animal, creature), it MUST use generation_method "t2i_i2v" with a t2i_prompt. Only pure environmental/atmospheric scenes without characters use "t2v".
5. Apply the {style} visual style consistently to every prompt.
6. Voiceover in {target_language}, sounding natural and human — in YOUR channel's voice.
7. Character descriptions must be identical word-for-word across all scenes.
8. CRITICAL: video_prompt, video_extend_prompt, and t2i_prompt must contain ZERO text content — no voiceover, no dialogue, no "Character says:", no on-screen text descriptions, no titles, no captions, no speech bubbles. These fields describe ONLY visuals, camera, and ambient sound. All spoken words go in voiceover_text. All on-screen text goes in title_card_text.
9. The content_strategy_notes field should describe YOUR engagement strategy for this content, not just analyze the source's structure.

Output the structured JSON response."""
