#!/usr/bin/env python3
import glob
import asyncio
from interior_designer import InteriorDesigner


DINING_ROOM_VARIANTS = [
    "round walnut pedestal dining table with cream upholstered mid-century chairs – classic board and batten wainscoting painted white, sideboard in matching walnut against left wall with abstract artwork above, round jute rug grounding the space for cohesion with living room textures",

    "rectangular trestle dining table in rustic oak with ladder-back chairs – shaker-style vertical panel wainscoting in soft white, black metal linear chandelier overhead, sideboard with fluted doors on right wall holding plants and pottery, tying to living room shelving greenery",

    "square modern dining table in dark espresso with four upholstered chairs in warm gray – beadboard wainscoting full-height painted muted sage, oversized black-and-white framed art above, tall corner olive tree softening the window wall and echoing living room greenery",

    "oval tulip-base dining table with light oak top and white pedestal – picture frame molding wainscoting in white, statement pendant light cluster above, wall-mounted gallery of geometric prints to tie to modern living room shelves and round mirror for visual rhythm",

    "extendable rectangular walnut dining table with six low-profile upholstered chairs – raised panel wainscoting in bright white, deep navy paint above, long sideboard on left wall with brass accents, leaning floor mirror on right wall to echo living room round mirror and expand light",

    "glass-top rectangular dining table with warm wood legs and six upholstered dining chairs – flat panel modern wainscoting, wall painted warm greige to match living room fireplace wall, floating shelves mounted above buffet with ceramics and books for a seamless continuation",

    "round marble-top dining table with walnut base and four beige upholstered chairs – two-tone board and batten wainscoting with white below and soft terracotta above, single oversized art canvas hung above, tall mid-century floor lamp in corner mirroring living room tripod lamp",

    "rectangular dining table in natural ash with bench seating along window side and spindle-back chairs opposite – geometric box grid wainscoting in white, wall sconces flanking abstract art, built-in shelves on left wall for books and pottery continuing living room’s open shelving aesthetic",

    "round pedestal dining table in espresso wood with boucle upholstered chairs – half-wall horizontal tongue-and-groove wainscoting capped with ledge, artwork leaned casually above the ledge, ceramic plates on adjacent wall echoing living room’s mix of art and organic décor",

    "long rectangular dining table in walnut with six sleek mid-century chairs – three-quarter height shaker wainscoting painted soft gray, modern LED strip accent lighting embedded into right wall framing artwork, creating cohesion with the track lighting aesthetic of the living room"
]



def create_dynamic_prompt(variation_index: int, variation_description: str) -> str:
    """Create a deterministic prompt with controlled diversity per iteration."""

  
    additional_notes = f"""
    CRITICAL REQUIREMENTS:
    - Use the exact room geometry and the measurements listed below. Do not alter architecture.
    - Same focal length and vantage as source. No wide angle exaggeration.
    - Change the color of the walls to be entirely white. Do NOT use the current green walls.

    EXACT ROOM DIMENSIONS:
    - 122 in back wall window 
    - 108 in wall parallel with kitchen, opposite from door
    - 72in wall next to door

    {variation_description}


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
    
    for variation_description in DINING_ROOM_VARIANTS:
        print(f"Variation {variation_index}: {variation_description[:50]}...")
        prompts.append(create_dynamic_prompt(variation_index, variation_description))
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
