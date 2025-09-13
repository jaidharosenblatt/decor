#!/usr/bin/env python3
import asyncio
import glob

from interior_designer import InteriorDesigner

# Lighting / time-of-day scenes
LIGHTING_PRESETS = [
    """TIME OF DAY: Daytime (soft overcast).
    Primary light source is daylight; windows are bright but not blown out.
    Track lights 10%, floor lamp OFF. White balance ~4500K.
    Exposure naturalistic for interiors; colors remain true.""",
]

ACCENT_WALL_INSTRUCTIONS = """
CRITICAL PAINT AND LIGHTING INSTRUCTIONS:
- Use the EXACT color from the paint CARDS (the small swatches), NOT the washed-out wall samples
- Match the SATURATED, RICH appearance of the paint cards themselves
- LIGHTING: The accent wall receives INDIRECT, WARM ambient lighting (not direct daylight)
- Colors must appear RICH and VIBRANT like they do on the fireplace wall in the reference image
- AVOID the pale, washed-out appearance seen on the left wall in the reference (that's from direct sunlight)
- Use warm 3000K lighting on accent surfaces to show full color depth and vibrancy
- Accent wall color must EXTEND FULLY into the staircase wall plane (no sharp cutoff)
- Fireplace bump-out must be the SAME COLOR as the surrounding accent (no white stripe)
- CRITICAL: All other walls (left wall with sliding door, right wall, etc.) must remain BRIGHT WHITE
- Accent colors should match the DEPTH and RICHNESS as shown on the paint swatches themselves

"""

# FINALISTS — unified color across fireplace bump-out and flanking planes.
WALL_TREATMENT_PRESETS = [
    "Use the 1st color swatch (leftmost warm beige) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 2nd color swatch (medium warm tan) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 3rd color swatch (peach/salmon tone) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 4th color swatch (terracotta/rust) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 5th color swatch (sage green) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
]

HARD_CONSTRAINTS = """
HARD CONSTRAINTS (MUST FOLLOW):
- Couch must be fixed on the 106" wall, facing the projector, PUSHED COMPLETELY AGAINST THE WALL.
- CRITICAL: Grey couch back must be flush against the accent wall with zero gap.
- Must not block stairs, stair rail, or stair opening.
- Leave vent left of fireplace visible.
- Maintain at least 36" walkway from stairs to sliding door.
- Keep all furniture at least 8" clear of sliding door track.
- Left bay furniture depth must be ≤9.75"; right side furniture ≤18".
"""

NEGATIVE_PROMPTS = """
DO NOT:
- Do not use glossy paint, high contrast gallery walls, or heavy clutter.
- Do not place TV above fireplace (projector only).
- Do not move, add, or remove windows, doors, or fireplace.
- Do not block or cover stair sconce.
- Do not cover sliding door.
- Do not block or cover vent left of fireplace.
- Do not block the entrance to the staircase.
"""


CAMERA_PROMPT = """
CAMERA VIEWPOINT:
- Show the back of the grey couch centered in foreground.
- Fireplace wall centered in background.
- Same focal length and vantage as source. No wide angle exaggeration.
"""


