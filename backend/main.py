"""
Waifu Animation Chat Backend
Handles AI chat integration and animation state management
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import asyncio
import json
import random
import httpx
from datetime import datetime
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from waifu_manager import WaifuModelManager, WaifuProfile
from llm_config import LLMClient, LLMProvider, get_llm_config, reload_config

# Load environment variables
load_dotenv(override=True)  # Override ensures .env is reloaded

# Application version
APP_VERSION = "1.0.0-beta"

# Initialize paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
FRONTEND_MODELS_DIR = BASE_DIR / "frontend" / "public" / "models"

# Initialize waifu manager
waifu_manager = WaifuModelManager(MODELS_DIR, FRONTEND_MODELS_DIR)

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Animation states and emotions
EMOTIONS = {
    "neutral": {"arousal": 0.5, "valence": 0.5},
    "happy": {"arousal": 0.7, "valence": 0.8},
    "shy": {"arousal": 0.3, "valence": 0.6},
    "flirty": {"arousal": 0.8, "valence": 0.9},
    "excited": {"arousal": 0.9, "valence": 0.8},
    "affectionate": {"arousal": 0.6, "valence": 0.9},
    "playful": {"arousal": 0.8, "valence": 0.7},
    "seductive": {"arousal": 0.9, "valence": 0.8}
}

# Animation actions based on emotions
ANIMATION_ACTIONS = {
    "neutral": ["idle_sway", "blink", "breathe"],
    "happy": ["smile", "bounce", "head_tilt", "giggle"],
    "shy": ["look_away", "blush", "fidget", "cover_face"],
    "flirty": ["wink", "lip_bite", "hair_flip", "pose"],
    "excited": ["jump", "clap", "spin", "wave"],
    "affectionate": ["blow_kiss", "heart_eyes", "lean_forward", "touch_chest"],
    "playful": ["tongue_out", "peace_sign", "hip_sway", "dance"],
    "seductive": ["sultry_look", "body_stretch", "bedroom_eyes", "slow_pose"]
}

class ChatMessage(BaseModel):
    text: str
    sender: str = "user"
    timestamp: datetime = None

class AnimationState(BaseModel):
    emotion: str = "neutral"
    action: str = "idle"
    intensity: float = 0.5
    arousal: float = 0.5
    valence: float = 0.5

# Keep for backwards compatibility but use WaifuProfile internally
class WaifuModel(BaseModel):
    id: str
    name: str
    personality: str
    image_path: str
    voice_pitch: float = 1.0
    default_emotion: str = "neutral"
    
    @classmethod
    def from_profile(cls, profile: WaifuProfile):
        """Convert WaifuProfile to legacy WaifuModel format"""
        return cls(
            id=profile.id,
            name=profile.name,
            personality=profile.full_personality,
            image_path=waifu_manager.get_image_url(profile.id),
            voice_pitch=profile.voice.pitch,
            default_emotion=profile.default_emotion
        )

# Store active connections and their states
connections: Dict[str, Dict] = {}

def analyze_emotion(text: str) -> str:
    """Simple emotion detection from text"""
    text_lower = text.lower()
    
    # Keyword-based emotion detection (can be enhanced with ML)
    if any(word in text_lower for word in ["love", "kiss", "hug", "cuddle"]):
        return "affectionate"
    elif any(word in text_lower for word in ["hot", "sexy", "beautiful", "gorgeous"]):
        return "seductive"
    elif any(word in text_lower for word in ["play", "fun", "game", "tease"]):
        return "playful"
    elif any(word in text_lower for word in ["hi", "hello", "hey"]):
        return "happy"
    elif any(word in text_lower for word in ["shy", "blush", "embarrass"]):
        return "shy"
    elif any(word in text_lower for word in ["wow", "amazing", "awesome"]):
        return "excited"
    elif any(word in text_lower for word in ["flirt", "wink", "cute"]):
        return "flirty"
    else:
        return "neutral"

def generate_animation_sequence(emotion: str, intensity: float = 0.5) -> List[Dict]:
    """Generate animation sequence based on emotion"""
    actions = ANIMATION_ACTIONS.get(emotion, ANIMATION_ACTIONS["neutral"])
    
    # Create animation sequence
    sequence = []
    
    # Add base idle animation
    sequence.append({
        "action": "idle_sway",
        "duration": 2.0,
        "intensity": 0.3
    })
    
    # Add emotion-specific actions
    for i in range(min(3, len(actions))):
        action = random.choice(actions)
        sequence.append({
            "action": action,
            "duration": random.uniform(1.0, 3.0),
            "intensity": intensity
        })
    
    return sequence

async def call_llm_api(prompt: str, model_personality: str, chat_history: List[Dict] = None) -> str:
    """Call LLM API for chat responses (supports vLLM, Ollama, OpenAI)"""
    
    # Reload config to pick up any .env changes
    reload_config()
    
    # Build conversation context
    system_prompt = f"""You are {model_personality}

