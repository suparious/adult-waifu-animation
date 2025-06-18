# Waifu Image Setup Guide

## Quick Start

1. **Place your waifu images in**: `frontend/public/models/`
2. **Name them to match the persona**: 
   - Luna → `luna.png`
   - Sakura → `sakura.png`
3. **Restart the application**

That's it! The system will automatically detect and use your images.

## Image Requirements

### Format & Size
- **File Types**: PNG (recommended), JPG, JPEG, or WebP
- **Dimensions**: 
  - Minimum: 512 x 1024 pixels
  - Recommended: 1024 x 2048 pixels
  - Maximum: 2048 x 4096 pixels
- **Aspect Ratio**: Portrait (1:2 ratio ideal)
- **File Size**: Under 5MB

### Content Guidelines
- **Pose**: Full body, facing forward or 3/4 view
- **Background**: Transparent (PNG) or solid color
- **Expression**: Neutral or slightly smiling
- **Framing**: Character fills 80-90% of height

## Persona System

Each waifu has a complete persona profile that includes:
- Personality traits (flirtatiousness, shyness, etc.)
- Full AI personality description
- Voice characteristics
- Default emotions
- Special animations
- NSFW level settings

### Current Personas

**Luna** - Cyberpunk Tease
- Personality: Flirty, confident, playful
- Style: Neon cyberpunk aesthetic
- Special: Loves to make people blush

**Sakura** - Shy Bookworm  
- Personality: Sweet, easily flustered, romantic
- Style: Soft kawaii aesthetic
- Special: Gets nervous but very affectionate

## Adding Custom Waifus

### Method 1: Quick Add (Image Only)
1. Add image to `frontend/public/models/` with a unique name
2. Create a profile in `models/profiles.json`

### Method 2: Full Custom Profile

Create `models/profiles.json`:

```json
{
  "custom_waifu": {
    "id": "custom_waifu",
    "name": "Your Waifu Name",
    "full_personality": "Detailed personality for AI...",
    "short_description": "Brief UI description",
    "personality_traits": {
      "flirtatiousness": 0.5,
      "playfulness": 0.5,
      "shyness": 0.5,
      "affection": 0.5,
      "confidence": 0.5,
      "seductiveness": 0.5
    },
    "appearance": {
      "hair_color": "#hexcolor",
      "eye_color": "#hexcolor",
      "style": "anime",
      "body_type": "average",
      "height": "medium"
    },
    "voice": {
      "pitch": 1.0,
      "speed": 1.0,
      "tone": "neutral"
    },
    "default_emotion": "neutral",
    "image_file": "custom_waifu.png",
    "nsfw_level": 1,
    "special_animations": ["wink", "blush"],
    "unlock_requirements": {}
  }
}
```

## Animation Mapping

The system procedurally animates your static image with:
- Breathing and idle movements
- Emotion-based animations
- Physics for hair/clothing
- Special actions (winks, poses, etc.)

Better quality images = better animation results!

## Troubleshooting

**Image not showing?**
- Check filename matches persona ID
- Verify image is in `frontend/public/models/`
- Clear browser cache
- Check browser console for errors

**Wrong aspect ratio?**
- Image will be stretched to fit
- Use 1:2 ratio for best results

**File too large?**
- Compress PNG with online tools
- Reduce resolution to 1024x2048
- Convert to WebP for smaller size

## Advanced Tips

1. **Transparency**: Use PNG with transparent background for better blending
2. **Layers**: Keep hair/accessories slightly separated for better physics
3. **Colors**: Bright colors animate better than dark ones
4. **Details**: Higher resolution = better zoom quality

## Directory Structure

```
adult-waifu-animation/
├── frontend/
│   └── public/
│       └── models/          ← Your images go here
│           ├── luna.png
│           ├── sakura.png
│           └── custom.png
└── models/
    ├── config.json          ← Legacy config (optional)
    └── profiles.json        ← Custom profiles (optional)
```

## Example Workflow

1. Find/create a waifu image (1024x2048 PNG)
2. Name it `mywaifu.png`
3. Copy to `frontend/public/models/`
4. Create profile in `models/profiles.json` with id "mywaifu"
5. Restart the app
6. Select your waifu from the dropdown!

Remember: The image is just the visual - the personality and behavior come from the AI configuration!
