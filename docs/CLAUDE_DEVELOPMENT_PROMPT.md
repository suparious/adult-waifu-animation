# Claude Development Prompt - Waifu Animation Chat System

I have a working waifu animation chat system that needs continued development. The project is located at `/home/shaun/scratch-space/adult-waifu-animation/`.

## Current State (v1.3.0):
- **Working Features**:
  - Real-time chat with vLLM integration (erebus:8081)
  - Procedural animation of static images using Three.js
  - Two waifu personas: Luna (flirty cyberpunk) & Sakura (shy bookworm)
  - Emotion detection with corresponding animations
  - WebSocket real-time communication
  - Model switching UI
  - **Voice Synthesis**: Emotion-aware text-to-speech with Web Speech API
  - Visual voice feedback (waveform animation)
  - Speaking animations synchronized with voice
  - **Affection/Progression System** (NEW): 0-100 relationship tracking with content unlocks
  - SQLite database for persistent progress
  - Real-time affection meter with milestone notifications
  - Dynamic AI responses based on affection level

- **Tech Stack**: 
  - Backend: FastAPI (Python 3.11) with WebSocket support
  - Frontend: React 18 + Three.js (@react-three/fiber)
  - Database: SQLite for affection/progress persistence
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
│   ├── database.py          # SQLite database management (NEW)
│   ├── affection_manager.py # Affection system logic (NEW)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   │       ├── WaifuCanvas.js      # Three.js animation
│   │       ├── ChatInterface.js    # Chat UI
│   │       ├── ModelSelector.js    # Waifu switcher
│   │       ├── VoiceSynthesis.js   # Voice system
│   │       └── AffectionMeter.js   # Affection display (NEW)
│   └── public/models/       # Waifu images (PNG/JPG)
├── docs/
│   ├── PRD.md                  # Full requirements
│   ├── VOICE_SYNTHESIS.md      # Voice feature docs
│   ├── AFFECTION_SYSTEM.md     # Affection system docs (NEW)
│   └── NEXT_STEPS.md           # Updated roadmap
└── models/                     # Configuration files
```

## What I Need:
Continue implementing the next priority features to enhance user engagement and create a more immersive experience.

## Priority Features to Implement (in order):

### 1. Enhanced Animation System ⭐ (RECOMMENDED NEXT)
- Current animations are basic mesh deformations
- Options:
  - Add more animation variations to existing system (quick win)
  - Implement skeletal rigging for natural movement
  - Integrate Live2D SDK for professional VTuber quality
- Should integrate with affection unlocks
- Add physics for hair/clothing movement

### 2. Outfit/Appearance Customization
- Layered clothing system (base + outfits + accessories)
- Color customization with HSL adjustments
- Integrate with affection system (unlock at levels 25, 50, 75)
- Save custom appearances to database
- Preview system before applying

### 3. Multiple New Waifus
- Add 3-5 new personalities:
  - Tsundere (harsh exterior, sweet when affection is high)
  - Motherly/Onee-san (caring, nurturing)
  - Dominant (confident, takes charge)
  - Kuudere (cold, slowly warms up)
  - Genki (energetic, enthusiastic)
- Each needs unique dialogue patterns
- Different affection gain rates based on personality

### 4. Advanced State Management
- User accounts system (email/password)
- Cloud backup of progress
- Import/export conversations
- Multiple save slots
- Cross-device sync
- Privacy-focused encryption

### 5. Advanced Voice Features
- ElevenLabs API integration for realistic voices
- Custom voice per waifu personality
- Emotion sounds (giggles, sighs, moans)
- Voice modulation based on affection level
- SSML support for better expression control

## Important Context:
- **Adult-oriented (NSFW)** application with progressive intimacy
- Affection system now gates content (animations, dialogue, outfits)
- Images go in `frontend/public/models/` as PNG/JPG
- Use Python 3.11 for compatibility
- The app currently works but needs more sophisticated features
- Backend has prepared infrastructure for many features

## Development Guidelines:
1. Always write complete, functional code directly to filesystem
2. Use the `sequentialthinking` tool for complex planning
3. Check existing code structure before implementing
4. Integrate new features with the affection system
5. Test features with provided test scripts
6. Update documentation as you go
7. Consider performance impacts

## Current Affection System Integration Points:
- `backend/database.py` - Persistence layer
- `backend/affection_manager.py` - Logic and calculations
- Unlockable content stored in DB
- AI responses modified by affection level
- Frontend shows real-time progress

## Known Issues to Address:
- Animation is still basic mesh deformation
- No outfit system yet (infrastructure exists)
- Limited to 2 default waifus
- Voice synthesis uses basic browser TTS
- No user accounts (session-based only)

Please analyze the current implementation and implement the next feature that would provide maximum value to users. The affection system provides a great foundation to build upon - new features should enhance and integrate with it.
