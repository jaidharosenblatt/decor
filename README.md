# Jaidha's Living Room Designer

A simple, focused tool for generating interior design variations for Jaidha's specific living room using Google's Gemini API. This tool takes current room photos and generates multiple unique design concepts with proper room dimensions and furniture placement.

## Features

- 🏠 **Room-Aware Design**: Uses exact room dimensions (55.5in left side, 168in sliding glass wall, etc.)
- 🎨 **Style Variations**: Generates mid-century modern designs with warm/cool balance
- 📸 **Image Integration**: Incorporates current room photos automatically
- 🔄 **Multiple Variations**: Creates 3 unique design concepts in parallel
- 📐 **Accurate Scaling**: Maintains proper room proportions and existing furniture
- 💰 **Usage Tracking**: Shows token usage and estimated costs for each request
- 📁 **Organized Output**: Timestamped folders for each generation run

## Prerequisites

1. **Google Gemini API Key**: Get your API key from [Google AI Studio](https://aistudio.google.com/)
2. **Python 3.11+**: The script requires Python 3.11 or higher
3. **uv**: Fast Python package manager

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

3. **Install dependencies**:

   ```bash
   uv sync
   ```

4. **Add your room photos**:
   - Put current room photos in the `current/` folder
   - Put furniture photos in the `items/` folder (optional)
   - Put inspiration photos in the `inspo/` folder (optional)

## Usage

### Simple Usage

Just run the main script:

```bash
uv run python jaidha_room.py
```

That's it! The script will:

- Load your room photos from `current/`
- Generate 3 design variations in parallel
- Save them to a timestamped folder in `output/`
- Show usage costs and token counts
- Create a grid overview of all variations

### Output Structure

Each run creates a timestamped folder:

```
output/
└── 2025-08-31_23-42-40/
    ├── design_variation_01.png
    ├── design_variation_02.png
    ├── design_variation_03.png
    └── jaidha_living_room_variations.png
```

### Design Specifications

The script is configured for Jaidha's specific living room:

**Room Dimensions:**

- Width: 14.0' (168" sliding glass wall)
- Length: 8.83' (106" back sofa wall)
- Height: 9.0' (107")

**Design Style:**

- Mid-century modern influence
- Warm leathers and wood with cool neutrals
- Curated comfort with light and contrast play

**Critical Requirements:**

- Existing grey leather couch (MUST KEEP)
- Existing floors (MUST KEEP)
- Grey couch faces projector at top of room
- Camera shows back of couch facing projector
- Room dimensions and proportions preserved exactly

**Variation Focus:**

- Wall furniture (materials, types, styles, colors)
- Wall colors (white, cream, gray, beige, blue-gray, taupe)
- Rug types (geometric, jute, Persian, abstract, kilim, solid)
- Handles room asymmetry properly

## Cost Information

The tool tracks usage and shows costs:

- **Input tokens**: ~2,400 per variation (~$0.00018)
- **Output tokens**: ~1,350 per variation (~$0.00040)
- **Total cost per variation**: ~$0.00058
- **Total cost for 3 variations**: ~$0.00175

## File Structure

```
decor/
├── jaidha_room.py          # Main script to run
├── interior_designer.py    # Core generation logic
├── pyproject.toml          # Dependencies
├── .env                    # Your API key
├── current/                # Current room photos
│   └── image.png
├── items/                  # Furniture photos
│   └── couch.png
├── inspo/                  # Inspiration photos
│   ├── image.png
│   ├── Pasted Graphic.png
│   └── ...
└── output/                 # Generated variations
    └── 2025-08-31_23-42-40/
        ├── design_variation_01.png
        ├── design_variation_02.png
        ├── design_variation_03.png
        └── jaidha_living_room_variations.png
```

## Customization

To modify the design preferences, edit the `design_prompt` in `jaidha_room.py`:

```python
design_prompt = DesignPrompt(
    style="mid-century modern",
    color_scheme="warm leathers and wood with cool neutrals",
    mood="curated comfort with light and contrast play",
    furniture_requirements=[
        "existing grey leather couch (MUST KEEP - do not change)",
        # ... add your furniture requirements
    ],
    additional_notes="""
    # ... add your specific design notes
    """
)
```

## Troubleshooting

**API Key Issues:**

- Make sure your `.env` file contains `GEMINI_API_KEY=your_key_here`
- Verify your API key is valid and has sufficient quota

**Image Loading Issues:**

- Ensure images in `current/` folder are valid image files
- Images should be in common formats (PNG, JPG, etc.)

**Generation Failures:**

- Check your internet connection
- Verify API quota hasn't been exceeded
- Try running again (API can be occasionally unstable)

## Dependencies

- `google-genai`: Google Gemini API client
- `PIL`: Image processing
- `python-dotenv`: Environment variable loading
- `asyncio`: Async/parallel processing

## License

This project is for personal use by Jaidha.
