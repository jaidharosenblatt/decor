#!/usr/bin/env python3
"""
Interior Designer - Generate living room design variations using Google Gemini API
"""

import os
import base64
import json
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from io import BytesIO

import google.genai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class RoomSpecs:
    """Room specifications and measurements"""
    width: float
    length: float
    height: float
    window_count: int
    door_count: int
    room_type: str = "living room"
    
    def to_prompt(self) -> str:
        """Convert room specs to a descriptive prompt"""
        return f"A {self.room_type} with dimensions {self.width}' x {self.length}' x {self.height}' high, featuring {self.window_count} windows and {self.door_count} doors."

@dataclass
class DesignPrompt:
    """Design prompt with style and requirements"""
    style: str
    color_scheme: str
    mood: str
    furniture_requirements: List[str]
    additional_notes: str = ""
    
    def to_prompt(self) -> str:
        """Convert design prompt to a descriptive string"""
        furniture_str = ", ".join(self.furniture_requirements)
        return f"Design in {self.style} style with {self.color_scheme} color scheme, {self.mood} mood. Include: {furniture_str}. {self.additional_notes}"

class InteriorDesigner:
    """Main class for generating interior design variations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the designer with Gemini API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini client
        genai.configure(api_key=self.api_key)
        self.model = "gemini-2.5-flash-image-preview"
        
        # Style variations for generating diverse designs
        self.style_variations = [
            "modern minimalist", "cozy bohemian", "scandinavian", "industrial chic",
            "traditional elegant", "mid-century modern", "coastal", "rustic farmhouse",
            "contemporary luxury", "eclectic", "zen minimalism", "art deco",
            "vintage industrial", "tropical modern", "nordic hygge", "mediterranean"
        ]
        
        self.color_variations = [
            "neutral grays and whites", "warm earth tones", "cool blues and greens",
            "bold jewel tones", "soft pastels", "monochromatic", "complementary colors",
            "analogous color scheme", "high contrast black and white", "warm neutrals"
        ]
        
        self.mood_variations = [
            "relaxing and peaceful", "energetic and vibrant", "sophisticated and elegant",
            "cozy and inviting", "bright and airy", "dramatic and bold", "serene and calm",
            "warm and welcoming", "modern and sleek", "romantic and intimate"
        ]
    
    def load_image(self, image_path: str) -> Image.Image:
        """Load and validate an image"""
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image {image_path}: {e}")
    
    def encode_image(self, image: Image.Image) -> str:
        """Convert PIL image to base64 string"""
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def create_variation_prompt(self, base_prompt: str, room_specs: RoomSpecs, 
                              design_prompt: DesignPrompt, variation_index: int) -> str:
        """Create a unique prompt for each variation"""
        # Add random variations to create diversity
        style = random.choice(self.style_variations) if variation_index > 0 else design_prompt.style
        colors = random.choice(self.color_variations) if variation_index > 0 else design_prompt.color_scheme
        mood = random.choice(self.mood_variations) if variation_index > 0 else design_prompt.mood
        
        # Add specific variation elements
        variation_elements = [
            "with natural light streaming through large windows",
            "featuring a statement lighting fixture",
            "with an accent wall",
            "incorporating indoor plants and greenery",
            "with a fireplace as the focal point",
            "featuring built-in storage solutions",
            "with a reading nook",
            "incorporating artwork and decorative elements",
            "with a home office area",
            "featuring a media center",
            "with a dining area",
            "incorporating vintage pieces",
            "with smart home technology integration",
            "featuring sustainable materials",
            "with a bar cart or beverage station",
            "incorporating seasonal decor elements"
        ]
        
        variation_element = random.choice(variation_elements) if variation_index > 0 else ""
        
        prompt = f"""
Create a photorealistic interior design rendering of a {room_specs.to_prompt()}

Design Requirements:
- Style: {style}
- Color Scheme: {colors}
- Mood: {mood}
- Must include: {', '.join(design_prompt.furniture_requirements)}
{variation_element}

Additional Notes: {design_prompt.additional_notes}

Generate a high-quality, detailed interior design visualization that shows:
1. Proper furniture placement and scale
2. Accurate lighting and shadows
3. Textures and materials
4. Decorative elements and accessories
5. Realistic perspective and depth

