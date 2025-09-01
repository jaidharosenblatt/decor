# Interior Designer - AI-Powered Room Design Generator

Generate beautiful interior design variations for your living room using Google's Gemini API. This tool takes your current room photos, measurements, design preferences, and inspiration images to create multiple unique design concepts.

## Features

- 🏠 **Room-Aware Design**: Uses your actual room dimensions and layout
- 🎨 **Style Variations**: Generates diverse styles from modern minimalist to bohemian
- 📸 **Image Integration**: Incorporates your current room photos and inspiration images
- 🔄 **Multiple Variations**: Creates 8+ unique design concepts with high variation
- 📐 **Accurate Scaling**: Maintains proper furniture proportions and room scale
- 🎯 **Customizable**: Specify exact furniture requirements and design preferences

## Prerequisites

1. **Google Gemini API Key**: Get your API key from [Google AI Studio](https://aistudio.google.com/)
2. **Python 3.11+**: The script requires Python 3.11 or higher
3. **uv**: Fast Python package manager (automatically installed)

## Setup

1. **Clone and navigate to the project**:

   ```bash
   cd /path/to/your/project
   ```

2. **Set up your API key**:
   Create a `.env` file in the project root:

   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Install dependencies** (already done with uv):
   ```bash
   uv sync
   ```

## Usage

### Command Line Interface (Recommended)

The easiest way to use the tool is through the CLI:

```bash
# Basic usage with room dimensions
python cli.py --width 16 --length 20 --height 9 --windows 2 --doors 1

# With current room images
python cli.py --width 16 --length 20 --current-room-images room1.jpg room2.jpg

# With inspiration images
python cli.py --width 16 --length 20 --inspiration-images insp1.jpg insp2.jpg

# Custom style and furniture requirements
python cli.py --width 16 --length 20 --style "modern minimalist" \
              --colors "neutral grays and whites" \
              --mood "relaxing and peaceful" \
              --furniture "comfortable sofa" "coffee table" "entertainment center" \
              --notes "Include lots of natural light and plants"

# Generate more variations
python cli.py --width 16 --length 20 --variations 12

# Specify output directory
python cli.py --width 16 --length 20 --output-dir ./my_designs
```

### CLI Options

| Option                  | Description                      | Default                                                      |
| ----------------------- | -------------------------------- | ------------------------------------------------------------ |
| `--width`               | Room width in feet               | Required                                                     |
| `--length`              | Room length in feet              | Required                                                     |
| `--height`              | Room height in feet              | 9.0                                                          |
| `--windows`             | Number of windows                | 2                                                            |
| `--doors`               | Number of doors                  | 1                                                            |
| `--room-type`           | Type of room                     | "living room"                                                |
| `--style`               | Design style                     | "modern minimalist"                                          |
| `--colors`              | Color scheme                     | "neutral grays and whites"                                   |
| `--mood`                | Room mood                        | "relaxing and peaceful"                                      |
| `--furniture`           | Required furniture items         | ["comfortable sofa", "coffee table", "entertainment center"] |
| `--notes`               | Additional design notes          | ""                                                           |
| `--current-room-images` | Paths to current room images     | []                                                           |
| `--inspiration-images`  | Paths to inspiration images      | []                                                           |
| `--variations`          | Number of variations to generate | 8                                                            |
| `--output-dir`          | Output directory                 | "."                                                          |

### Programmatic Usage

You can also use the script programmatically:

```python
from interior_designer import InteriorDesigner, RoomSpecs, DesignPrompt

# Initialize designer
designer = InteriorDesigner()

# Define room specifications
room_specs = RoomSpecs(
    width=16.0,
    length=20.0,
    height=9.0,
    window_count=2,
    door_count=1,
    room_type="living room"
)

# Define design prompt
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

# Generate variations
variations = designer.generate_design_variations(
    current_room_paths=["room1.jpg", "room2.jpg"],
    inspiration_paths=["insp1.jpg", "insp2.jpg"],
    room_specs=room_specs,
    design_prompt=design_prompt,
    num_variations=8
)

# Save grid overview
designer.save_variations_grid(variations, "all_variations.png")
```

## Available Styles

The tool includes 16 different style variations:

- Modern Minimalist
- Cozy Bohemian
- Scandinavian
- Industrial Chic
- Traditional Elegant
- Mid-Century Modern
- Coastal
- Rustic Farmhouse
- Contemporary Luxury
- Eclectic
- Zen Minimalism
- Art Deco
- Vintage Industrial
- Tropical Modern
- Nordic Hygge
- Mediterranean

## Color Schemes

10 different color scheme variations:

- Neutral grays and whites
- Warm earth tones
- Cool blues and greens
- Bold jewel tones
- Soft pastels
- Monochromatic
- Complementary colors
- Analogous color scheme
- High contrast black and white
- Warm neutrals

## Output

The tool generates:

1. **Individual variation images**: `design_variation_01.png`, `design_variation_02.png`, etc.
2. **Grid overview**: `all_variations.png` showing all variations in a single image
3. **Console output**: Progress updates and final summary

## Tips for Best Results

1. **Provide clear room photos**: Take photos from different angles showing the current layout
2. **Use high-quality inspiration images**: Choose images that clearly show the style you want
3. **Be specific with furniture**: List exact pieces you want included
4. **Include measurements**: Accurate room dimensions help with proper scaling
5. **Add context notes**: Mention specific requirements like "pet-friendly" or "kid-friendly"

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `GEMINI_API_KEY` is set in the `.env` file
2. **Image Loading Error**: Ensure image files exist and are in supported formats (JPG, PNG)
3. **No Images Generated**: Check your API quota and ensure prompts are clear and appropriate

### Getting Help

- Check the console output for detailed error messages
- Ensure all required arguments are provided
- Verify image file paths are correct
- Check your Gemini API quota and billing status

## License

This project is licensed under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!
