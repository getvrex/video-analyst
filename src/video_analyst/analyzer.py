"""Gemini video analysis orchestration."""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from google import genai
from google.genai import types

from .config import Config
from .humanizer import humanize_voiceovers
from .models import VideoReproductionPlan, resolve_schema_refs
from .prompts.system import get_system_prompt
from .prompts.templates import get_user_prompt


# Gemini 2.5 Flash pricing (per 1M tokens)
PRICING = {
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}
DEFAULT_PRICING = {"input": 0.30, "output": 2.50}  # Flash fallback


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    attempts: int = 0

    def add(self, response) -> None:
        """Accumulate token usage from a Gemini response."""
        self.attempts += 1
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            meta = response.usage_metadata
            self.prompt_tokens += getattr(meta, "prompt_token_count", 0) or 0
            self.completion_tokens += getattr(meta, "candidates_token_count", 0) or 0
            self.total_tokens += getattr(meta, "total_token_count", 0) or 0

    def cost_usd(self, model: str = "gemini-2.5-flash") -> float:
        """Calculate cost in USD based on model pricing."""
        rates = PRICING.get(model, DEFAULT_PRICING)
        input_cost = (self.prompt_tokens / 1_000_000) * rates["input"]
        output_cost = (self.completion_tokens / 1_000_000) * rates["output"]
        return input_cost + output_cost


@dataclass
class AnalysisResult:
    plan: VideoReproductionPlan
    token_usage: TokenUsage


def _wait_for_file_active(
    client: genai.Client, uploaded_file, verbose: bool = False, timeout: int = 300
) -> None:
    """Poll until uploaded file is in ACTIVE state, with timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        f = client.files.get(name=uploaded_file.name)
        if f.state == "ACTIVE":
            break
        if f.state == "FAILED":
            raise RuntimeError(f"File processing failed: {uploaded_file.name}")
        if verbose:
            print(f"  File state: {f.state}, waiting...", file=sys.stderr)
        time.sleep(2)
    else:
        raise RuntimeError(
            f"File processing timed out after {timeout}s: {uploaded_file.name}"
        )


def _generate_with_retry(
    client: genai.Client,
    model: str,
    contents: list,
    system_prompt: str,
    schema: dict,
    uploaded_file,
    user_prompt: str,
    token_usage: TokenUsage,
    verbose: bool = False,
    max_retries: int = 2,
) -> VideoReproductionPlan:
    """Generate content with retry on truncation or validation errors."""

    for attempt in range(max_retries + 1):
        if verbose and attempt > 0:
            print(f"  Retry attempt {attempt}...", file=sys.stderr)

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.7,
                max_output_tokens=65536,
            ),
        )

        token_usage.add(response)

        raw = response.text
        if verbose:
            print(f"  Response length: {len(raw)} chars", file=sys.stderr)
            if response.usage_metadata:
                meta = response.usage_metadata
                print(
                    f"  Tokens — prompt: {getattr(meta, 'prompt_token_count', '?')}, "
                    f"completion: {getattr(meta, 'candidates_token_count', '?')}, "
                    f"total: {getattr(meta, 'total_token_count', '?')}",
                    file=sys.stderr,
                )

        # Check if response was truncated
        truncated = False
        if response.candidates and response.candidates[0].finish_reason:
            reason = str(response.candidates[0].finish_reason)
            if "MAX_TOKENS" in reason or "LENGTH" in reason:
                truncated = True
                if verbose:
                    print(f"  Response truncated (reason: {reason})", file=sys.stderr)

        # Try to parse
        try:
            plan = VideoReproductionPlan.model_validate_json(raw)
            return plan
        except Exception as e:
            if attempt < max_retries:
                if truncated:
                    print(
                        "  Output truncated, retrying with condensed request...",
                        file=sys.stderr,
                    )
                    condensed_prompt = (
                        user_prompt
                        + "\n\nIMPORTANT: Keep the total response under 50000 characters. "
                        "Limit to the most important scenes (max 15 scenes). "
                        "Keep prompts concise but complete."
                    )
                    contents = [
                        types.Content(
                            parts=[
                                types.Part.from_uri(
                                    file_uri=uploaded_file.uri,
                                    mime_type=uploaded_file.mime_type,
                                ),
                                types.Part.from_text(text=condensed_prompt),
                            ]
                        )
                    ]
                else:
                    print(f"  Parse error, retrying: {e}", file=sys.stderr)
                continue
            raise RuntimeError(
                f"Failed to parse Gemini response after {max_retries + 1} attempts: {e}"
            ) from e

    raise RuntimeError("Unexpected: exhausted retries without returning or raising")


def analyze_video(
    video_path: Path,
    mode: str,
    target_language: str,
    video_metadata: dict,
    config: Config,
    style: str = "realistic",
    verbose: bool = False,
) -> AnalysisResult:
    """Upload video to Gemini and produce a structured reproduction plan."""

    client = genai.Client(api_key=config.gemini_api_key)
    token_usage = TokenUsage()

    # Step 1: Upload video file
    print("[2/4] Uploading to Gemini...", file=sys.stderr)
    uploaded_file = client.files.upload(file=video_path)

    # Wait for file to be processed
    _wait_for_file_active(client, uploaded_file, verbose=verbose)
    if verbose:
        print(f"  File ready: {uploaded_file.name}", file=sys.stderr)

    # Step 2: Build prompts
    system_prompt = get_system_prompt(
        mode=mode, target_language=target_language, style=style
    )
    user_prompt = get_user_prompt(
        mode=mode,
        target_language=target_language,
        video_metadata=video_metadata,
        style=style,
    )

    # Step 3: Build schema
    schema = resolve_schema_refs(VideoReproductionPlan.model_json_schema())

    # Step 4: Generate structured content
    print("[3/4] Analyzing video...", file=sys.stderr)

    contents = [
        types.Content(
            parts=[
                types.Part.from_uri(
                    file_uri=uploaded_file.uri,
                    mime_type=uploaded_file.mime_type,
                ),
                types.Part.from_text(text=user_prompt),
            ]
        )
    ]

    plan = _generate_with_retry(
        client=client,
        model=config.model_name,
        contents=contents,
        system_prompt=system_prompt,
        schema=schema,
        uploaded_file=uploaded_file,
        user_prompt=user_prompt,
        token_usage=token_usage,
        verbose=verbose,
    )

    # Step 5: Post-process voiceover text
    print("[4/4] Generating reproduction plan...", file=sys.stderr)
    plan = humanize_voiceovers(plan)

    # Step 6: Cleanup uploaded file
    try:
        client.files.delete(name=uploaded_file.name)
    except Exception:
        pass  # Best-effort cleanup

    return AnalysisResult(plan=plan, token_usage=token_usage)
