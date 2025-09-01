#!/usr/bin/env python3
"""
Jaidha's Living Room Designer - Simple Script
"""

import glob
import asyncio
from datetime import datetime
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

async def main():
    """Generate design variations for Jaidha's living room"""
    print("🎨 Jaidha's Living Room Designer")
    print("=" * 50)
    
    # Initialize designer
    designer = InteriorDesigner()
    
    # Room specs
    room_specs = RoomSpecs(
        width=14.0,  # Sliding glass wall: 168" = 14'
        length=8.83,  # Back sofa wall: 106" = 8.83'
        height=9.0,   # 107" = 8.92'
        room_type="living room"
    )
    
    # Design prompt
    design_prompt = DesignPrompt(
        style="mid-century modern",
        color_scheme="warm leathers and wood with cool neutrals",
        mood="curated comfort with light and contrast play",
        furniture_requirements=[
            "existing grey leather couch (MUST KEEP - do not change)",
            "existing floors (MUST KEEP - do not change)",
            "grey couch MUST face the projector at the top of the room",
            "walnut wood coffee table",
            "mid-century accent chairs with wooden arms",
            "geometric area rug (vary type and pattern)",
            "built-in shelving with styled objects and art (not cluttered)",
            "natural woven textures",
            "brass framed mirror",
            "floor lamp",
            "natural materials (wood, woven, linen, wool)",
            "wall-mounted elements (vary: plants, artwork, shelves, lighting)"
        ],
        additional_notes="""
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
        
        ROOM LAYOUT - CRITICAL:
        - Top part of room has a PROJECTOR - grey couch MUST face this projector
        - Grey leather couch positioning is FIXED - do not change its location or orientation
        - Couch must be positioned to view the projector screen
        - Camera/viewpoint should show the BACK of the grey couch facing the projector
        - We should see the back of the couch in the foreground, with the projector area in the background
        
        DO NOT CHANGE ANY ROOM DIMENSIONS OR PROPORTIONS
        Keep the room exactly the same size and shape
        Maintain all existing architectural features and proportions
        
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
        
        WALL COLOR VARIATIONS:
        - White walls (clean backdrop)
        - Warm off-white/cream walls
        - Light gray walls
        - Soft beige walls
        - Light blue-gray walls
        - Warm taupe walls
        
        RUG TYPE VARIATIONS:
        - Geometric mid-century modern rugs
        - Natural woven jute/sisal rugs
        - Persian/Oriental style rugs
        - Abstract contemporary rugs
        - Vintage kilim rugs
        - Minimalist solid color rugs
        
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
    )
    
    # Get current room images
    current_room_paths = glob.glob("current/*")
    print(f"Found {len(current_room_paths)} current room images")
    
    # Generate variations
    variations, output_dir = await designer.generate_variations(
        current_room_paths=current_room_paths,
        room_specs=room_specs,
        design_prompt=design_prompt,
        num_variations=3
    )
    
    # Save grid
    if variations:
        grid_path = f"{output_dir}/jaidha_living_room_variations.png"
        designer.save_grid(variations, grid_path)
    
    print(f"\n✅ Generated {len(variations)} variations!")

if __name__ == "__main__":
    asyncio.run(main()) 