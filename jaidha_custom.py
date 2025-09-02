#!/usr/bin/env python3
import glob
import asyncio
from interior_designer import InteriorDesigner

# Tightened palettes and presets
FURNITURE_WOOD_TONES = [
    "mid walnut wood - neutral brown - matte finish",
    "light oak warm - matte finish",
]


# Lighting / time-of-day scenes
LIGHTING_PRESETS = [
    """TIME OF DAY: Daytime (soft overcast).
    Primary light source is daylight; windows are bright but not blown out.
    Track lights 10%, floor lamp OFF. White balance ~4500K.
    Exposure naturalistic for interiors; colors remain true.""",
]

ACCENT_WALL_INSTRUCTIONS = """
accent wall color that must EXTEND FULLY into the staircase wall plane (no sharp cutoff). Fireplace bump-out must be the SAME COLOR as the surrounding accent (no white stripe).
Do not paint the right wall 

"""

# FINALISTS — unified color across fireplace bump-out and flanking planes.
WALL_TREATMENT_PRESETS = [
    "beige (brown and not gray)" + ACCENT_WALL_INSTRUCTIONS,
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

def create_dynamic_prompt(variation_index: int, wall_treatment: str, lighting: str) -> str:
    """Create a deterministic prompt with controlled diversity per iteration."""

    additional_notes = f"""
    CRITICAL REQUIREMENTS:
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.
    - Keep existing couch facing the projector.

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

    Rug:
    Mid century modern rug

    On the left wall, a tall thin mid century modern lamp sits right next to the sliding door.

    Couch:
    - existing grey leather couch facing the projector all the way back of the wall. the back half of the couch should be off of the rug.

    Fireplace wall:
    Left bay (left of fireplace):
    2 side by side bookshelves (use bookshelf.png) image twice. They are 75in H X 26in W X 15in D each. so in total they are 75 in (70% of the wall) and 52in (2 inch on each side)
    
    Right bay (right of fireplace):
    Short hutch with a round mirror hung above it on the wall

    Accent chair:
     brown leather accent chair placed to the right of the couch on the rug facing the sliding door
   
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
    print("🎨 Jaidha's Living Room Designer — Testing Completely Dark")
    print("=" * 50)
    current_room_paths = glob.glob("current/*")
    items = glob.glob("items/*")
    print(f"Found {len(current_room_paths)} current room images")
    print(f"Found {len(items)} items images")
    # Generate variations using nested loops
    prompts = []
    variation_index = 0
    
    for wall_treatment in WALL_TREATMENT_PRESETS:
        for lighting in LIGHTING_PRESETS:
            print(f"Variation {variation_index}: Wall treatment: {wall_treatment[:50]}..., Lighting: {lighting[:50]}...")
            prompts.append(create_dynamic_prompt(variation_index, wall_treatment, lighting))
            variation_index += 1

    num_variations = len(prompts)
    print(f"Generating {num_variations} variations...")

    designer = InteriorDesigner()
    variations, output_dir = await designer.generate_variations(
        current_room_paths=current_room_paths,
        num_variations=num_variations,
        prompts=prompts,
        items=items
    )
    print(f"\n✅ Generated {len(variations)} variations!")

if __name__ == "__main__":
    asyncio.run(main())
