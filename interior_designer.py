#!/usr/bin/env python3
"""
Simple Interior Designer for Jaidha's Living Room
"""

import os
import asyncio
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from io import BytesIO

from google import genai
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
    room_type: str = "living room"

@dataclass
class DesignPrompt:
    """Design prompt with style and requirements"""
    style: str
    color_scheme: str
    mood: str
    furniture_requirements: List[str]
    additional_notes: str = ""

class InteriorDesigner:
    """Simple interior designer for Jaidha's living room"""
    
    def __init__(self):
        """Initialize the designer with Gemini API key"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-image-preview"
    
    def load_image(self, image_path: str) -> Image.Image:
        """Load and validate an image"""
        try:
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image {image_path}: {e}")
    
    def create_prompt(self, room_specs: RoomSpecs, design_prompt: DesignPrompt, variation_index: int) -> str:
        """Create the design prompt for a variation"""
        furniture_str = ", ".join(design_prompt.furniture_requirements)
        
        prompt = f"""
Create a photorealistic interior design for a {room_specs.room_type} with dimensions {room_specs.width}' x {room_specs.length}' x {room_specs.height}' high.

Design Style: {design_prompt.style}
Color Scheme: {design_prompt.color_scheme}
Mood: {design_prompt.mood}

Required Furniture: {furniture_str}

{design_prompt.additional_notes}

This is variation {variation_index + 1}. Make it unique and distinctive.
"""
        return prompt.strip()
    
    def log_usage_info(self, response, variation_num: int):
        """Log token usage and estimated cost for the API request"""
        try:
            if hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                print(f"\n💰 Usage for variation {variation_num}:")
                print(f"   Input tokens: {usage.prompt_token_count}")
                print(f"   Output tokens: {usage.candidates_token_count}")
                print(f"   Total tokens: {usage.total_token_count}")
                
                # Estimate cost with correct pricing
                # Input: $0.000075 per 1K tokens
                # Output: $30 per 1M tokens = $0.03 per 1K tokens (image output tokenized at 1290 tokens per image)
                input_cost = (usage.prompt_token_count / 1000) * 0.000075
                
                # For image generation, use flat 1290 tokens per image output
                # Check if this is an image generation response
                has_image_output = False
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        has_image_output = True
                        break
                
                if has_image_output:
                    # Use flat 1290 tokens for image output
                    # $30 per 1M tokens = $0.03 per 1K tokens
                    output_cost = (1290 / 1000) * 0.03
                else:
                    # Use actual token count for text output
                    output_cost = (usage.candidates_token_count / 1000) * 0.03
                
                total_cost = input_cost + output_cost
                
                print(f"   Estimated cost: ${total_cost:.6f}")
                if has_image_output:
                    print(f"   (Image output: 1290 tokens flat rate)")
                
        except Exception as e:
            print(f"Could not log usage info: {e}")
    
    async def generate_variations(self, 
                                 current_room_paths: List[str],
                                 room_specs: RoomSpecs,
                                 design_prompt: DesignPrompt = None,
                                 num_variations: int = 3,
                                 output_dir: str = None,
                                 prompts: list = None) -> tuple[List[Image.Image], str]:
        """Generate multiple design variations"""
        print(f"Generating {num_variations} design variations...")
        
        # Create timestamped output directory
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_dir = f"output/{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Output directory: {output_dir}")
        
        # Load current room images
        current_room_images = []
        for path in current_room_paths:
            try:
                img = self.load_image(path)
                current_room_images.append(img)
            except Exception as e:
                print(f"Warning: Could not load image {path}: {e}")
        
        # Create tasks for parallel execution
        async def generate_with_usage(i):
            # Use dynamic prompt if provided, otherwise use the static one
            if prompts is not None:
                prompt = self.create_prompt(room_specs, prompts[i], i)
            elif design_prompt is None:
                from jaidha_room import create_dynamic_prompt
                prompt = self.create_prompt(room_specs, create_dynamic_prompt(i), i)
            else:
                prompt = self.create_prompt(room_specs, design_prompt, i)
            
            contents = [prompt] + current_room_images[:3]  # Up to 3 images
            
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=contents,
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
                    # Save each variation
                    output_path = f"{output_dir}/design_variation_{i + 1:02d}.png"
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
            output_cost = (len(generated_images) * 1290 / 1000) * 0.03
            total_cost = input_cost + output_cost
            
            print(f"\n📊 Total Usage Summary:")
            print(f"   Total input tokens: {total_input_tokens:,}")
            print(f"   Total output tokens: {len(generated_images) * 1290:,} (1290 per image)")
            print(f"   Total tokens: {total_tokens:,}")
            print(f"   Estimated total cost: ${total_cost:.6f}")
            print(f"   Cost per variation: ${total_cost / len(generated_images):.6f}")
        
        return generated_images, output_dir 