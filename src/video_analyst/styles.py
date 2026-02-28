"""Predefined visual styles for video generation prompts."""

from __future__ import annotations

# Each style has a name, a short description, and a style directive
# that gets injected into every video_prompt and t2i_prompt.
STYLES: dict[str, dict[str, str]] = {
    "realistic": {
        "label": "Ultra Realistic (default)",
        "description": "Photorealistic, cinematic quality — indistinguishable from real footage",
        "video_directive": (
            "Ultra-realistic rendering, shot on 35mm film with natural grain and "
            "subtle chromatic aberration. Professional cinematography, shallow depth "
            "of field. Natural lighting with micro-imperfections. "
            "No stylization, no AI look."
        ),
        "image_directive": (
            "Photorealistic, shot on 35mm film, natural grain, professional "
            "photography lighting, shallow depth of field, subtle lens flare. "
            "RAW photo quality."
        ),
    },
    "cinematic": {
        "label": "Cinematic Blockbuster",
        "description": "Hollywood blockbuster look — anamorphic, dramatic lighting, color graded",
        "video_directive": (
            "Cinematic blockbuster quality, shot on Arri Alexa with anamorphic "
            "lens. Dramatic three-point lighting, teal and orange color grade. "
            "Lens flares, volumetric lighting, film grain. IMAX quality."
        ),
        "image_directive": (
            "Cinematic blockbuster still frame, anamorphic bokeh with subtle "
            "horizontal flares, dramatic lighting, teal and orange color palette, "
            "shot on Arri Alexa. IMAX quality."
        ),
    },
    "ghibli": {
        "label": "Studio Ghibli",
        "description": "Hand-painted anime — lush backgrounds, soft colors, whimsical atmosphere",
        "video_directive": (
            "Studio Ghibli hand-drawn animation style. Lush, detailed painted "
            "backgrounds with soft watercolor textures. Warm, vibrant colors. "
            "Gentle character movements, whimsical atmosphere. Soft natural lighting."
        ),
        "image_directive": (
            "Studio Ghibli art style, hand-painted illustration with detailed "
            "watercolor backgrounds, soft warm colors, whimsical and serene "
            "atmosphere, gentle natural lighting."
        ),
    },
    "wes-anderson": {
        "label": "Wes Anderson",
        "description": "Symmetrical compositions, pastel palette, meticulous production design",
        "video_directive": (
            "Wes Anderson visual style. Perfectly symmetrical centered composition, "
            "pastel color palette with muted pinks, yellows, and teals. Flat front "
            "camera angle, meticulous production design, whimsical set decoration. "
            "Soft diffused lighting."
        ),
        "image_directive": (
            "Wes Anderson aesthetic, perfectly symmetrical centered composition, "
            "pastel color palette, meticulous production design, flat frontal "
            "camera angle, whimsical vintage set decoration."
        ),
    },
    "noir": {
        "label": "Film Noir",
        "description": "High contrast black and white, dramatic shadows, 1940s atmosphere",
        "video_directive": (
            "Classic film noir style. High contrast black and white cinematography, "
            "dramatic chiaroscuro lighting with deep shadows and bright highlights. "
            "Venetian blind shadow patterns, wet reflective streets, "
            "1940s urban atmosphere. Shot on vintage 35mm film with heavy grain."
        ),
        "image_directive": (
            "Film noir aesthetic, high contrast black and white, dramatic "
            "chiaroscuro lighting, deep shadows, venetian blind shadow patterns, "
            "1940s urban atmosphere, vintage 35mm grain."
        ),
    },
    "cyberpunk": {
        "label": "Cyberpunk Neon",
        "description": "Neon-lit dystopia — dark environments, vibrant neon, rain-slicked streets",
        "video_directive": (
            "Cyberpunk neon aesthetic. Dark dystopian urban environment drenched "
            "in vibrant neon lights — magenta, cyan, electric blue. Rain-slicked "
            "streets with neon reflections, holographic advertisements, "
            "dense atmosphere with fog and volumetric lighting. Cool teal shadows."
        ),
        "image_directive": (
            "Cyberpunk neon aesthetic, dark urban dystopia, vibrant magenta and "
            "cyan neon lights, rain-slicked streets with neon reflections, "
            "holographic elements, volumetric fog, cool teal shadows."
        ),
    },
    "vintage-film": {
        "label": "Vintage 70s Film",
        "description": "Warm analog film — heavy grain, faded colors, retro lens characteristics",
        "video_directive": (
            "Retro 1970s film aesthetic, shot on 16mm Kodak film stock. Heavy "
            "natural grain, warm faded color palette with golden highlights and "
            "muted shadows. Soft halation around bright areas, slight vignetting. "
            "Handheld camera with subtle organic movement."
        ),
        "image_directive": (
            "1970s vintage film photography, shot on Kodak film stock, heavy "
            "natural grain, warm faded colors, golden highlights, soft halation, "
            "slight vignetting, analog aesthetic."
        ),
    },
    "anime": {
        "label": "Modern Anime",
        "description": "Clean anime aesthetic — sharp linework, dynamic angles, vivid colors",
        "video_directive": (
            "Modern anime animation style with clean sharp linework, vivid "
            "saturated colors, dynamic camera angles. Detailed character animation "
            "with expressive features. Atmospheric lighting with dramatic lens "
            "flares and particle effects."
        ),
        "image_directive": (
            "Modern anime illustration style, clean sharp linework, vivid "
            "saturated colors, detailed character design with expressive features, "
            "atmospheric lighting, dynamic composition."
        ),
    },
    "watercolor": {
        "label": "Watercolor Painting",
        "description": "Soft painted aesthetic — visible brush strokes, flowing colors, dreamy",
        "video_directive": (
            "Watercolor painting animation style. Soft, flowing colors that bleed "
            "into each other with visible paper texture. Delicate brush strokes, "
            "gentle pastel palette with occasional vivid accents. Dreamy, "
            "ethereal atmosphere with soft diffused lighting."
        ),
        "image_directive": (
            "Watercolor painting style, soft flowing colors with visible paper "
            "texture, delicate brush strokes, gentle pastel palette, dreamy "
            "ethereal atmosphere, artistic and impressionistic."
        ),
    },
    "documentary": {
        "label": "Documentary",
        "description": "Raw, authentic footage — handheld camera, natural light, unpolished",
        "video_directive": (
            "Handheld documentary style, shot on 16mm film. Natural available "
            "lighting, slightly grainy, unpolished and authentic. Real-world "
            "imperfections, natural camera shake. Raw, intimate perspective."
        ),
        "image_directive": (
            "Documentary photography style, natural available lighting, "
            "slightly grainy, authentic and unpolished, shot on 16mm film, "
            "raw intimate perspective."
        ),
    },
}

# Sorted list for CLI display
STYLE_NAMES = sorted(STYLES.keys())


def get_style(name: str) -> dict[str, str]:
    """Get a style definition by name. Defaults to 'realistic'."""
    return STYLES.get(name, STYLES["realistic"])


def list_styles() -> str:
    """Format all available styles for display."""
    lines = []
    for name in STYLE_NAMES:
        style = STYLES[name]
        lines.append(f"  {name:16s} {style['description']}")
    return "\n".join(lines)
