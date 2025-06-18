"""
Waifu Model Management System
Handles persona profiles, image management, and model configuration
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import json
import os

class WaifuPersonality(BaseModel):
    """Personality traits for a waifu"""
    flirtatiousness: float = Field(ge=0.0, le=1.0, default=0.5)
    playfulness: float = Field(ge=0.0, le=1.0, default=0.5)
    shyness: float = Field(ge=0.0, le=1.0, default=0.5)
    affection: float = Field(ge=0.0, le=1.0, default=0.5)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    seductiveness: float = Field(ge=0.0, le=1.0, default=0.5)

class WaifuVoice(BaseModel):
    """Voice characteristics"""
    pitch: float = Field(ge=0.5, le=2.0, default=1.0)
    speed: float = Field(ge=0.5, le=2.0, default=1.0)
    tone: str = "neutral"  # neutral, soft, energetic, sultry

class WaifuAppearance(BaseModel):
    """Visual appearance settings"""
    hair_color: str = "#000000"
    eye_color: str = "#000000"
    style: str = "anime"  # anime, realistic, cartoon
    body_type: str = "average"  # petite, average, curvy
    height: str = "medium"  # short, medium, tall

class WaifuProfile(BaseModel):
    """Complete waifu profile with all attributes"""
    id: str
    name: str
    full_personality: str  # Detailed personality description for AI
    short_description: str  # Brief description for UI
    personality_traits: WaifuPersonality
    appearance: WaifuAppearance
    voice: WaifuVoice
    default_emotion: str = "neutral"
    image_file: Optional[str] = None  # Filename in models directory
    nsfw_level: int = Field(ge=0, le=3, default=1)  # 0=SFW, 1=Flirty, 2=Suggestive, 3=Explicit
    special_animations: List[str] = []
    unlock_requirements: Dict[str, int] = {}  # animation: affection_level

class WaifuModelManager:
    def __init__(self, models_dir: Path, frontend_models_dir: Path):
        self.models_dir = models_dir
        self.frontend_models_dir = frontend_models_dir
        self.profiles: Dict[str, WaifuProfile] = {}
        self.load_profiles()
        
    def load_profiles(self):
        """Load waifu profiles from configuration"""
        # Default profiles
        self.profiles = {
            "luna": WaifuProfile(
                id="luna",
                name="Luna",
                full_personality="""I'm Luna, a playful and flirty cyberpunk girl from Neo-Tokyo. I love teasing people and making them blush, but I also have a caring side. I work as a digital artist by day and party at underground clubs by night. I'm confident, outgoing, and always up for an adventure. I express myself through playful banter, winks, and the occasional sultry comment. I love technology, neon lights, and making new connections.""",
                short_description="Playful cyberpunk girl who loves to tease",
                personality_traits=WaifuPersonality(
                    flirtatiousness=0.8,
                    playfulness=0.9,
                    shyness=0.2,
                    affection=0.7,
                    confidence=0.8,
                    seductiveness=0.7
                ),
                appearance=WaifuAppearance(
                    hair_color="#ff6ec7",
                    eye_color="#9f7aea",
                    style="cyberpunk",
                    body_type="average",
                    height="medium"
                ),
                voice=WaifuVoice(pitch=1.2, speed=1.0, tone="energetic"),
                default_emotion="flirty",
                image_file="sakura.png",
                nsfw_level=2,
                special_animations=["wink", "hip_sway", "blow_kiss", "seductive_pose"],
                unlock_requirements={
                    "blow_kiss": 25,
                    "seductive_pose": 50
                }
            ),
            "sakura": WaifuProfile(
                id="sakura",
                name="Sakura",
                full_personality="""I'm Sakura, a sweet and shy college student studying literature. I get flustered easily, especially around people I find attractive. I love reading manga, writing poetry, and quiet cafes. Despite my shyness, I have a romantic heart and dream of finding true love. I tend to stutter when nervous and often hide behind my books. But once I'm comfortable with someone, I can be quite affectionate and loving. I express my feelings through blushes, soft giggles, and gentle touches.""",
                short_description="Sweet and shy girl who gets flustered easily",
                personality_traits=WaifuPersonality(
                    flirtatiousness=0.3,
                    playfulness=0.5,
                    shyness=0.9,
                    affection=0.8,
                    confidence=0.4,
                    seductiveness=0.2
                ),
                appearance=WaifuAppearance(
                    hair_color="#ffb6d9",
                    eye_color="#ff66a3",
                    style="kawaii",
                    body_type="petite",
                    height="short"
                ),
                voice=WaifuVoice(pitch=1.1, speed=0.9, tone="soft"),
                default_emotion="shy",
                image_file="luna.jpg",
                nsfw_level=1,
                special_animations=["blush", "hide_face", "shy_smile", "fidget"],
                unlock_requirements={
                    "shy_smile": 15,
                    "gentle_touch": 40
                }
            )
        }
        
        # Load custom profiles from config file if exists
        config_path = self.models_dir / "profiles.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    custom_profiles = json.load(f)
                    for profile_id, profile_data in custom_profiles.items():
                        self.profiles[profile_id] = WaifuProfile(**profile_data)
            except Exception as e:
                print(f"Error loading custom profiles: {e}")
    
    def scan_for_images(self) -> Dict[str, str]:
        """Scan the frontend models directory for available images"""
        images = {}
        
        if self.frontend_models_dir.exists():
            for file in self.frontend_models_dir.iterdir():
                if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                    # Match image to profile by filename (without extension)
                    profile_id = file.stem.lower()
                    images[profile_id] = file.name
        
        return images
    
    def get_profile(self, profile_id: str) -> Optional[WaifuProfile]:
        """Get a specific waifu profile"""
        return self.profiles.get(profile_id)
    
    def get_all_profiles(self) -> List[WaifuProfile]:
        """Get all available profiles"""
        # Update image paths based on available files
        available_images = self.scan_for_images()
        
        profiles_list = []
        for profile_id, profile in self.profiles.items():
            # Check if image exists for this profile
            if profile_id in available_images:
                profile.image_file = available_images[profile_id]
            
            profiles_list.append(profile)
        
        return profiles_list
    
    def create_custom_profile(self, profile_data: dict) -> WaifuProfile:
        """Create a new custom waifu profile"""
        profile = WaifuProfile(**profile_data)
        self.profiles[profile.id] = profile
        self.save_profiles()
        return profile
    
    def save_profiles(self):
        """Save custom profiles to configuration"""
        config_path = self.models_dir / "profiles.json"
        
        # Only save custom profiles (not default ones)
        custom_profiles = {
            pid: profile.dict() 
            for pid, profile in self.profiles.items() 
            if pid not in ["luna", "sakura"]
        }
        
        with open(config_path, 'w') as f:
            json.dump(custom_profiles, f, indent=2)
    
    def get_image_url(self, profile_id: str) -> str:
        """Get the URL for a waifu's image"""
        profile = self.get_profile(profile_id)
        if profile and profile.image_file:
            return f"/models/{profile.image_file}"
        
        # Return placeholder if no image
        return f"/models/placeholder.png"

