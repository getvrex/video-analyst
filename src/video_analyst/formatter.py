"""Output formatting for JSON and Markdown."""

from __future__ import annotations

from .models import VideoReproductionPlan


def format_json(plan: VideoReproductionPlan) -> str:
    """Format plan as indented JSON."""
    return plan.model_dump_json(indent=2)


def format_markdown(plan: VideoReproductionPlan, style: str = "realistic") -> str:
    """Format plan as human-readable Markdown."""
    lines: list[str] = []

    # Header
    lines.append(f"# {plan.title}")
    lines.append("")
    lines.append(f"> {plan.description}")
    lines.append("")
    lines.append(
        f"**Duration**: {plan.total_duration_seconds}s | "
        f"**Language**: {plan.target_language} | "
        f"**Scenes**: {len(plan.scenes)} | "
        f"**Style**: {style}"
    )
    lines.append("")

    # Viral structure
    lines.append("## Viral Structure Analysis")
    lines.append("")
    lines.append(plan.viral_structure_notes)
    lines.append("")

    # Characters
    if plan.characters:
        lines.append("## Characters")
        lines.append("")
        for char in plan.characters:
            lines.append(f"### {char.character_name}")
            lines.append(f"{char.character_description}")
            lines.append("")
            lines.append("**Reference Sheet Prompt**:")
            lines.append(f"```\n{char.t2i_reference_prompt}\n```")
            lines.append("")

    # Scenes
    lines.append("## Scenes")
    lines.append("")
    for scene in plan.scenes:
        method_label = (
            "T2I → I2V" if scene.generation_method == "t2i_i2v" else "T2V"
        )
        lines.append(
            f"### Scene {scene.scene_number} — {scene.duration_seconds}s [{method_label}]"
        )
        lines.append(f"*{scene.scene_description}*")
        lines.append("")

        # T2I prompt (if applicable)
        if scene.t2i_prompt:
            lines.append("**Image Prompt (Nano Banana 2)**:")
            lines.append(f"```\n{scene.t2i_prompt}\n```")
            lines.append("")

        # Video prompt
        lines.append("**Video Prompt (Veo 3 — 0-8s)**:")
        lines.append(f"```\n{scene.video_prompt}\n```")
        lines.append("")

        # Extend prompt
        if scene.video_extend_prompt:
            lines.append("**Video Extend Prompt (8s+)**:")
            lines.append(f"```\n{scene.video_extend_prompt}\n```")
            lines.append("")

        # Voiceover
        lines.append(
            f"**Voiceover** ({scene.voiceover_duration_estimate_seconds}s):"
        )
        lines.append(f"> {scene.voiceover_text}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Cover
    lines.append("## Cover Image")
    lines.append("")
    lines.append("**T2I Prompt (Nano Banana 2)**:")
    lines.append(f"```\n{plan.cover_t2i_prompt}\n```")
    lines.append("")

    # Tags
    lines.append("## Tags")
    lines.append("")
    lines.append(" ".join(plan.metadata_tags))
    lines.append("")

    return "\n".join(lines)


def format_output(plan: VideoReproductionPlan, fmt: str, style: str = "realistic") -> str:
    """Format the plan in the requested format."""
    if fmt == "markdown":
        return format_markdown(plan, style=style)
    return format_json(plan)