def create_dynamic_prompt(
    variation_index: int, wall_treatment: str, lighting: str
) -> str:
    """Create a deterministic prompt with controlled diversity per iteration."""

    additional_notes = f"""
    IMAGE REFERENCES:
    - Room layout images: Use for current room geometry and layout (DO NOT ALTER)
    - Paint colors image: Contains 5 color swatches for accent wall selection (use EXACT colors)
    - Rug image (3. rug.png): Traditional red/burgundy ornate area rug to be placed in the room
    - Floating shelves image: Shelves for the left fireplace bay
    - Couch image: Existing grey leather couch to keep in place

    CRITICAL REQUIREMENTS:
    - Use the current room images as a reference for the layout of the room. DO NOT ALTER THE LAYOUT.
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.
    - Keep existing couch facing the projector. Show only the front half of the couch.

    EXACT ROOM DIMENSIONS:
    - Left bay depth 9.75in max
    - Right side furniture 18in max depth
    - 55.5in left bay width
    - 55in to staircase on right, 38in to sconce
    - 106in back sofa wall, 168in sliding door wall

    {HARD_CONSTRAINTS}

    WALL TREATMENT
    {wall_treatment}

    LIGHTING & TIME OF DAY:
    {lighting}

    FURNITURE:

    Rug: CRITICAL - Use the traditional red/burgundy ornate rug from the rug image (3. rug.png) - NOT any other rug

    On the left wall, a tall thin mid century modern lamp. Lamp is 12 inches from the sliding door.

    Couch:
    - existing grey leather couch facing the projector
    - CRITICAL: the back of the couch is FLUSH AGAINST the accent wall with NO GAP
    - the couch back is completely touching the wall, pushed all the way back
    - back legs of couch are off of the rug

    Fireplace wall:
    Left bay (left of fireplace):
    6 Floating shelves (use provided shelves image) 8in deep, 48 in wide (leave 10 inch gap on each side) Filled with green plants, mid century decor, and minimalistic books.

    Right bay (right of fireplace):
    Short hutch positioned DIRECTLY next to the fireplace wall (not centered in bay, but close to fireplace) with a round mirror hung above it on the wall

    Accent chairs:
    CRITICAL CHAIR POSITIONING - READ CAREFULLY:
    - 2 matching brown fabric swivel accent chairs positioned on EACH SIDE of the couch
    - ORIENTATION: Each chair must be turned 45 DEGREES INWARD toward the CENTER of the couch
    - Chairs should create a CONVERSATION CIRCLE with the couch, NOT face the fireplace/projector
    - Think "chairs facing each other across the couch" not "all furniture facing the TV"
    - The goal is INTIMATE CONVERSATION SEATING, not media viewing alignment
    - Position: Adequate spacing from couch (NOT pinned against couch)
   
    PHOTO BEHAVIOR:
    - Do not show the projector screen; keep it retracted.
    - No flash. Use naturalistic interior lighting and accurate exposure.

    FURNITURE PLACEMENT:
    - Keep furniture within depth limits (left ≤9.75in, right ≤18in)

    {NEGATIVE_PROMPTS}
    {CAMERA_PROMPT}

    DESIGN INTENT:
    - Quiet, modern, and elevated. Subtle detail over bold patterns.
    - Prioritize negative space. Avoid visual heaviness.

    MUST PRESERVE:
    - Existing couch, floors, openings, fireplace, window and door positions.
    - Vent left of fireplace remains visible.
    """

    return additional_notes


async def main():
    print("🎨 Jaidha's Living Room Designer")
    print("=" * 50)
    all_images = glob.glob("input/living_room/*")
    print(f"Found {len(all_images)} living room images")

    if not all_images:
        print("❌ No images found in input/living_room/")
        print("Please add your images to this directory first.")
        return

    for img in all_images:
        print(f"  - {img}")
    # Generate variations using nested loops
    prompts = []
    variation_index = 0

    for wall_treatment in WALL_TREATMENT_PRESETS:
        for lighting in LIGHTING_PRESETS:
            print(
                f"Variation {variation_index}: Wall treatment: {wall_treatment[:50]}..., Lighting: {lighting[:50]}..."
            )
            prompts.append(
                create_dynamic_prompt(variation_index, wall_treatment, lighting)
            )
            variation_index += 1

    num_variations = len(prompts)
    print(f"Generating {num_variations} variations...")

    designer = InteriorDesigner()
    variations, output_dir = await designer.generate_variations(
        images=all_images,
        prompts=prompts,
        output_dir="outputs",
        num_variations=num_variations,
    )
    print(f"\n✅ Generated {len(variations)} variations in {output_dir}!")


if __name__ == "__main__":
    asyncio.run(main())
