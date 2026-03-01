"""Pydantic models for the video reproduction plan output schema."""

from __future__ import annotations

import copy
from typing import Literal

from pydantic import BaseModel, Field


class Scene(BaseModel):
    scene_number: int = Field(description="Sequential scene number starting from 1")
    duration_seconds: int = Field(
        description="Target duration in seconds. Must be 8, 16, or 24. 16 is ideal."
    )
    generation_method: Literal["t2i_i2v", "t2v"] = Field(
        description=(
            "Use 't2i_i2v' when the scene needs a character/object reference image "
            "generated first (Nano Banana 2) then animated (Veo 3). "
            "Use 't2v' for scenes generated directly as video."
        )
    )
    video_prompt: str = Field(
        description=(
            "Veo 3 prompt for the first 8 seconds. Structure: scene description + "
            "visual style + camera movement + subject action + background + lighting + audio. "
            "NEVER include voiceover text here — voiceover goes only in voiceover_text. "
            "For dialogue: 'Character says: \"words\"' with '(no subtitles)'. "
            "Always specify ambient sound to prevent hallucinated audio."
        )
    )
    video_extend_prompt: str = Field(
        description=(
            "Veo 3 scene extension prompt for continuing beyond 8s. Describes how the "
            "scene evolves visually from the first 8 seconds. "
            "NEVER include voiceover text here. Empty string if duration is 8 seconds."
        )
    )
    t2i_prompt: str = Field(
        description=(
            "Nano Banana 2 prompt for generating the reference/first-frame image. "
            "Use natural language, include camera metadata (lens, aperture), "
            "spatial relationships. Empty string if generation_method is 't2v'."
        )
    )
    voiceover_text: str = Field(
        description=(
            "Voiceover narration in the target language. Must sound natural and human. "
            "Calibrated to fit the scene duration (~2.5 words/second for English)."
        )
    )
    voiceover_duration_estimate_seconds: float = Field(
        description="Estimated voiceover duration based on word count and language"
    )
    title_card_text: str = Field(
        description=(
            "Text for a title card overlay if the original scene features prominent "
            "on-screen text (big titles, chapter headings, key statements). "
            "Empty string if no significant text is shown. "
            "Skip small/incidental text like watermarks, lower-thirds, or captions."
        )
    )
    scene_description: str = Field(
        description="Brief human-readable description of what happens in this scene"
    )


class CharacterProfile(BaseModel):
    character_name: str = Field(
        description="Consistent identifier for this character across all scenes"
    )
    character_description: str = Field(
        description="Detailed visual description. Must be identical in every scene prompt."
    )
    t2i_reference_prompt: str = Field(
        description=(
            "Nano Banana 2 prompt for a character reference sheet on a PLAIN WHITE background. "
            "Must include: specific ethnicity, age, build, skin tone, hair details, eye color, "
            "full clothing description. Request 3 views (front, 3/4, side). "
            "NO expressions, emotions, poses, actions, or scene context — neutral standing only."
        )
    )


class VideoReproductionPlan(BaseModel):
    title: str = Field(description="Engaging title for the video")
    description: str = Field(description="Brief description of the video concept and hook")
    metadata_tags: list[str] = Field(
        description="Hashtags and metadata tags for discoverability"
    )
    target_language: str = Field(description="Language code for voiceover (e.g. 'en', 'vi')")
    total_duration_seconds: int = Field(
        description="Total estimated duration of the reproduced video"
    )
    viral_structure_notes: str = Field(
        description=(
            "Analysis of the viral structure: hook mechanism (first 3 seconds), "
            "content arc, resolution, and what makes this video engaging."
        )
    )
    characters: list[CharacterProfile] = Field(
        description="Character profiles for consistency. Empty list if no characters needed."
    )
    scenes: list[Scene] = Field(description="Ordered list of scenes composing the video")
    cover_t2i_prompt: str = Field(
        description=(
            "Nano Banana 2 prompt for the video cover/thumbnail. "
            "Capture the most engaging moment or hook."
        )
    )


def resolve_schema_refs(schema: dict) -> dict:
    """Inline $defs/$ref references for Gemini API compatibility.

    Gemini's response_json_schema doesn't handle $ref well,
    so we recursively replace all $ref pointers with the actual definitions.
    """
    schema = copy.deepcopy(schema)
    defs = schema.pop("$defs", {})
    if not defs:
        return schema

    def _resolve(obj: dict | list | str) -> dict | list | str:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref_path = obj["$ref"]  # e.g. "#/$defs/Scene"
                ref_name = ref_path.split("/")[-1]
                resolved = copy.deepcopy(defs[ref_name])
                # Recursively resolve nested refs
                return _resolve(resolved)
            return {k: _resolve(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_resolve(item) for item in obj]
        return obj

    return _resolve(schema)
