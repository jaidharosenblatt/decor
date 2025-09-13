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

from PIL import Image
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import ContentListUnion

# Load environment variables
load_dotenv()

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
                                 images: List[str],
                                 prompts: list,
                                 output_dir: str,
                                 num_variations: int = 3) -> tuple[List[Image.Image], str]:
        """Generate multiple design variations"""
        print(f"Generating {num_variations} design variations...")

        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Output directory: {output_dir}")

        # Load all images
        loaded_images = []
        for path in images:
            try:
                img = self.load_image(path)
                loaded_images.append(img)
            except Exception as e:
                print(f"Warning: Could not load image {path}: {e}")
        
        # Create tasks for parallel execution
        async def generate_with_usage(prompt:str, i:int):
            # Add variation index and image references to prompt
            enhanced_prompt = f"""VARIATION #{i+1}

{prompt}"""

            if len(loaded_images) > 3:
                print(f"Warning: Too many images ({len(loaded_images)}), using only the first 3")
                images_to_use = loaded_images[:3]
            else:
                images_to_use = loaded_images

            contents = [enhanced_prompt] + images_to_use
            
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=contents,
            )
            return i, response
        
        tasks = [generate_with_usage(prompt, i) for i, prompt in enumerate(prompts)]
        
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