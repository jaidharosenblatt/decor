#!/usr/bin/env python3
"""
Tailored Interior Designer for Jaidha's Living Room
"""

import os
import glob
import asyncio
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

async def jaidha_living_room():
    """Generate design variations for Jaidha's specific living room"""
    print("🎨 Interior Designer - Jaidha's Living Room")
    print("=" * 60)
    
    # Initialize designer
    designer = InteriorDesigner()
    
    # Jaidha's specific room measurements (converted to feet)
    room_specs = RoomSpecs(
        width=14.0,  # Sliding glass wall: 168" = 14'
        length=8.83,  # Back sofa wall: 106" = 8.83'
        height=9.0,   # Rounded from 107" = 8.92'
        window_count=1,  # Large sliding glass wall
        door_count=1,    # Assuming one main entry
        room_type="living room"
    )
    
    # Jaidha's specific design preferences
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
    
    # Get all images using glob
    current_room_paths = glob.glob("current/*")
    items_paths = glob.glob("items/*")
    inspiration_paths = glob.glob("inspo/*")
    
    print(f"Room: {room_specs.room_type}")
    print(f"Dimensions: {room_specs.width}' x {room_specs.length}' x {room_specs.height}'")
    print(f"Style: {design_prompt.style}")
    print(f"Colors: {design_prompt.color_scheme}")
    print(f"Mood: {design_prompt.mood}")
    print(f"Current room images: {len(current_room_paths)}")
    print(f"Items images: {len(items_paths)}")
    print(f"Inspiration images: {len(inspiration_paths)}")
    print()
    
    # Generate multiple variations focusing on wall furniture
    print("Generating 3 design variations focusing on wall furniture...")
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Use single image approach - just one current room photo
    single_image = current_room_paths[0] if current_room_paths else None
    
    variations = await designer.generate_design_variations(
        current_room_paths=[single_image] if single_image else [],  # Single image only
        inspiration_paths=[],  # No inspiration images for now
        room_specs=room_specs,
        design_prompt=design_prompt,
        num_variations=3  # Generate 3 variations
    )
    
    # Save grid to output directory
    grid_path = os.path.join(output_dir, "jaidha_living_room_variations.png")
    designer.save_variations_grid(variations, grid_path)
    
    print(f"\n✅ Generated {len(variations)} variations!")
    print(f"Check '{output_dir}/jaidha_living_room_variations.png' for the overview")
    print(f"Individual files: {output_dir}/design_variation_01.png, {output_dir}/design_variation_02.png, {output_dir}/design_variation_03.png")

if __name__ == "__main__":
    asyncio.run(jaidha_living_room()) 