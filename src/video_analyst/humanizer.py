"""Post-process voiceover text to remove AI writing patterns.

Based on the humanizer skill: removes common AI-generated text patterns
to make voiceover sound more natural and human.
"""

from __future__ import annotations

import re

from .models import VideoReproductionPlan

# Phrases that signal AI-generated text
AI_HEDGE_PHRASES = [
    r"\bIt'?s worth noting that\b",
    r"\bInterestingly enough\b",
    r"\bInterestingly,\b",
    r"\bIt'?s important to note that\b",
    r"\bIt'?s important to remember that\b",
    r"\bIn today'?s world\b",
    r"\bIn today'?s digital age\b",
    r"\bAt the end of the day\b",
    r"\bThe reality is\b",
    r"\bHere'?s the thing\b",
    r"\bLet'?s be honest\b",
    r"\bLet'?s dive in\b",
    r"\bLet'?s explore\b",
    r"\bWithout further ado\b",
    r"\bIn this day and age\b",
    r"\bIt goes without saying\b",
    r"\bAs we all know\b",
    r"\bNeedless to say\b",
]

# Formulaic transitions
AI_TRANSITIONS = [
    r"^So, ",
    r"^Now, ",
    r"^Well, ",
    r"^Moving on,? ",
    r"^Let'?s move on to ",
    r"^Now let'?s ",
    r"^Speaking of which,? ",
    r"^That being said,? ",
    r"^With that in mind,? ",
    r"^Having said that,? ",
]

# Overly formal constructions that should use contractions
FORMAL_TO_CONTRACTION = [
    (r"\bdo not\b", "don't"),
    (r"\bcannot\b", "can't"),
    (r"\bwill not\b", "won't"),
    (r"\bshould not\b", "shouldn't"),
    (r"\bwould not\b", "wouldn't"),
    (r"\bcould not\b", "couldn't"),
    (r"\bI am\b", "I'm"),
    (r"\bthey are\b", "they're"),
    (r"\bwe are\b", "we're"),
    (r"\bit is\b", "it's"),
    (r"\bthat is\b", "that's"),
]


def _clean_text(text: str) -> str:
    """Remove AI writing patterns from a single text."""
    if not text:
        return text

    result = text

    # Remove hedge phrases
    for pattern in AI_HEDGE_PHRASES:
        result = re.sub(pattern, "", result, flags=re.IGNORECASE)

    # Remove formulaic transitions at sentence starts
    sentences = result.split(". ")
    cleaned_sentences = []
    for sentence in sentences:
        s = sentence.strip()
        for pattern in AI_TRANSITIONS:
            s = re.sub(pattern, "", s, flags=re.IGNORECASE)
        if s:
            cleaned_sentences.append(s)
    result = ". ".join(cleaned_sentences)

    # Apply contractions for more natural speech
    for formal, contraction in FORMAL_TO_CONTRACTION:
        result = re.sub(formal, contraction, result, flags=re.IGNORECASE)

    # Clean up double spaces and punctuation artifacts
    result = re.sub(r"  +", " ", result)
    result = re.sub(r"\. \.", ".", result)
    result = re.sub(r",\s*,", ",", result)
    result = result.strip()

    return result


def humanize_voiceovers(plan: VideoReproductionPlan) -> VideoReproductionPlan:
    """Post-process all voiceover text fields in the plan."""
    for scene in plan.scenes:
        scene.voiceover_text = _clean_text(scene.voiceover_text)
    return plan
