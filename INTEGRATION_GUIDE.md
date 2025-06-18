# Integration Guide

## vLLM Integration

To connect the waifu chat system to vLLM or any OpenAI-compatible API:

### 1. Configure vLLM Server

First, ensure your vLLM server is running:

```bash
# Example vLLM startup
python -m vllm.entrypoints.openai.api_server \
    --model your-model-name \
    --port 8001 \
    --max-model-len 4096
```

### 2. Update Backend Configuration

Edit `backend/.env`:

```env
VLLM_API_URL=http://localhost:8001/v1/completions
VLLM_API_KEY=your-api-key-if-needed
VLLM_MODEL=your-model-name
```

### 3. Modify the Backend Code

In `backend/main.py`, update the `call_llm_api` function:

```python
async def call_llm_api(prompt: str, model_personality: str) -> str:
    """Call vLLM API for chat responses"""
    async with httpx.AsyncClient() as client:
        # Build the full prompt with personality
        full_prompt = f"""You are {model_personality}
        
User: {prompt}
Assistant: """
        
        response = await client.post(
            os.getenv("VLLM_API_URL", "http://localhost:8001/v1/completions"),
            json={
                "prompt": full_prompt,
                "max_tokens": 150,
                "temperature": 0.8,
                "stop": ["\n\nUser:", "\n\nHuman:"],
                "presence_penalty": 0.6,
                "frequency_penalty": 0.3
            },
            headers={
                "Authorization": f"Bearer {os.getenv('VLLM_API_KEY', '')}"
            } if os.getenv('VLLM_API_KEY') else {}
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["text"].strip()
        else:
            return "I'm having trouble connecting right now... *looks worried*"
```

## Adding Custom Waifu Models

### 1. Prepare Your Waifu Image

Your waifu image should be:
- PNG format with transparency
- Minimum 1024x2048 pixels
- Full body pose facing forward
- Clear separation between body parts for rigging

### 2. Create Model Configuration

Add to `models/config.json`:

```json
{
  "models": {
    "your_waifu_name": {
      "id": "your_waifu_name",
      "name": "Display Name",
      "personality": "Detailed personality description for the AI...",
      "traits": {
        "flirtatiousness": 0.0-1.0,
        "playfulness": 0.0-1.0,
        "shyness": 0.0-1.0,
        "affection": 0.0-1.0,
        "confidence": 0.0-1.0
      },
      "appearance": {
        "hair_color": "#hexcolor",
        "eye_color": "#hexcolor",
        "style": "style_name"
      },
      "animations": {
        "idle": ["animation_list"],
        "happy": ["animation_list"],
        "special": ["animation_list"]
      },
      "voice": {
        "pitch": 1.0,
        "speed": 1.0,
        "tone": "voice_tone"
      }
    }
  }
}
```

### 3. Add to Backend Models

In `backend/main.py`, add your model:

```python
waifu_models = {
    # ... existing models ...
    "your_waifu_name": WaifuModel(
        id="your_waifu_name",
        name="Display Name",
        personality="Your waifu's personality...",
        image_path="/models/your_waifu.png",
        voice_pitch=1.0,
        default_emotion="neutral"
    )
}
```

### 4. Add Image to Frontend

1. Place your waifu image in `frontend/public/models/your_waifu.png`
2. Update the model selector to include your waifu

### 5. Create Custom Animations (Optional)

In `backend/animation_engine.py`, add custom animations:

```python
def _your_waifu_special_animation(self, intensity: float) -> List[AnimationKeyframe]:
    """Custom animation for your waifu"""
    keyframes = []
    # Define your custom animation keyframes
    return keyframes
```

## Advanced Customization

### Custom Emotion Detection

Enhance emotion detection for your waifu's personality:

```python
def analyze_emotion_for_waifu(text: str, waifu_id: str) -> str:
    """Custom emotion detection based on waifu personality"""
    if waifu_id == "your_waifu_name":
        # Custom emotion rules
        if "specific_keyword" in text.lower():
            return "special_emotion"
    
    return analyze_emotion(text)  # Fallback to default
```

### Progressive Unlock System

Implement affection-based content:

```python
class AffectionSystem:
    def __init__(self):
        self.user_affection = {}
    
    def increase_affection(self, user_id: str, amount: float):
        current = self.user_affection.get(user_id, 0)
        self.user_affection[user_id] = min(100, current + amount)
        return self.get_unlock_level(user_id)
    
    def get_unlock_level(self, user_id: str) -> str:
        affection = self.user_affection.get(user_id, 0)
        if affection >= 75:
            return "intimate"
        elif affection >= 50:
            return "close"
        elif affection >= 25:
            return "friend"
        else:
            return "acquaintance"
```

### Voice Synthesis Integration

For voice output using Web Speech API:

```javascript
// In ChatInterface.js
const speakMessage = (text, voicePitch = 1.0) => {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.pitch = voicePitch;
    utterance.rate = 0.9;
    utterance.volume = 0.8;
    
    // Select voice (if available)
    const voices = speechSynthesis.getVoices();
    const femaleVoice = voices.find(voice => 
      voice.name.includes('female') || 
      voice.name.includes('Female')
    );
    
    if (femaleVoice) {
      utterance.voice = femaleVoice;
    }
    
    speechSynthesis.speak(utterance);
  }
};
```

## Performance Optimization

### Backend Optimization

1. **Enable Response Streaming**:
```python
async def stream_llm_response(prompt: str):
    # Implement streaming for faster perceived response
    pass
```

2. **Cache Common Responses**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_animation(emotion: str, intensity: float):
    return generate_animation_sequence(emotion, intensity)
```

### Frontend Optimization

1. **Lazy Load Models**:
```javascript
const ModelLoader = React.lazy(() => import('./ModelLoader'));
```

2. **Optimize Three.js Performance**:
```javascript
// Reduce draw calls
const geometry = new THREE.BufferGeometry();
// Use instanced meshes for particles
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
```

## Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
# Backend
FROM python:3.9
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Security Considerations

1. **API Rate Limiting**:
```python
from slowapi import Limiter
limiter = Limiter(key_func=lambda: request.client.host)
app.state.limiter = limiter
```

2. **Content Filtering**:
```python
def filter_inappropriate_content(text: str) -> str:
    # Implement content filtering
    return filtered_text
```

3. **User Authentication** (if needed):
```python
from fastapi_users import FastAPIUsers
# Implement user authentication
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check CORS settings
   - Ensure backend is running
   - Verify firewall settings

2. **Animation Lag**
   - Reduce particle count
   - Lower animation complexity
   - Enable hardware acceleration

3. **vLLM Integration Issues**
   - Verify API endpoint
   - Check model compatibility
   - Monitor token limits

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Community and Support

For additional help:
- Check the README.md
- Review code comments
- Test with provided examples

Remember to always test new waifus thoroughly before deployment!
