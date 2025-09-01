#!/usr/bin/env python3
"""
CLI interface for the Interior Designer
"""

import argparse
import sys
from pathlib import Path
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate interior design variations using Google Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with room specs
  python cli.py --width 16 --length 20 --height 9 --windows 2 --doors 1

  # With current room images
  python cli.py --width 16 --length 20 --current-room-images room1.jpg room2.jpg

  # With inspiration images
  python cli.py --width 16 --length 20 --inspiration-images insp1.jpg insp2.jpg

  # Custom style and requirements
  python cli.py --width 16 --length 20 --style "modern minimalist" --colors "neutral grays" --furniture "sofa,coffee table,TV stand"
        """
    )
    
    # Room specifications
    parser.add_argument("--width", type=float, required=True, help="Room width in feet")
    parser.add_argument("--length", type=float, required=True, help="Room length in feet")
    parser.add_argument("--height", type=float, default=9.0, help="Room height in feet (default: 9.0)")
    parser.add_argument("--windows", type=int, default=2, help="Number of windows (default: 2)")
    parser.add_argument("--doors", type=int, default=1, help="Number of doors (default: 1)")
    parser.add_argument("--room-type", default="living room", help="Type of room (default: living room)")
    
    # Design specifications
    parser.add_argument("--style", default="modern minimalist", help="Design style (default: modern minimalist)")
    parser.add_argument("--colors", default="neutral grays and whites", help="Color scheme (default: neutral grays and whites)")
    parser.add_argument("--mood", default="relaxing and peaceful", help="Room mood (default: relaxing and peaceful)")
    parser.add_argument("--furniture", nargs="+", default=["comfortable sofa", "coffee table", "entertainment center"], 
                       help="Required furniture items")
    parser.add_argument("--notes", default="", help="Additional design notes")
    
    # Images
    parser.add_argument("--current-room-images", nargs="+", default=[], 
                       help="Paths to current room images")
    parser.add_argument("--inspiration-images", nargs="+", default=[], 
                       help="Paths to inspiration images")
    
    # Output
    parser.add_argument("--variations", type=int, default=8, 
                       help="Number of variations to generate (default: 8)")
    parser.add_argument("--output-dir", default=".", 
                       help="Output directory for generated images (default: current directory)")
    
    return parser.parse_args()

def validate_image_paths(image_paths):
    """Validate that image files exist"""
    valid_paths = []
    for path in image_paths:
        if Path(path).exists():
            valid_paths.append(path)
        else:
            print(f"Warning: Image file not found: {path}")
    return valid_paths

def main():
    """Main CLI function"""
    args = parse_arguments()
    
    # Validate image paths
    current_room_paths = validate_image_paths(args.current_room_images)
    inspiration_paths = validate_image_paths(args.inspiration_images)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize designer
        designer = InteriorDesigner()
        
        # Create room specifications
        room_specs = RoomSpecs(
            width=args.width,
            length=args.length,
            height=args.height,
            window_count=args.windows,
            door_count=args.doors,
            room_type=args.room_type
        )
        
        # Create design prompt
        design_prompt = DesignPrompt(
            style=args.style,
            color_scheme=args.colors,
            mood=args.mood,
            furniture_requirements=args.furniture,
            additional_notes=args.notes
        )
        
        print(f"Generating {args.variations} design variations for a {room_specs.room_type}...")
        print(f"Room dimensions: {room_specs.width}' x {room_specs.length}' x {room_specs.height}'")
        print(f"Style: {design_prompt.style}")
        print(f"Color scheme: {design_prompt.color_scheme}")
        print(f"Mood: {design_prompt.mood}")
        print(f"Furniture: {', '.join(design_prompt.furniture_requirements)}")
        
        if current_room_paths:
            print(f"Current room images: {len(current_room_paths)}")
        if inspiration_paths:
            print(f"Inspiration images: {len(inspiration_paths)}")
        
        # Generate variations
        variations = designer.generate_design_variations(
            current_room_paths=current_room_paths,
            inspiration_paths=inspiration_paths,
            room_specs=room_specs,
            design_prompt=design_prompt,
            num_variations=args.variations
        )
        
        # Save grid
        grid_path = output_dir / "all_variations.png"
        designer.save_variations_grid(variations, str(grid_path))
        
        print(f"\n✅ Successfully generated {len(variations)} design variations!")
        print(f"Individual images saved in: {output_dir}")
        print(f"Grid overview saved as: {grid_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 