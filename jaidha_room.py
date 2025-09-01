#!/usr/bin/env python3
"""
Jaidha's Living Room Designer - Simple Script
"""

import glob
import asyncio
import random
from datetime import datetime
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

# Random variation agents for more diversity
FURNITURE_COLORS = [
    "warm walnut wood",
    "rich mahogany wood", 
    "light oak wood",
    "dark espresso wood",
    "natural bamboo",
    "whitewashed wood",
    "black lacquered wood",
    "golden teak wood",
    "cherry wood",
    "ash wood",
    "maple wood",
    "birch wood"
]

WALL_TREATMENTS = [
    "white walls",
    "warm off-white/cream walls",
    "light gray walls", 
    "soft beige walls",
    "light blue-gray walls",
    "warm taupe walls",
    "white walls with one accent wall in deep navy blue",
    "white walls with one accent wall in emerald green",
    "white walls with one accent wall in warm terracotta",
    "white walls with one accent wall in charcoal gray",
    "white walls with one accent wall in sage green",
    "white walls with one accent wall in burgundy",
    "white walls with one accent wall in mustard yellow",
    "white walls with one accent wall in dusty rose"
]

RUG_STYLES = [
    "geometric mid-century modern rug",
    "natural woven jute/sisal rug",
    "Persian/Oriental style rug",
    "abstract contemporary rug",
    "vintage kilim rug",
    "minimalist solid color rug",
    "Indian style rug with traditional patterns",
    "Moroccan style rug with geometric designs",
    "Turkish style rug with floral motifs",
    "Scandinavian style rug with simple patterns",
    "Bohemian style rug with eclectic patterns",
    "Modern abstract rug with bold colors",
    "Traditional Indian dhurrie rug",
    "Persian Tabriz style rug",
    "Moroccan Beni Ourain style rug"
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
NEGATIVE PROMPTS (DO NOT DO):
- Do not place TV above fireplace (projector only).
- Do not move, add, or remove windows, doors, or fireplace.
- Do not block or cover stair sconce.
- Do not cover sliding door.
- Do not block or cover vent left of fireplace.
"""

CAMERA_PROMPT = """
CAMERA VIEWPOINT:
- Always show the back of the couch in the foreground.
- Fireplace wall must be centered in the background.
"""

def create_dynamic_prompt(variation_index: int) -> DesignPrompt:
    """Create a dynamic prompt with random variations for more diversity"""
    
    # Randomly select variations
    furniture_color = random.choice(FURNITURE_COLORS)
    wall_treatment = random.choice(WALL_TREATMENTS)
    rug_style = random.choice(RUG_STYLES)
    
    # Create variation-specific furniture requirements
    base_furniture = [
        "existing grey leather couch (MUST KEEP - do not change)",
        "existing floors (MUST KEEP - do not change)",
        "grey couch MUST face the projector at the top of the room"
    ]
    
    # Add random furniture variations
    furniture_variations = [
        f"{furniture_color} coffee table",
        f"{furniture_color} accent chairs with wooden arms",
        f"{furniture_color} side table",
        f"{furniture_color} bookshelf",
        f"{furniture_color} console table",
        f"{furniture_color} floor lamp base",
        f"{furniture_color} mirror frame"
    ]
    
    # Randomly select 3-4 furniture pieces
    selected_furniture = random.sample(furniture_variations, random.randint(3, 4))
    
    furniture_requirements = base_furniture + selected_furniture + [
        f"{rug_style}",
        "built-in shelving with styled objects and art (not cluttered)",
        "natural woven textures",
        "brass framed mirror",
        "floor lamp",
        "natural materials (wood, woven, linen, wool)",
        "wall-mounted elements (vary: plants, artwork, shelves, lighting)"
    ]
    
    # Create dynamic additional notes
    additional_notes = f"""
    CRITICAL REQUIREMENTS - MUST FOLLOW EXACTLY:
    
    EXACT ROOM DIMENSIONS (DO NOT MODIFY):
    Living room
    - Left side 55.5 in
    - Accent depth 9.75in
    - Right of fireplace: 55in to stair case, 38in to light
    - 107in tall
    - Left of sliding door 46.5in
    - Right of sliding door 46.5in
    - Back sofa wall 106in
    - 168in sliding glass wall
    
    {HARD_CONSTRAINTS}
    
    WALL TREATMENT - VARIATION {variation_index + 1}:
    {wall_treatment}
    
    FURNITURE COLOR - VARIATION {variation_index + 1}:
    Use {furniture_color} for wooden furniture pieces
    
    RUG STYLE - VARIATION {variation_index + 1}:
    {rug_style}
    
    {NEGATIVE_PROMPTS}
    
    {CAMERA_PROMPT}
    
    DESIGN STYLE - WARM + COOL BALANCE:
    - Mix warm leathers/wood (tan chairs, walnut cabinets, natural textures) with cool neutrals (grey couches, white walls)
    - This keeps the space from feeling cold or sterile
    
    MID-CENTURY MODERN INFLUENCE:
    - Clean lines, low-slung furniture
    - Accent chairs with wooden arms
    - Geometric rugs
    - Occasional retro vibes
    
    CURATED COMFORT:
    - Shelving with objects/art styled but not cluttered
    - Rugs that ground the space and add warmth without overpowering
    - Natural materials (wood, woven, linen, wool)
    
    LIGHT & CONTRAST PLAY:
    - White walls + dark floors = bold backdrop
    - Break this up with warm wood cabinetry, built-ins, or furniture
    
    MIX OF MODERN & CLASSIC:
    - Transitional balance — not one strict style
    - Some rooms lean modern (sleek fireplace, built-in shelving)
    - Others have hint of traditional (brass framed mirrors, patterned rugs)
    
    MUST PRESERVE EXACTLY:
    - Existing grey leather couch (do not change or replace)
    - Existing floors (do not change or replace)
    - Room dimensions and proportions (do not make room bigger or smaller)
    - All architectural features and room layout
    - Couch positioning facing projector
    
    HANDLE ASYMMETRY:
    - Room is asymmetrical - respect the uneven layout
    - Left side: 55.5 inches, Right side: different measurements
    - Sliding door sides: 46.5 inches each (symmetrical)
    - Fireplace area: 55 inches to staircase, 38 inches to light
    - Do not force symmetry - work with the natural asymmetrical layout
    - Furniture placement should respect the uneven room proportions
    - Wall treatments should balance the asymmetry without forcing perfect symmetry
    
    VARIATION FOCUS - WALL FURNITURE:
    Vary the furniture on the walls based on:
    - Material: wood, metal, glass, woven, ceramic
    - Furniture type: plants, side tables, lamps, bookshelves, artwork, mirrors, decorative objects
    - Style: mid-century modern, contemporary, vintage, eclectic
    - Color: warm woods, cool metals, natural textures, bold accents
    
    Generate a photorealistic interior design that shows proper furniture placement, accurate lighting, textures, and realistic perspective while maintaining the exact room dimensions and proportions.
    """
    
    return DesignPrompt(
        style="mid-century modern",
        color_scheme="warm leathers and wood with cool neutrals",
        mood="curated comfort with light and contrast play",
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
    num_variations = 10
    prompts = [create_dynamic_prompt(i) for i in range(num_variations)]
    variations, output_dir = await designer.generate_variations(
        current_room_paths=current_room_paths,
        room_specs=room_specs,
        design_prompt=None,  # We'll use the prompts list
        num_variations=num_variations,
        prompts=prompts
    )
    print(f"\n✅ Generated {len(variations)} variations!")

if __name__ == "__main__":
    asyncio.run(main()) 