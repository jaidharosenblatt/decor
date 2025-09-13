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
CRITICAL WALL PAINTING AND LIGHTING:
- ACCENT WALL (entire fireplace wall extending to staircase):
  * Fireplace center section: Direct light = BRIGHT accent color
  * Staircase section: Less light = DARKER version of same accent color
  * Must be continuous with NO sharp cutoff between sections
  * Fireplace bump-out same color as surrounding accent (no white stripe)
- ALL OTHER WALLS: Must remain BRIGHT WHITE
  * Sliding door wall: WHITE
  * Entry wall: WHITE
  * Any other walls: WHITE
- Use exact paint colors from reference image with proper lighting variation

"""

# FINALISTS — unified color across fireplace bump-out and flanking planes.
WALL_TREATMENT_PRESETS = [
    "Use the 1st color swatch (leftmost warm beige) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 2nd color swatch (medium warm tan) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 3rd color swatch (warm beige) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 4th color swatch (terracotta/rust) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "Use the 5th color swatch (sage green) from the paint colors image"
    + ACCENT_WALL_INSTRUCTIONS,
    "All walls must be white",
]

HARD_CONSTRAINTS = """
HARD CONSTRAINTS (MUST FOLLOW):
- Must not block stairs, stair rail, or stair opening.
- Leave vent left of fireplace visible.
- Maintain at least 36" walkway from stairs to sliding door.
- Keep all furniture at least 8" clear of sliding door track.
- Left bay furniture depth must be ≤9.75"; right side furniture ≤18".
"""

CRITICAL_DO_NOT_INSTRUCTIONS = """
WALL COLOR MISTAKES TO AVOID:
- DO NOT: Make accent colors pale, washed out, or barely visible
- DO NOT: Paint the sliding door wall with accent color (must stay WHITE)
- DO NOT: Paint the entry wall with accent color (must stay WHITE)
- DO NOT: Leave white stripes on the fireplace bump-out
- DO NOT: Create breaks or gaps in accent wall color continuity
- DO NOT: Paint walls that should be white with accent color

ROOM LAYOUT MISTAKES TO AVOID:
- Do not place TV above fireplace (projector only)
- Do not move, add, or remove windows, doors, or fireplace
- Do not block or cover stair sconce
- Do not cover sliding door
- Do not block or cover vent left of fireplace
- Do not block the entrance to the staircase

STYLE MISTAKES TO AVOID:
- Do not use glossy paint, high contrast gallery walls, or heavy clutter
"""


CAMERA_PROMPT = """
CAMERA VIEWPOINT:
- View from seating area toward fireplace wall.
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

    CRITICAL REQUIREMENTS:
    - Use the current room images as a reference for the layout of the room. DO NOT ALTER THE LAYOUT.
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.

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

    WALL COLORING - CRITICAL INSTRUCTIONS:

    ACCENT WALL (MUST BE BOLD AND SATURATED):
    - Paint the ENTIRE back wall from left bookshelf area through fireplace to staircase
    - This includes: left bay area + fireplace center + fireplace bump-out + right bay area + staircase wall
    - Use RICH, BOLD, SATURATED color - NOT pale or washed out
    - Fireplace bump-out MUST be same color as surrounding accent wall (no white stripe)
    - Color should be CONTINUOUS across all sections with no breaks

    WHITE WALLS (MUST REMAIN BRIGHT WHITE):
    - Sliding door wall (left side of room)
    - Entry wall (right side of room)
    - All other walls that are NOT the fireplace/back wall

    Furniture and Decor:
    - Use traditional red/burgundy ornate rug from reference image
    - Six Floating shelves in left bay filled with green plants and books
    - Short hutch with round mirror in right bay
   
    PHOTO BEHAVIOR:
    - Do not show the projector screen; keep it retracted.
    - No flash. Use naturalistic interior lighting and accurate exposure.

    FURNITURE PLACEMENT:
    - Keep furniture within depth limits (left ≤9.75in, right ≤18in)

    {CRITICAL_DO_NOT_INSTRUCTIONS}
    {CAMERA_PROMPT}

    DESIGN INTENT:
    - Quiet, modern, and elevated. Subtle detail over bold patterns.
    - Prioritize negative space. Avoid visual heaviness.

    MUST PRESERVE:
    - Existing floors, openings, fireplace, window and door positions.
    - Vent left of fireplace remains visible.

    FINAL VERIFICATION CHECKLIST:
    1. ACCENT WALL: Entire back wall (left bay + fireplace + right bay + staircase) is BOLD and SATURATED with chosen color
    2. WHITE WALLS: Sliding door wall and entry wall are BRIGHT WHITE
    3. CONTINUITY: No breaks, gaps, or white stripes in accent wall color
    4. RUG: Traditional red/burgundy ornate rug is used
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