Make this variation {variation_index + 1} of {len(self.style_variations)} with a unique and distinctive character.
"""
        return prompt.strip()
    
    def generate_design_variation(self, current_room_images: List[Image.Image], 
                                inspiration_images: List[Image.Image],
                                room_specs: RoomSpecs, 
                                design_prompt: DesignPrompt,
                                variation_index: int) -> Optional[Image.Image]:
        """Generate a single design variation"""
        try:
            # Create the prompt for this variation
            prompt = self.create_variation_prompt(
                "", room_specs, design_prompt, variation_index
            )
            
            # Prepare content with images and text
            contents = [prompt]
            
            # Add current room images (up to 3)
            for i, img in enumerate(current_room_images[:3]):
                contents.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": self.encode_image(img)
                    }
                })
            
            # Add inspiration images (up to 2)
            for i, img in enumerate(inspiration_images[:2]):
                contents.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": self.encode_image(img)
                    }
                })
            
            # Generate content using Gemini
            response = genai.generate_content(
                model=self.model,
                contents=contents
            )
            
            # Extract generated image
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = base64.b64decode(part.inline_data.data)
                    return Image.open(BytesIO(image_data))
            
            print(f"Warning: No image generated for variation {variation_index + 1}")
            return None
            
        except Exception as e:
            print(f"Error generating variation {variation_index + 1}: {e}")
            return None
    
    def generate_design_variations(self, 
                                 current_room_paths: List[str],
                                 inspiration_paths: List[str],
                                 room_specs: RoomSpecs,
                                 design_prompt: DesignPrompt,
                                 num_variations: int = 8) -> List[Image.Image]:
        """Generate multiple design variations"""
        print(f"Generating {num_variations} design variations...")
        
        # Load images
        current_room_images = [self.load_image(path) for path in current_room_paths]
        inspiration_images = [self.load_image(path) for path in inspiration_paths]
        
        generated_images = []
        
        for i in range(num_variations):
            print(f"Generating variation {i + 1}/{num_variations}...")
            
            image = self.generate_design_variation(
                current_room_images, inspiration_images, room_specs, design_prompt, i
            )
            
            if image:
                generated_images.append(image)
                # Save each variation as it's generated
                output_path = f"design_variation_{i + 1:02d}.png"
                image.save(output_path)
                print(f"Saved {output_path}")
            else:
                print(f"Failed to generate variation {i + 1}")
        
        return generated_images
    
    def save_variations_grid(self, images: List[Image.Image], output_path: str = "all_variations.png"):
        """Save all variations in a grid layout"""
        if not images:
            print("No images to save")
            return
        
        # Calculate grid dimensions
        cols = min(4, len(images))
        rows = (len(images) + cols - 1) // cols
        
        # Get dimensions of first image
        img_width, img_height = images[0].size
        
        # Create grid image
        grid_width = cols * img_width
        grid_height = rows * img_height
        grid_image = Image.new('RGB', (grid_width, grid_height), 'white')
        
        # Paste images into grid
        for i, img in enumerate(images):
            row = i // cols
            col = i % cols
            x = col * img_width
            y = row * img_height
            grid_image.paste(img, (x, y))
        
        grid_image.save(output_path)
        print(f"Saved grid of all variations to {output_path}")

def main():
    """Main function to run the interior designer"""
    # Example usage
    designer = InteriorDesigner()
    
    # Room specifications
    room_specs = RoomSpecs(
        width=16.0,
        length=20.0,
        height=9.0,
        window_count=2,
        door_count=1,
        room_type="living room"
    )
    
    # Design prompt
    design_prompt = DesignPrompt(
        style="modern minimalist",
        color_scheme="neutral grays and whites",
        mood="relaxing and peaceful",
        furniture_requirements=[
            "comfortable sofa seating for 4-6 people",
            "coffee table",
            "entertainment center with TV",
            "accent chair",
            "floor lamp",
            "area rug"
        ],
        additional_notes="Focus on natural light and open space. Include some greenery."
    )
    
    # Example file paths (you'll need to provide actual paths)
    current_room_paths = [
        # "path/to/current_room_1.jpg",
        # "path/to/current_room_2.jpg"
    ]
    
    inspiration_paths = [
        # "path/to/inspiration_1.jpg",
        # "path/to/inspiration_2.jpg"
    ]
    
    # Generate variations
    variations = designer.generate_design_variations(
        current_room_paths=current_room_paths,
        inspiration_paths=inspiration_paths,
        room_specs=room_specs,
        design_prompt=design_prompt,
        num_variations=8
    )
    
    # Save grid
    designer.save_variations_grid(variations)

if __name__ == "__main__":
    main() 