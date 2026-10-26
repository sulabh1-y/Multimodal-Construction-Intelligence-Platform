"""Pollinations AI Conceptual 3D Architectural Rendering Integration (Epic 3).

Generates high-fidelity conceptual 3D architectural renders via the free Pollinations AI API.
Provides architectural style presets, lighting options, and camera angle controls.
"""

import urllib.parse
import random
from typing import Dict, Any

STYLE_PRESETS = {
    "Sustainable Biophilic": "lush vertical gardens, hanging green balconies, solar pergolas, timber battens, integrated rainwater harvesting channels",
    "Modern Parametric Glass": "curved double-glazed curtain wall, aerodynamic aerodynamic sun-shading louvers, sleek metallic mullions, soaring atrium",
    "Contemporary Indian Urban": "terracotta jali screens, shaded courtyards, exposed concrete finishes, cantilevered cantilever balconies, warm ambient illumination",
    "Industrial Precast Tech": "exposed structural steel truss work, polished concrete floors, expansive glass clerestory windows, modular steel portal frame",
    "Luxury Tropical Minimalist": "frameless glass walls, cantilevered infinity deck, natural teak wood panels, water reflection ponds, dramatic night uplighting"
}

LIGHTING_PRESETS = {
    "Crisp Architectural Daylight": "bright midday natural sunlight, sharp crisp shadows, clear azure sky, ultra-clear building details",
    "Golden Hour Sunset": "warm orange and gold low-angle sunlight, long soft shadows, dramatic warm reflections on glass facade",
    "Dramatic Twilight Blue Hour": "deep sapphire twilight sky, warm interior LED architectural lighting glowing through glass, exterior uplights",
    "Overcast Diffused": "soft diffused architectural light, balanced neutral tones, hyper-realistic materiality and texture"
}

CAMERA_ANGLES = {
    "Eye-Level Street Hero Perspective": "photorealistic street-level eye-level architectural photography shot from pedestrian promenade",
    "Dynamic Low-Angle Drone": "low-angle dramatic drone aerial view capturing the full building height and structural grandeur",
    "Three-Quarter Corner View": "classic 3/4 axonometric perspective highlighting both facade elevations and structural entrance canopy"
}

def generate_architectural_prompt(
    structure_type: str,
    style_choice: str = "Sustainable Biophilic",
    lighting_choice: str = "Golden Hour Sunset",
    camera_choice: str = "Eye-Level Street Hero Perspective",
    extra_keywords: str = ""
) -> str:
    """Constructs an expert-level text prompt tailored for Pollinations / Flux architectural rendering."""
    style_desc = STYLE_PRESETS.get(style_choice, list(STYLE_PRESETS.values())[0])
    light_desc = LIGHTING_PRESETS.get(lighting_choice, list(LIGHTING_PRESETS.values())[0])
    cam_desc = CAMERA_ANGLES.get(camera_choice, list(CAMERA_ANGLES.values())[0])
    
    prompt = (
        f"Masterpiece 3D architectural rendering of a {structure_type}. "
        f"Design features {style_desc}. "
        f"{cam_desc}, illuminated by {light_desc}. "
        f"Rendered in Unreal Engine 5, Octane render, V-Ray 6, hyper-realistic, photorealistic 8k, architectural visualization award winner."
    )
    if extra_keywords.strip():
        prompt += f" Additional details: {extra_keywords.strip()}."
    return prompt

def build_pollinations_image_url(prompt: str, seed: int = None, width: int = 1024, height: int = 768) -> str:
    """Builds a direct Pollinations.ai image URL for rendering."""
    if seed is None:
        seed = random.randint(1000, 999999)
    encoded_prompt = urllib.parse.quote_plus(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
    return url
