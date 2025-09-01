#!/usr/bin/env python3
"""
Jaidha's Living Room Designer - Simple Script
"""

import glob
import asyncio
import random
from datetime import datetime
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

# Tightened palettes and presets
FURNITURE_WOOD_TONES = [
    "mid walnut wood - neutral brown - matte finish"
]

RUG_STYLES = [
    "Indian dhurrie rug in deep red with traditional patterns",
    "Indian dhurrie rug in forest green with geometric motifs",
    "Indian dhurrie rug in warm beige with subtle patterns",
    "natural woven jute rug - light sand",
    "subtle Persian style rug - faded warm neutrals",
    "minimal wool flatweave - light gray"
]

WALL_TREATMENT_PRESETS = [
    # 1
    "Subtle picture-frame trim - slim 3/4in stiles and rails - same paint as wall - matte - 2 or 3 frames per bay - no crown - no base change.",
    # 2
    "Narrow vertical panels behind the fireplace only - 3in spacing - painted the same color as surrounding wall - matte - flanking bays remain plain.",
    # 3
    "Soft limewash in warm off-white (slight movement) on flanking bays - leave fireplace plane crisp white for contrast.",
    # 4
    "Light greige wall with a single mid-walnut shelf per side - thin profile - no additional shelving - negative space prioritized.",
    # 5
    "Fireplace accent wall painted deep navy blue - all other walls crisp white - fireplace wall only gets the color treatment.",
    # 6
    "Fireplace accent wall painted warm terracotta - all other walls crisp white - fireplace wall only gets the color treatment.",
    # 7
    "Fireplace accent wall painted sage green - all other walls crisp white - fireplace wall only gets the color treatment.",
    # 8
    "Fireplace accent wall painted charcoal gray - all other walls crisp white - fireplace wall only gets the color treatment.",
    # 9
    "Fireplace accent wall painted warm taupe - all other walls crisp white - fireplace wall only gets the color treatment.",
    # 10
    "Fireplace accent wall painted dusty rose - all other walls crisp white - fireplace wall only gets the color treatment."
]

HARD_CONSTRAINTS = """
HARD CONSTRAINTS (MUST FOLLOW):
- Couch must be fixed on the 106" wall, facing the projector.
- Must not block stairs, stair rail, or stair opening.
- Leave vent left of fireplace visible.
- Maintain at least 36" walkway from stairs to sliding door.
- Keep all furniture at least 8" clear of sliding door track.
- Left bay furniture depth must be ≤9.75"; right side furniture ≤18".
"""

NEGATIVE_PROMPTS = """
DO NOT:
- Do not apply more than one wall treatment per render.
- Do not cover every wall with paneling or slats.
- Do not use thick grid paneling, shiplap, beadboard, rustic slats, or wainscoting.
- Do not introduce red, orange, cherry, or teak woods. Use mid walnut only.
- Do not use glossy paint, high contrast gallery walls, or heavy clutter.
- Do not add black bookcases or black console tables.
- Do not add additional furniture beyond one console and two open shelves total.
- Do not place TV above fireplace (projector only).
- Do not move, add, or remove windows, doors, or fireplace.
- Do not block or cover stair sconce.
- Do not cover sliding door.
- Do not block or cover vent left of fireplace.
"""

STYLE_GUARDRAILS = """
SCOPE OF CHANGE:
- Change the wall treatment only. One treatment max.
- Keep at least 40% of the wall surface plain.

MATERIAL UNIFICATION:
- Single wood family: mid walnut - matte. No other wood tones.

OBJECT BUDGET:
- Max 7 styled objects per side (books count as 1 group).
- Max 1 plant per side. No gallery walls. No overlapping frames.

COMPOSITION:
- If shelves are present, use at most 2 floating shelves per side.
- Prefer negative space around art and objects.
"""

CAMERA_PROMPT = """
CAMERA VIEWPOINT:
- Show the back of the grey couch centered in foreground.
- Fireplace wall centered in background.
- Same focal length and vantage as source. No wide angle exaggeration.
"""

