#!/usr/bin/env python3
"""
Simple test script following the official Google GenAI documentation exactly
"""

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_simple_generation():
    """Test simple text-to-image generation following official docs"""
    print("Testing simple text-to-image generation...")
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return
    
    # Initialize client exactly as in docs
    client = genai.Client(api_key=api_key)
    
    # Simple prompt exactly as in docs
    prompt = "Create a picture of a modern living room with mid-century furniture"
    
    try:
        print("Making API call...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt],
        )
        
        print("✅ API call successful!")
        print("Processing response...")
        
        # Process response exactly as in docs
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(f"Text response: {part.text}")
            elif part.inline_data is not None:
                print("✅ Image generated!")
                image = Image.open(BytesIO(part.inline_data.data))
                image.save("test_generated_image.png")
                print("Saved as test_generated_image.png")
                return True
        
        print("❌ No image found in response")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_simple_generation() 