# Image format requirements
IMAGE_REQUIREMENTS = """
# Waifu Image Requirements

## Format
- **File Types**: PNG (preferred), JPG, JPEG, or WebP
- **Transparency**: PNG with transparent background recommended
- **Color Mode**: RGB (not CMYK)

## Dimensions
- **Minimum Size**: 512 x 1024 pixels
- **Recommended Size**: 1024 x 2048 pixels
- **Maximum Size**: 2048 x 4096 pixels
- **Aspect Ratio**: Portrait orientation (1:2 ratio ideal)

## Content Guidelines
- **Pose**: Full body, facing forward or 3/4 view
- **Framing**: Character should fill 80-90% of frame height
- **Centering**: Character centered horizontally
- **Expression**: Neutral or slightly smiling
- **Clothing**: Appropriate to character personality

## Technical Requirements
- **File Size**: Under 5MB
- **Naming**: Use profile ID as filename (e.g., luna.png, sakura.png)
- **Location**: Place in frontend/public/models/ directory

## For Best Animation Results
- Clear separation between body parts
- Distinct hair that can be animated
- Visible eyes for expression changes
- Arms slightly away from body
- No complex overlapping elements
"""

def create_placeholder_image():
    """Create a placeholder image for missing waifus"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create gradient background
        width, height = 512, 1024
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw gradient
        for y in range(height):
            color = int(255 * (1 - y / height))
            draw.rectangle([(0, y), (width, y + 1)], 
                         fill=(255, color, 200, 200))
        
        # Draw silhouette
        draw.ellipse([(width//2 - 80, 100), (width//2 + 80, 300)], 
                    fill=(255, 255, 255, 180))
        draw.rectangle([(width//2 - 60, 250), (width//2 + 60, 800)], 
                      fill=(255, 255, 255, 180))
        
        # Add text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        except:
            font = None
        
        draw.text((width//2, height//2), "WAIFU", 
                 fill=(100, 100, 100, 255), 
                 anchor="mm", font=font)
        
        return img
    except ImportError:
        print("PIL not available, skipping placeholder creation")
        return None
