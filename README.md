# Waifu Animation Chat System

An interactive waifu chat system with real-time procedural animations, AI-powered conversations, and VTuber-like capabilities.

## Features

- 🎨 **Real-time 3D Animation**: Procedural animations using Three.js with emotion-based movements
- 💬 **AI Chat Integration**: Ready for vLLM or OpenAI-compatible API integration
- 🎭 **Multiple Waifu Models**: Easily extensible system for adding new characters
- 🌟 **Emotion Detection**: Automatic emotion analysis and corresponding animations
- 💕 **Progressive Interaction**: Affection system that unlocks new animations
- 🎪 **Physics Simulation**: Natural hair and clothing movement
- 🔊 **Voice Synthesis**: Emotion-aware text-to-speech with visual feedback (NEW!)

## Requirements

- **Python 3.11** (recommended) - See [PYTHON_VERSION_GUIDE.md](PYTHON_VERSION_GUIDE.md)
- **Node.js 16+**
- **pyenv** (recommended for Python version management)

## Quick Start

1. **Setup the environment:**
   ```bash
   chmod +x *.sh
   ./setup.sh
   ```

2. **Configure vLLM API:**
   Edit `backend/.env` to add your vLLM API endpoint:
   ```env
   VLLM_API_URL=http://your-server:8081/v1/completions
   VLLM_MODEL=your-model-name
   ```

3. **Add your waifu images:**
   - Place PNG images in `frontend/public/models/`
   - Name them `luna.png` and `sakura.png`
   - See [IMAGE_SETUP_GUIDE.md](IMAGE_SETUP_GUIDE.md) for details

4. **Run the application:**
   ```bash
   ./run.sh
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Architecture

### Backend (FastAPI)
- WebSocket chat server
- Emotion detection system
- Animation state management
- vLLM/OpenAI API integration
- Model configuration management

### Frontend (React + Three.js)
- 3D waifu rendering with procedural animation
- Real-time chat interface
- Model selection system
- WebSocket communication
- Responsive animations based on emotions

## Adding Waifu Images & Models

### Quick Image Setup
1. Add your images to `frontend/public/models/`
2. Name them to match personas (e.g., `luna.png`, `sakura.png`)
3. Images should be 1024x2048 PNG format (portrait orientation)
4. System automatically detects and uses them

### Full Setup Guide
See [IMAGE_SETUP_GUIDE.md](IMAGE_SETUP_GUIDE.md) for:
- Detailed image requirements
- Custom persona creation
- Troubleshooting tips
- Advanced configuration

## Animation System

The animation system supports:
- Idle animations (breathing, swaying, blinking)
- Emotion-based animations (happy, shy, flirty, etc.)
- Physics simulation for hair and clothing
- Smooth transitions between states
- Customizable intensity and timing

## API Endpoints

- `GET /api/models` - List available models
- `GET /api/models/{model_id}` - Get model details
- `WebSocket /ws/{client_id}` - Real-time chat connection

## Configuration

### Backend Configuration
Edit `backend/.env` for:
- vLLM API settings
- Feature toggles
- Security settings
- Performance tuning

### Frontend Configuration
The frontend now has a centralized configuration system:
- Main config: `frontend/src/config.js`
- Local overrides: Create `frontend/src/config.local.js` (git-ignored)
- See [FRONTEND_CONFIG.md](docs/FRONTEND_CONFIG.md) for detailed documentation

Quick example - create `frontend/src/config.local.js`:
```javascript
export default {
  api: {
    baseUrl: 'http://192.168.1.100:8000'  // Use different backend
  },
  visual: {
    particles: { count: 25 }  // Reduce particles for performance
  }
};
```

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python main.py
```

### Frontend Development
```bash
cd frontend
npm start
```

## NSFW Content Notice

This system is designed for adult interactions. Please ensure:
- Appropriate age verification
- Privacy-conscious deployment
- Responsible use of the platform

## What's New (v1.2.0)

### 📋 Centralized Frontend Configuration
- **Single Source of Truth**: All frontend parameters in one place
- **Local Overrides**: Create `config.local.js` for custom settings
- **Environment Aware**: Different settings for dev/production
- **Easy Customization**: Tweak animations, colors, performance
- **No More Hardcoding**: All values configurable

See [FRONTEND_CONFIG.md](docs/FRONTEND_CONFIG.md) for details.

### 🔊 Voice Synthesis Feature (v1.1.0)
- **Emotion-Aware Speech**: Voice changes based on waifu's emotions
- **Personality Voices**: Each waifu has unique voice characteristics
- **Visual Feedback**: Waveform visualization and speaking animations
- **User Controls**: Volume adjustment and on/off toggle
- **Browser Native**: Uses Web Speech API (no external dependencies)

See [VOICE_SYNTHESIS.md](docs/VOICE_SYNTHESIS.md) for details.

## Future Enhancements

- [x] Voice synthesis with emotion awareness
- [ ] Live2D integration for more advanced animations
- [ ] Advanced voice providers (ElevenLabs, Azure)
- [ ] Affection/progression system with unlockables
- [ ] Outfit/appearance customization
- [ ] State persistence (save conversations)
- [ ] Advanced physics simulation
- [ ] Multi-language support
- [ ] Custom model import system
- [ ] Gesture recognition
- [ ] VR/AR support

## License

Private use only. Not for redistribution.
