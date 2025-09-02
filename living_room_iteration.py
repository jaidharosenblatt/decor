#!/usr/bin/env python3
import glob
import asyncio
from interior_designer import InteriorDesigner

# Tightened palettes and presets
FURNITURE_WOOD_TONES = [
    "mid walnut wood - neutral brown - matte finish",
    "light oak warm - matte finish",
]

RUG_STYLES = [
    "Indian dhurrie rug in deep red with traditional patterns",
    "Indian dhurrie rug in forest green with geometric motifs",
    "Indian dhurrie rug in warm beige with subtle patterns",
    "natural woven jute rug - light sand",
    "subtle Persian style rug - faded warm neutrals",
    "minimal wool flatweave - light gray"
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
    "Warm terracotta " + ACCENT_WALL_INSTRUCTIONS,
    "Clay " + ACCENT_WALL_INSTRUCTIONS,
    "Deep olive green " + ACCENT_WALL_INSTRUCTIONS, 
    "Sage green " + ACCENT_WALL_INSTRUCTIONS,
    "Beige tan " + ACCENT_WALL_INSTRUCTIONS,
    "dusty light blue " + ACCENT_WALL_INSTRUCTIONS,
    "white"
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

    def select(array:list[str]) -> str:
        return array[variation_index % len(array)]
   
    furniture_color = select(FURNITURE_WOOD_TONES)

    left_side_furniture_options = [
        f"{furniture_color} floating shelves - depth <= 9.75in. Filled with mid century decor and minimalistic books",
        f"{furniture_color} console table - depth <= 9.75in with mirror on top"
    ] 


    right_side_furniture_options = [
        "brass tall framed rectangular mirror - max 36in height",
        "tall thin mid century modern lamp",
        "tall thin olive tree in mid century modern pot"
    ]

    accent_chair_options = [
        "brown leather accent chair",
        "green leather accent chair",
        "forrest green boucle accent chair",
        "velvet bronze accent chair"
    ]

    

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

    WALL TREATMENT - VARIATION {variation_index + 1}:
    {wall_treatment}

    LIGHTING & TIME OF DAY:
    {lighting}

    FURNITURE:

    Rug:
    {select(RUG_STYLES)}

    Couch:
    - existing grey leather couch facing the projector

    Fireplace wall:
    Left bay (left of fireplace):
    {select(left_side_furniture_options)}
    Right bay (right of fireplace):
    {select(right_side_furniture_options)}

    Accent chair:
    Placed to the right of the couch on the rug
    {select(accent_chair_options)}

    PHOTO BEHAVIOR:
    - Do not show the projector screen; keep it retracted.
    - No flash. Use naturalistic interior lighting and accurate exposure.

    FURNITURE PLACEMENT:
    - Keep furniture within depth limits (left ≤9.75in, right ≤18in)

    MATERIAL AND COLOR RULES:
    - Walls: soft warm gray or off-white, matte (unless accent wall specified).
    - Wood: {furniture_color}. Absolutely no red/orange wood.
    - Metals: small brass accents only.

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
    current_room_paths = glob.glob("living_room/*")
    print(f"Found {len(current_room_paths)} current room images")

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
        items=[]
    )
    print(f"\n✅ Generated {len(variations)} variations!")

if __name__ == "__main__":
    asyncio.run(main())