def create_dynamic_prompt(variation_index: int, wall_treatment: str) -> DesignPrompt:
    """Create a deterministic prompt with controlled random diversity per iteration."""
    random.seed(variation_index + 2025)

    furniture_color = FURNITURE_WOOD_TONES[0]
    rug_style = random.choice(RUG_STYLES)  # includes Indian rugs now

    base_furniture = [
        "existing grey leather couch - keep exactly as is",
        "existing floors - keep exactly as is",
        "grey couch faces the projector"
    ]

    # Add floating shelves on left and mirrors on right
    left_side_furniture = [
        f"{furniture_color} floating shelves - left bay only - depth <= 9.75in - 2 shelves max",
        f"{furniture_color} console table - left bay only - depth <= 9.75in"
    ]
    
    right_side_furniture = [
        "brass framed round mirror - right side - max 30in diameter",
        "brass framed rectangular mirror - right side - max 36in height",
        f"{furniture_color} side table - right side - depth <= 18in"
    ]

    # tightly scoped and consistent with mid-century
    furniture_requirements = base_furniture + left_side_furniture + right_side_furniture + [
        f"{furniture_color} coffee table - simple rectangular - thin legs",
        "one pair of mid-century armchairs - light tan leather or oatmeal fabric",
        rug_style,
        "one floor lamp with fabric shade - warm white bulb",
        "a few ceramic objects in matte white - no bright colors"
    ]

    additional_notes = f"""
    CRITICAL REQUIREMENTS:
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.

    EXACT ROOM DIMENSIONS:
    - Left bay depth 9.75in max
    - Right side furniture 18in max depth
    - 55.5in left bay width
    - 55in to staircase on right, 38in to sconce
    - 106in back sofa wall, 168in sliding door wall

    {HARD_CONSTRAINTS}

    WALL TREATMENT - VARIATION {variation_index + 1}:
    {wall_treatment}

    FURNITURE PLACEMENT:
    - LEFT SIDE: Floating shelves and console table only
    - RIGHT SIDE: Mirrors and side table only
    - Keep furniture within depth limits (left ≤9.75in, right ≤18in)

    MATERIAL AND COLOR RULES:
    - Walls: soft warm gray or off-white, matte (unless accent wall specified).
    - Wood: {furniture_color}. Absolutely no red/orange wood.
    - Metals: small brass accents only.

    {STYLE_GUARDRAILS}
    {NEGATIVE_PROMPTS}
    {CAMERA_PROMPT}

    DESIGN INTENT:
    - Quiet, modern, and elevated. Subtle detail over bold patterns.
    - Prioritize negative space. Avoid visual heaviness.
    - Styling should feel airy and uncluttered.

    MUST PRESERVE:
    - Existing couch, floors, openings, fireplace, window and door positions.
    - Vent left of fireplace remains visible.
    """

    return DesignPrompt(
        style="quiet modern with mid-century influence",
        color_scheme="soft warm grays, white, mid walnut, brass accents",
        mood="calm, airy, refined, comfortable",
        furniture_requirements=furniture_requirements,
        additional_notes=additional_notes
    )

async def main():
    print("🎨 Jaidha's Living Room Designer")
    print("=" * 50)
    designer = InteriorDesigner()
    room_specs = RoomSpecs(
        width=14.0,
        length=8.83,
        height=9.0,
        room_type="living room"
    )
    current_room_paths = glob.glob("current/*")
    print(f"Found {len(current_room_paths)} current room images")
    
    # Deterministic: one variation per wall treatment preset (now 10 options)
    num_variations = len(WALL_TREATMENT_PRESETS)
    prompts = [create_dynamic_prompt(i, WALL_TREATMENT_PRESETS[i]) for i in range(num_variations)]
    
    variations, output_dir = await designer.generate_variations(
        current_room_paths=current_room_paths,
        room_specs=room_specs,
        design_prompt=None,
        num_variations=num_variations,
        prompts=prompts
    )
    print(f"\n✅ Generated {len(variations)} variations!")

if __name__ == "__main__":
    asyncio.run(main())
