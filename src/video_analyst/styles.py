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
    "kurzgesagt": {
        "label": "Kurzgesagt Flat Design",
        "description": "Vibrant flat vector — rounded shapes, bold colors, clean infographic aesthetic",
        "video_directive": (
            "Kurzgesagt flat design motion graphics style. Clean vector animation "
            "with rounded geometric shapes and bold vibrant colors on dark backgrounds. "
            "Smooth gradient shading, no outlines, simplified cute characters with "
            "dot eyes. Rich jewel-tone palette — deep blues, warm oranges, bright "
            "teals, vivid magentas. Subtle particle effects and glowing accents. "
            "Smooth satisfying transitions and fluid motion."
        ),
        "image_directive": (
            "Kurzgesagt flat design illustration, clean vector art with rounded "
            "geometric shapes, bold vibrant colors on dark background, smooth "
            "gradients, no outlines, simplified cute characters with dot eyes, "
            "rich jewel-tone palette, subtle glow effects, infographic aesthetic."
        ),
    },
    "synthwave": {
        "label": "Synthwave Retrowave",
        "description": "80s retro-futuristic — neon grids, chrome, sunset gradients, laser lines",
        "video_directive": (
            "Synthwave retrowave aesthetic. Neon-lit 1980s retro-futuristic world "
            "with perspective grid landscapes vanishing into glowing horizons. "
            "Chrome and metallic surfaces reflecting neon pink, electric purple, "
            "and hot cyan. Sunset gradient skies from deep purple to hot pink. "
            "Laser scan lines, lens flares, and deep glow bloom effects. "
            "Smooth cinematic camera movement across digital landscapes."
        ),
        "image_directive": (
            "Synthwave retrowave art, neon-lit 1980s retro-futuristic scene, "
            "perspective grid landscape, chrome metallic surfaces, neon pink "
            "and electric purple and hot cyan palette, sunset gradient sky, "
            "laser scan lines, deep glow bloom effects, retro-futuristic."
        ),
    },
    "comic-book": {
        "label": "Comic Book Pop Art",
        "description": "Bold ink outlines, halftone dots, vivid primary colors, dynamic panels",
        "video_directive": (
            "Comic book pop art style. Bold black ink outlines, vivid primary "
            "colors — red, blue, yellow — with Ben-Day halftone dot shading. "
            "Dynamic Dutch angles and dramatic foreshortening. Speed lines for "
            "motion, impact bursts, and graphic onomatopoeia. High contrast "
            "cel shading with flat color fills. Punchy, energetic composition."
        ),
        "image_directive": (
            "Comic book pop art illustration, bold black ink outlines, vivid "
            "primary colors, Ben-Day halftone dot shading, dynamic composition, "
            "speed lines, high contrast cel shading, flat color fills, "
            "graphic novel aesthetic."
        ),
    },
    "pixel-art": {
        "label": "Pixel Art Retro",
        "description": "Retro 16-bit gaming — chunky pixels, limited palette, nostalgic charm",
        "video_directive": (
            "16-bit pixel art animation style. Chunky visible pixels with a "
            "limited but vibrant color palette. Smooth sub-pixel animation with "
            "satisfying frame-by-frame motion. Rich parallax scrolling backgrounds "
            "with detailed pixel environments. Dithering for gradients, crisp "
            "pixel-perfect edges. Nostalgic retro gaming aesthetic with modern "
            "color depth."
        ),
        "image_directive": (
            "16-bit pixel art illustration, chunky visible pixels, limited "
            "vibrant color palette, dithering for gradients, pixel-perfect "
            "edges, detailed pixel environment, nostalgic retro gaming aesthetic."
        ),
    },
    "paper-cutout": {
        "label": "Paper Cutout Craft",
        "description": "Layered paper craft — textured cardstock, visible layers, handmade charm",
        "video_directive": (
            "Paper cutout stop-motion animation style. Characters and environments "
            "made from layered textured cardstock and craft paper. Visible paper "
            "grain and fiber texture, slightly imperfect hand-cut edges. Subtle "
            "drop shadows between paper layers creating depth. Warm soft lighting "
            "as if on a physical craft table. Charming handmade aesthetic with "
            "gentle, slightly jerky stop-motion movement."
        ),
        "image_directive": (
            "Paper cutout craft illustration, layered textured cardstock, "
            "visible paper grain and fiber, hand-cut edges, drop shadows "
            "between layers, warm soft lighting, charming handmade aesthetic, "
            "paper craft collage style."
        ),
    },
    "low-poly": {
        "label": "Low Poly Geometric",
        "description": "Faceted 3D geometry — crystalline surfaces, vibrant gradients, modern minimal",
        "video_directive": (
            "Low poly 3D animation style. Faceted geometric surfaces with flat "
            "triangular polygons creating crystalline, angular forms. Vibrant "
            "color gradients across polygon faces with subtle lighting variation. "
            "Clean minimal environments with bold color blocking. Smooth camera "
            "orbits revealing geometric depth. Modern, stylized aesthetic with "
            "sharp clean edges and no texture maps."
        ),
        "image_directive": (
            "Low poly 3D illustration, faceted geometric surfaces with flat "
            "triangular polygons, crystalline angular forms, vibrant color "
            "gradients across faces, clean minimal composition, bold color "
            "blocking, sharp edges, modern stylized aesthetic."
        ),
    },
    "claymation": {
        "label": "Claymation Stop-Motion",
        "description": "Clay animation — tactile sculpted figures, fingerprint textures, warm lighting",
        "video_directive": (
            "Claymation stop-motion animation style. Characters and sets sculpted "
            "from modeling clay with visible fingerprint impressions and tool marks. "
            "Slightly bumpy imperfect surfaces with rich saturated clay colors. "
            "Warm studio lighting with soft shadows. Charming slightly jerky "
            "stop-motion movement at 12fps. Physical miniature set pieces with "
            "tactile handcrafted quality."
        ),
        "image_directive": (
            "Claymation style, sculpted modeling clay characters, visible "
            "fingerprint textures and tool marks, bumpy imperfect surfaces, "
            "rich saturated clay colors, warm studio lighting, miniature set, "
            "tactile handcrafted quality."
        ),
    },
    "vaporwave": {
        "label": "Vaporwave Aesthetic",
        "description": "90s surreal digital — pastel gradients, glitch effects, marble busts, retro tech",
        "video_directive": (
            "Vaporwave aesthetic. Dreamy surreal 90s digital world with pastel "
            "pink, lavender, and mint gradients. Glitch effects, scan lines, and "
            "chromatic aberration. Classical Greek marble statues and busts in "
            "neon-lit digital spaces. Retro computer UI elements, checkerboard "
            "floors, palm trees, and Japanese text. Lo-fi VHS quality with "
            "tracking artifacts and color bleeding."
        ),
        "image_directive": (
            "Vaporwave aesthetic, dreamy surreal 90s digital art, pastel pink "
            "and lavender and mint gradients, glitch effects, scan lines, "
            "Greek marble busts, neon-lit digital space, retro computer elements, "
            "lo-fi VHS quality, chromatic aberration."
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
