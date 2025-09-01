#!/usr/bin/env python3
"""
Interior Designer - Generate living room design variations using Google Gemini API
"""

import os
import base64
import json
import random
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from io import BytesIO

from google import genai
from google.genai import types
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
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-image-preview"  # Image generation model
        
        # Style variations for generating diverse designs
        self.style_variations = [
            "mid-century modern", "modern minimalist", "transitional", "scandinavian", 
            "industrial chic", "traditional elegant", "cozy bohemian", "coastal", 
            "rustic farmhouse", "contemporary luxury", "eclectic", "zen minimalism", 
            "art deco", "vintage industrial", "tropical modern", "nordic hygge"
        ]
        
        self.color_variations = [
            "warm leathers and wood with cool neutrals", "neutral grays and whites", 
            "warm earth tones", "cool blues and greens", "bold jewel tones", 
            "soft pastels", "monochromatic", "complementary colors", 
            "analogous color scheme", "high contrast black and white"
        ]
        
        self.mood_variations = [
            "curated comfort with light and contrast play", "relaxing and peaceful", 
            "energetic and vibrant", "sophisticated and elegant", "cozy and inviting", 
            "bright and airy", "dramatic and bold", "serene and calm", 
            "warm and welcoming", "modern and sleek"
        ]
    
    def load_image(self, image_path: str) -> Image.Image:
        """Load and validate an image"""
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
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
    
    async def generate_design_variation(self, current_room_images: List[Image.Image], 
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
            
            # Prepare content with images and text - following official docs exactly
            contents = [prompt]
            
            # Add current room images (up to 3) - following the Python example format
            for i, img in enumerate(current_room_images[:3]):
                contents.append(img)
            
            # Add inspiration images (up to 2) - following the Python example format
            for i, img in enumerate(inspiration_images[:2]):
                contents.append(img)
            
            # Generate content using Gemini async - following official docs exactly
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=contents,
            )
            
            # Log usage information
            self.log_usage_info(response, variation_index + 1)
            
            # Extract generated image - following official docs exactly
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    print(f"Text response: {part.text}")
                elif part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    return image
            
            print(f"Warning: No image generated for variation {variation_index + 1}")
            return None
            
        except Exception as e:
            print(f"Error generating variation {variation_index + 1}: {e}")
            return None
    
    def log_usage_info(self, response, variation_num: int):
        """Log token usage and estimated cost for the API request"""
        try:
            if hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                print(f"\n💰 Usage for variation {variation_num}:")
                print(f"   Input tokens: {usage.prompt_token_count}")
                print(f"   Output tokens: {usage.candidates_token_count}")
                print(f"   Total tokens: {usage.total_token_count}")
                
                # Estimate cost (prices as of 2024, may vary)
                # gemini-2.5-flash-image-preview pricing:
                # Input: $0.000075 per 1K tokens
                # Output: $0.0003 per 1K tokens
                input_cost = (usage.prompt_token_count / 1000) * 0.000075
                output_cost = (usage.candidates_token_count / 1000) * 0.0003
                total_cost = input_cost + output_cost
                
                print(f"   Estimated cost: ${total_cost:.6f}")
                print(f"     - Input: ${input_cost:.6f}")
                print(f"     - Output: ${output_cost:.6f}")
                
            elif hasattr(response, 'usage'):
                # Alternative usage field
                usage = response.usage
                print(f"\n💰 Usage for variation {variation_num}:")
                print(f"   Total tokens: {usage.total_tokens}")
                print(f"   Estimated cost: ${(usage.total_tokens / 1000) * 0.000375:.6f}")
                
        except Exception as e:
            print(f"Could not log usage info: {e}")
    
    def get_total_usage_summary(self, total_tokens: int = 0):
        """Display total usage summary"""
        if total_tokens > 0:
            total_cost = (total_tokens / 1000) * 0.000375  # Average cost per 1K tokens
            print(f"\n📊 Total Usage Summary:")
            print(f"   Total tokens used: {total_tokens:,}")
            print(f"   Estimated total cost: ${total_cost:.6f}")
            print(f"   Cost per variation: ${total_cost / 3:.6f}")
    
    async def generate_design_variations(self, 
                                 current_room_paths: List[str],
                                 inspiration_paths: List[str],
                                 room_specs: RoomSpecs,
                                 design_prompt: DesignPrompt,
                                 num_variations: int = 8,
                                 output_dir: str = "output") -> List[Image.Image]:
        """Generate multiple design variations in parallel"""
        print(f"Generating {num_variations} design variations in parallel...")
        
        # Load images
        current_room_images = []
        for path in current_room_paths:
            try:
                img = self.load_image(path)
                current_room_images.append(img)
            except Exception as e:
                print(f"Warning: Could not load image {path}: {e}")
        
        inspiration_images = []
        for path in inspiration_paths:
            try:
                img = self.load_image(path)
                inspiration_images.append(img)
            except Exception as e:
                print(f"Warning: Could not load image {path}: {e}")
        
        # Create tasks for parallel execution with response tracking
        async def generate_with_usage(i):
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=[self.create_variation_prompt("", room_specs, design_prompt, i)] + 
                        current_room_images[:3] + inspiration_images[:2]
            )
            return i, response
        
        tasks = [generate_with_usage(i) for i in range(num_variations)]
        
        # Execute all tasks in parallel
        print("Starting parallel generation...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        generated_images = []
        total_input_tokens = 0
        total_output_tokens = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"Failed to generate variation: {result}")
            else:
                i, response = result
                
                # Log usage for this variation
                self.log_usage_info(response, i + 1)
                
                # Extract image
                image = None
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        image = Image.open(BytesIO(part.inline_data.data))
                        break
                
                if image:
                    generated_images.append(image)
                    # Save each variation as it's generated
                    output_path = f"{output_dir}/design_variation_{i + 1:02d}.png"
                    # Ensure output directory exists
                    os.makedirs(output_dir, exist_ok=True)
                    image.save(output_path)
                    print(f"Saved {output_path}")
                    
                    # Track total tokens
                    if hasattr(response, 'usage_metadata'):
                        usage = response.usage_metadata
                        total_input_tokens += usage.prompt_token_count
                        total_output_tokens += usage.candidates_token_count
                else:
                    print(f"Failed to generate variation {i + 1}")
        
        # Display total usage summary
        total_tokens = total_input_tokens + total_output_tokens
        if total_tokens > 0:
            input_cost = (total_input_tokens / 1000) * 0.000075
            output_cost = (total_output_tokens / 1000) * 0.0003
            total_cost = input_cost + output_cost
            
            print(f"\n📊 Total Usage Summary:")
            print(f"   Total input tokens: {total_input_tokens:,}")
            print(f"   Total output tokens: {total_output_tokens:,}")
            print(f"   Total tokens: {total_tokens:,}")
            print(f"   Estimated total cost: ${total_cost:.6f}")
            print(f"     - Input cost: ${input_cost:.6f}")
            print(f"     - Output cost: ${output_cost:.6f}")
            print(f"   Cost per variation: ${total_cost / len(generated_images):.6f}")
        
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
    variations = asyncio.run(designer.generate_design_variations(
        current_room_paths=current_room_paths,
        inspiration_paths=inspiration_paths,
        room_specs=room_specs,
        design_prompt=design_prompt,
        num_variations=8
    ))
    
    # Save grid
    designer.save_variations_grid(variations)

if __name__ == "__main__":
    main() 