IMPORTANT: You should embody this character fully. Express emotions through actions in *asterisks* and use casual, flirty language when appropriate. Keep responses engaging and playful."""
    
    # Build conversation history for context
    full_prompt = ""
    if chat_history:
        # Include last few messages for context
        recent_history = chat_history[-6:]  # Last 3 exchanges
        for msg in recent_history:
            if msg["role"] == "user":
                full_prompt += f"User: {msg['content']}\n"
            else:
                full_prompt += f"Assistant: {msg['content']}\n"
    
    full_prompt += f"User: {prompt}\nAssistant: "
    
    try:
        async with LLMClient() as llm:
            response = await llm.generate(
                prompt=full_prompt,
                system_prompt=system_prompt,
                stop=["\nUser:", "\nHuman:", "\n\n"]
            )
            return response
                
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        # Fallback to demo responses if LLM fails
        emotion = analyze_emotion(prompt)
        demo_responses = {
            "flirty": "*winks playfully* Even without my full power, I still find you interesting~",
            "shy": "*fidgets nervously* S-sorry, I'm having technical difficulties... but I'm still here for you!",
            "playful": "*giggles* My connection's being silly, but that won't stop us from having fun!",
            "neutral": "*smiles warmly* I'm having a small issue, but I'm still happy to chat with you!"
        }
        return demo_responses.get(emotion, demo_responses["neutral"])

@app.get("/")
async def root():
    return {"message": "Waifu Animation Chat API", "version": APP_VERSION}

@app.get("/api/system-info")
async def get_system_info():
    """Get system information including LLM configuration"""
    config = get_llm_config()
    
    # Get friendly model name
    model_display = config.model or "Default Model"
    
    # Handle OpenAI model names
    if config.provider == LLMProvider.OPENAI:
        openai_models = {
            "gpt-4.1-mini": "GPT-4.1 Mini",
            "gpt-4.1-nano": "GPT-4.1 Nano",
            "gpt-4-turbo": "GPT-4 Turbo",
            "gpt-4": "GPT-4",
            "gpt-3.5-turbo": "GPT-3.5 Turbo",
            "o1-mini": "O1 Mini",
            "o3-mini": "O3 Mini"
        }
        model_display = openai_models.get(config.model, config.model)
    
    # Handle Ollama model names
    elif config.provider == LLMProvider.OLLAMA:
        if ":" in model_display:
            # Remove version tag for display
            model_display = model_display.split(":")[0]
        if "/" in model_display:
            # Extract model name from path
            parts = model_display.split("/")
            model_display = parts[-1].replace("-", " ").title()
    
    # Handle vLLM/HuggingFace style model names
    elif "/" in model_display:
        # Simplify model names like "solidrust/dolphin-2.9.2-qwen2-7b-AWQ" to "Dolphin 2.9.2"
        parts = model_display.split("/")
        if len(parts) > 1:
            model_name = parts[-1]
            # Extract main model name
            if "-" in model_name:
                model_parts = model_name.split("-")
                if "dolphin" in model_name.lower():
                    model_display = "Dolphin " + model_parts[1]
                elif "llama" in model_name.lower():
                    model_display = "LLaMA " + model_parts[1] if len(model_parts) > 1 else "LLaMA"
                elif "mistral" in model_name.lower():
                    model_display = "Mistral " + model_parts[1] if len(model_parts) > 1 else "Mistral"
                elif "qwen" in model_name.lower():
                    model_display = "Qwen " + model_parts[1] if len(model_parts) > 1 else "Qwen"
                elif len(model_parts) > 2:
                    model_display = f"{model_parts[0].title()} {model_parts[1]}"
                else:
                    model_display = model_parts[0].title()
    
    return {
        "version": APP_VERSION,
        "llm": {
            "provider": config.provider.value.upper(),
            "model": config.model,
            "model_display": model_display,
            "api_url": config.api_url.split("/v1")[0] if "/v1" in config.api_url else config.api_url,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens
        },
        "features": {
            "voice_synthesis": os.getenv("ENABLE_VOICE_SYNTHESIS", "true").lower() == "true",
            "voice_synthesis_provider": os.getenv("VOICE_SYNTHESIS_PROVIDER", "webspeech"),
            "advanced_physics": os.getenv("ENABLE_ADVANCED_PHYSICS", "true").lower() == "true",
            "max_affection_level": int(os.getenv("MAX_AFFECTION_LEVEL", "100")),
            "nsfw_enabled": os.getenv("NSFW_ENABLED", "true").lower() == "true"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/models")
async def get_models():
    """Get available waifu models"""
    profiles = waifu_manager.get_all_profiles()
    models = [WaifuModel.from_profile(profile) for profile in profiles]
    return {"models": models}

@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    """Get specific model details"""
    profile = waifu_manager.get_profile(model_id)
    if profile:
        return WaifuModel.from_profile(profile)
    return {"error": "Model not found"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    
    # Initialize connection state
    connections[client_id] = {
        "websocket": websocket,
        "model": "luna",
        "animation_state": AnimationState(),
        "chat_history": []
    }
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to Waifu Chat",
            "model": connections[client_id]["model"]
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            if data["type"] == "chat":
                # Process chat message
                user_message = data["message"]
                model_id = connections[client_id]["model"]
                profile = waifu_manager.get_profile(model_id)
                
                if not profile:
                    # Fallback to first available profile
                    profiles = waifu_manager.get_all_profiles()
                    if profiles:
                        profile = profiles[0]
                        model_id = profile.id
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": "No waifu models available"
                        })
                        continue
                
                # Analyze emotion
                emotion = analyze_emotion(user_message)
                emotion_data = EMOTIONS[emotion]
                
                # Generate animation sequence
                animation_sequence = generate_animation_sequence(emotion, emotion_data["arousal"])
                
                # Update animation state
                connections[client_id]["animation_state"] = AnimationState(
                    emotion=emotion,
                    action=animation_sequence[0]["action"],
                    intensity=animation_sequence[0]["intensity"],
                    arousal=emotion_data["arousal"],
                    valence=emotion_data["valence"]
                )
                
                # Get AI response with chat history
                ai_response = await call_llm_api(
                    user_message, 
                    profile.full_personality,
                    connections[client_id]["chat_history"]
                )
                
                # Send response with animation data
                await websocket.send_json({
                    "type": "response",
                    "message": ai_response,
                    "emotion": emotion,
                    "animation": {
                        "sequence": animation_sequence,
                        "state": connections[client_id]["animation_state"].dict()
                    },
                    "timestamp": datetime.now().isoformat()
                })
                
                # Store in chat history
                connections[client_id]["chat_history"].extend([
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": ai_response}
                ])
                
            elif data["type"] == "change_model":
                # Change waifu model
                new_model = data["model"]
                if waifu_manager.get_profile(new_model):
                    connections[client_id]["model"] = new_model
                    await websocket.send_json({
                        "type": "model_changed",
                        "model": new_model
                    })
                    
            elif data["type"] == "get_state":
                # Send current animation state
                await websocket.send_json({
                    "type": "state",
                    "state": connections[client_id]["animation_state"].dict()
                })
                
    except WebSocketDisconnect:
        del connections[client_id]
        print(f"Client {client_id} disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
