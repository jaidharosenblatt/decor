#!/usr/bin/env python3
"""
Example usage of the Interior Designer
"""

from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

def example_basic_usage():
    """Example of basic usage without images"""
    print("🎨 Interior Designer - Basic Example")
    print("=" * 50)
    
    # Initialize designer
    designer = InteriorDesigner()
    
    # Define room specifications
    room_specs = RoomSpecs(
        width=14.0,
        length=18.0,
        height=9.0,
        window_count=3,
        door_count=2,
        room_type="living room"
    )
    
    # Define design prompt
    design_prompt = DesignPrompt(
        style="scandinavian",
        color_scheme="warm earth tones",
        mood="cozy and inviting",
        furniture_requirements=[
            "comfortable sectional sofa",
            "wooden coffee table",
            "floor lamp",
            "area rug",
            "accent chair",
            "bookshelf"
        ],
        additional_notes="Include lots of natural light, plants, and warm textures."
    )
    
    print(f"Room: {room_specs.room_type} ({room_specs.width}' x {room_specs.length}' x {room_specs.height}')")
    print(f"Style: {design_prompt.style}")
    print(f"Colors: {design_prompt.color_scheme}")
    print(f"Mood: {design_prompt.mood}")
    print(f"Furniture: {', '.join(design_prompt.furniture_requirements)}")
    print()
    
    # Generate 4 variations (smaller number for demo)
    print("Generating 4 design variations...")
    variations = designer.generate_design_variations(
        current_room_paths=[],  # No current room images
        inspiration_paths=[],   # No inspiration images
        room_specs=room_specs,
        design_prompt=design_prompt,
        num_variations=4
    )
    
    # Save grid
    designer.save_variations_grid(variations, "example_variations.png")
    
    print(f"\n✅ Generated {len(variations)} variations!")
    print("Check 'example_variations.png' for the grid overview")

if __name__ == "__main__":
    example_basic_usage() 