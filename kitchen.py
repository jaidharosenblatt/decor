#!/usr/bin/env python3
import glob
import asyncio
from interior_designer import InteriorDesigner


WALL_TREATMENT_PRESETS = [
    "classic board and batten wainscoting – tall rectangular battens evenly spaced, painted white",
    "shaker-style vertical panel wainscoting – wide flat vertical planks with clean lines, semi-gloss finish",
    "beadboard wainscoting – narrow vertical grooves running full height of panel, cottage-inspired",
    "picture frame molding wainscoting – rectangular boxes with subtle trim stacked across the wall",
    "raised panel wainscoting – traditional square panels with beveled molding, slightly more formal",
    "flat panel modern wainscoting – sleek flush panels with minimal trim, contemporary look",
    "two-tone board and batten – lower half white, upper wall painted accent color, strong contrast",
    "geometric box grid wainscoting – symmetrical square insets creating a modern checkerboard pattern",
    "half-wall tongue and groove planks – horizontal wood slats capped with a ledge for display",
    "three-quarter height shaker wainscoting – taller installation reaching window sill height for drama"
]


def create_dynamic_prompt(wall_treatment: str) -> str:
    """Create a deterministic prompt with controlled diversity per iteration."""

    additional_notes = f"""
    CRITICAL REQUIREMENTS:
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.
    - Same focal length and vantage as source. No wide angle exaggeration.

    EXACT ROOM DIMENSIONS:
    - 122 in back wall window 
    - 108 in wall parallel with kitchen, opposite from door
    - 72in wall next to door

    WALL TREATMENT:
    {wall_treatment}

    FURNITURE:


    PHOTO BEHAVIOR:
    - No flash. Use naturalistic interior lighting and accurate exposure.

    MATERIAL AND COLOR RULES:
    - Walls: soft warm gray or off-white, matte (unless accent wall specified).

    DESIGN INTENT:
    - Quiet, modern, and elevated. Subtle detail over bold patterns.
    - Prioritize negative space. Avoid visual heaviness.
    """

    return additional_notes

async def main():
    print("🎨 Jaidha's Kitchen Designer")
    print("=" * 50)
    current_room_paths = glob.glob("source_images/kitchen/*")
    print(f"Found {len(current_room_paths)} current room images")

    # Generate variations using nested loops
    prompts = []
    variation_index = 0
    
    for wall_treatment in WALL_TREATMENT_PRESETS:
        print(f"Variation {variation_index}: Wall treatment: {wall_treatment[:50]}...")
        prompts.append(create_dynamic_prompt(wall_treatment))
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
