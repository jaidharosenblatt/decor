#!/usr/bin/env python3
"""
Tailored Interior Designer for Jaidha's Living Room
"""

import os
import glob
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

def jaidha_living_room():
    """Generate design variations for Jaidha's specific living room"""
    print("🎨 Interior Designer - Jaidha's Living Room")
    print("=" * 60)
    
    # Initialize designer
    designer = InteriorDesigner()
    
    # Jaidha's specific room measurements (converted to feet)
    room_specs = RoomSpecs(
        width=14.0,  # Approximate width based on sliding glass wall
        length=12.0,  # Approximate length based on back wall
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
            "existing leather couch from items folder (must keep)",
            "existing floors (must remain unchanged)",
            "walnut wood coffee table",
            "mid-century accent chairs with wooden arms",
            "geometric area rug",
            "built-in shelving with styled objects and art",
            "natural woven textures",
            "brass framed mirror",
            "floor lamp",
            "natural materials (wood, woven, linen, wool)"
        ],
        additional_notes="""
        Design Requirements:
        - MUST KEEP: Existing leather couch and current floors (do not change these)
        - Mix warm leathers/wood (tan chairs, walnut cabinets) with cool neutrals (grey elements, white walls)
        - Clean lines and low-slung furniture
        - Curated shelving with objects/art (styled but not cluttered)
        - Rugs that ground the space and add warmth
        - White walls + dark floors = bold backdrop (walls can change color)
        - Break up with warm wood cabinetry, built-ins, or furniture
        - Transitional balance between modern and classic elements
        - Natural light from large sliding glass wall
        - Incorporate existing couch and maintain its placement
        - All other furniture, wall colors, and decor can be changed
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
    
    # Generate 1 variation as requested
    print("Generating 1 design variation for your living room...")
    
    # Start with just text prompt to test API
    variations = designer.generate_design_variations(
        current_room_paths=[],  # Start with no images to test
        inspiration_paths=[],   # Start with no images to test
        room_specs=room_specs,
        design_prompt=design_prompt,
        num_variations=1
    )
    
    # Save grid
    designer.save_variations_grid(variations, "jaidha_living_room_variations.png")
    
    print(f"\n✅ Generated {len(variations)} variations!")
    print("Check 'jaidha_living_room_variations.png' for the overview")
    print("Individual files: design_variation_01.png")

if __name__ == "__main__":
    jaidha_living_room() 