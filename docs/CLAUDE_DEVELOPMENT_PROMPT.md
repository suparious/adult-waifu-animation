# Claude Development Prompt - Waifu Animation Chat System

I have a working waifu animation chat system that needs continued development. The project is located at `/home/shaun/scratch-space/adult-waifu-animation/`.

## Current State (v1.1.0):
- **Working Features**:
  - Real-time chat with vLLM integration (erebus:8081)
  - Procedural animation of static images using Three.js
  - Two waifu personas: Luna (flirty cyberpunk) & Sakura (shy bookworm)
  - Emotion detection with corresponding animations
  - WebSocket real-time communication
  - Model switching UI
  - **Voice Synthesis** (NEW): Emotion-aware text-to-speech with Web Speech API
  - Visual voice feedback (waveform animation)
  - Speaking animations synchronized with voice

- **Tech Stack**: 
  - Backend: FastAPI (Python 3.11) with WebSocket support
  - Frontend: React 18 + Three.js (@react-three/fiber)
  - Package Managers: pip/venv (backend), yarn (frontend)
  - Voice: Web Speech API (browser-native)

## Project Structure:
```
adult-waifu-animation/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── animation_engine.py  # Procedural animation system
│   ├── waifu_manager.py     # Model/persona management
│   ├── llm_config.py        # LLM configuration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   │       ├── WaifuCanvas.js     # Three.js animation
│   │       ├── ChatInterface.js   # Chat UI
│   │       ├── ModelSelector.js   # Waifu switcher
│   │       └── VoiceSynthesis.js  # Voice system (NEW)
│   └── public/models/       # Waifu images (PNG/JPG)
├── docs/
│   ├── PRD.md              # Full requirements
│   ├── VOICE_SYNTHESIS.md  # Voice feature docs
│   └── NEXT_STEPS.md       # Roadmap
└── models/                 # Configuration files
```

## What I Need:
Continue implementing the next priority features to enhance user engagement and create a more immersive experience.

## Priority Features to Implement (in order):

### 1. Affection/Progression System ⭐ (RECOMMENDED NEXT)
- Track relationship progress (0-100 affection points)
- Unlock new animations, outfits, and dialogue at milestones
- NSFW content progression based on affection level
- Visual indicators of affection state
- Save progress between sessions

### 2. State Persistence
- SQLite database for storing:
  - Chat history
  - Affection levels
  - Unlocked content
  - User preferences
- Session management
- Export/import conversations

### 3. Enhanced Animation System
- More animation variations for existing system
- Consider Live2D integration (requires .model3.json files)
- Improved physics for hair/clothing
- Facial expressions and lip sync
- Touch/click interactions

### 4. Outfit/Appearance Customization
- Layered clothing system (base + outfits + accessories)
- Color customization
- Unlockable outfits tied to affection levels
- Save custom appearances

### 5. Advanced Voice Features
- ElevenLabs API integration for better voices
- Custom voice per waifu
- Emotion sounds (giggles, sighs, moans)
- SSML support for better control

## Important Context:
- **Adult-oriented (NSFW)** application with progressive intimacy
- Images go in `frontend/public/models/` as PNG/JPG
- Use Python 3.11 for compatibility
- The app currently works but needs more sophisticated features
- Backend has prepared infrastructure for many features (check `waifu_manager.py`)

## Development Guidelines:
1. Always write complete, functional code directly to filesystem
2. Use the `sequentialthinking` tool for complex planning
3. Check existing code structure before implementing
4. Test features with provided test scripts
5. Update documentation as you go
6. Consider performance impacts

## Known Issues:
- Animation is basic mesh deformation (not skeletal)
- No outfit system yet
- No state persistence
- Limited to 2 default waifus
- Voice synthesis uses basic browser TTS

Please analyze the current implementation and implement the next feature that would provide maximum value to users. Start by exploring the codebase to understand the current architecture.
