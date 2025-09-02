#!/usr/bin/env python3
import glob
import asyncio
from interior_designer import InteriorDesigner


WALL_TREATMENT_PRESETS = [
    "classic board and batten wainscoting – tall rectangular battens evenly spaced, painted white, framed artwork hung above in a neat row",
    "shaker-style vertical panel wainscoting – wide flat vertical planks with clean lines, semi-gloss finish",
    "beadboard wainscoting – narrow vertical grooves running full height of panel, cottage-inspired, single large art piece centered above",
    "picture frame molding wainscoting – rectangular boxes with subtle trim stacked across the wall",
    "raised panel wainscoting – traditional square panels with beveled molding, slightly more formal, complemented by a gallery wall of small prints above",
    "flat panel modern wainscoting – sleek flush panels with minimal trim, contemporary look",
    "two-tone board and batten – lower half white, upper wall painted accent color, oversized canvas artwork adding contrast above",
    "geometric box grid wainscoting – symmetrical square insets creating a modern checkerboard pattern",
    "half-wall tongue and groove planks – horizontal wood slats capped with a ledge for display, artwork casually leaned against wall above",
    "three-quarter height shaker wainscoting – taller installation reaching window sill height for drama, framed minimalist prints above"
]

DINING_ROOM_EXTRAS = [
    "slim sideboard in warm wood with artwork above – storage and display combined",
    "bar cabinet with fluted doors and a brass lamp on top – compact entertaining station",
    "floating shelves with stacked ceramics and cookbooks – casual and modern",
    "arched wall mirror with sconces on either side – adds depth and light",
    "gallery wall of black-and-white photography – structured but personal",
    "floor-to-ceiling built-in shelving with lower cabinets – functional and architectural",
    "olive tree in a textured planter placed in corner – natural height and greenery",
    "bench along one wall with upholstered cushion – extra seating and cozy feel",
    "plate wall with mismatched ceramics – artistic and collected look",
    "modern wall panel with integrated LED lighting – subtle glow and architectural interest"
]


DINING_TABLE_PRESETS = [
    "rounded pedestal dining table in medium walnut with 4 upholstered chairs – cozy, space-efficient",
    "rectangular farmhouse dining table in warm oak with 4 ladder-back chairs – rustic yet simple",
    "rectangular modern dining table in dark espresso with 4 upholstered chairs – clean lines, minimal look",
    "round tulip base dining table in light oak with 4 molded chairs – mid-century modern inspired",
    "rectangular trestle dining table in walnut with 4 cushioned side chairs – traditional and sturdy",
    "oval pedestal dining table in rich cherry with 4 high-back chairs – elegant and transitional",
    "square compact dining table in matte black with 4 fabric chairs – urban and contemporary",
    "rectangular glass-top dining table with 4 wood-frame chairs – airy, modern aesthetic",
    "round marble-top dining table with 4 upholstered chairs – refined and upscale",
    "extendable rectangular dining table in natural oak with 4 spindle-back chairs – versatile and casual"
]

def create_dynamic_prompt(variation_index: int, wall_treatment: str) -> str:
    """Create a deterministic prompt with controlled diversity per iteration."""

    def select(array:list[str]) -> str:

        return array[variation_index % len(array)]
    dining_table = select(DINING_TABLE_PRESETS)
    dining_room_extra = select(DINING_ROOM_EXTRAS)
    additional_notes = f"""
    CRITICAL REQUIREMENTS:
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.
    - Same focal length and vantage as source. No wide angle exaggeration.
    - Change the color of the walls to be entirely white. Do NOT use the current green walls.

    EXACT ROOM DIMENSIONS:
    - 122 in back wall window 
    - 108 in wall parallel with kitchen, opposite from door
    - 72in wall next to door

    WALL TREATMENT:

    {wall_treatment}

    FURNITURE:
    {dining_table}

    {dining_room_extra}

    PHOTO BEHAVIOR:
    - No flash. Use naturalistic interior lighting and accurate exposure.

    DESIGN INTENT:
    - Mid century modern, and elevated. Subtle detail over bold patterns.
    - Prioritize negative space. Avoid visual heaviness.

    NEVER
    - Make any structural changes to the kitchen.
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
        prompts.append(create_dynamic_prompt(variation_index, wall_treatment))
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
