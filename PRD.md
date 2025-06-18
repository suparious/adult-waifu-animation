# Waifu Animation Chat - Product Requirements Document & Development Prompt

## Project Overview

You are tasked with continuing development on an interactive waifu animation chat system. This is a web-based application that combines AI-powered chat with procedurally animated anime-style characters (waifus) for an immersive, adult-oriented conversational experience.

## Current Implementation Status

### Working Features ✅
1. **Full-stack Web Application**
   - Backend: FastAPI (Python 3.11) with WebSocket support
   - Frontend: React with Three.js for 3D animations
   - Real-time bidirectional communication

2. **AI Integration**
   - vLLM API integration for chat responses
   - Personality-based prompting system
   - Emotion detection from conversation context
   - Chat history maintenance

3. **Waifu System**
   - Two default personas: Luna (flirty cyberpunk) and Sakura (shy bookworm)
   - Image loading from `frontend/public/models/`
   - Basic procedural animation (breathing, swaying, emotion-based movement)
   - Model switching in UI

4. **Animation Engine**
   - Three.js-based 3D scene
   - Texture mapping of static images onto animated mesh
   - Emotion-driven animation states
   - Particle effects for ambiance

### Technical Stack
- **Python**: 3.11 (managed with pyenv)
- **Backend**: FastAPI, uvicorn, httpx, pydantic, numpy
- **Frontend**: React 18, Three.js, @react-three/fiber, styled-components, framer-motion
- **Package Manager**: yarn (frontend), pip with venv (backend)
- **AI**: vLLM or OpenAI-compatible API

### Project Structure
```
adult-waifu-animation/
├── backend/
│   ├── main.py              # FastAPI server with WebSocket
│   ├── animation_engine.py  # Procedural animation system
│   ├── waifu_manager.py     # Model/persona management
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React app
│   │   └── components/
│   │       ├── WaifuCanvas.js    # Three.js animation
│   │       ├── ChatInterface.js  # Chat UI
│   │       └── ModelSelector.js  # Waifu switcher
│   └── public/models/       # Waifu images go here
└── models/                  # Configuration files
```

## Features Needing Implementation 🚧

### 1. Advanced Animation System
- **Live2D Integration**: Replace simple mesh deformation with Live2D SDK for professional VTuber-quality animation
- **Skeletal Rigging**: Implement proper bone system for more natural movement
- **Facial Expressions**: Eye tracking, blinking, mouth movement for talking
- **Lip Sync**: Match mouth movement to AI speech or text
- **Physics Simulation**: Realistic hair and clothing physics

### 2. Enhanced Interaction
- **Voice Synthesis**: Integrate Web Speech API or ElevenLabs for voice output
- **Voice Input**: Speech-to-text for hands-free chat
- **Gesture Recognition**: Webcam-based user tracking for interactive responses
- **Touch/Click Interactions**: Click on waifu for reactions

### 3. Progression System
- **Affection Levels**: Track relationship progress (0-100)
- **Unlockable Content**: New animations, outfits, dialogue options
- **Memory System**: Waifus remember past conversations
- **Gift System**: Virtual gifts affect affection

### 4. Content & Customization
- **Multiple Outfits**: Changeable clothing system
- **Custom Waifu Creator**: User-uploaded images with auto-rigging
- **Personality Editor**: GUI for creating custom personas
- **Scene Backgrounds**: Different environments

### 5. NSFW Features
- **Progressive Intimacy**: Content scales with affection level
- **Private Mode**: Enhanced privacy features
- **Age Verification**: Proper adult content gating
- **Content Filters**: User-adjustable NSFW levels

### 6. Technical Improvements
- **State Persistence**: Save conversations and progress
- **Performance Optimization**: GPU acceleration, LOD system
- **Mobile Support**: Responsive design and touch controls
- **Deployment**: Docker containers, cloud hosting ready

## Development Guidelines

### Code Standards
- Type hints in Python
- PropTypes or TypeScript for React
- Comprehensive error handling
- WebSocket reconnection logic
- Modular, extensible architecture

### Animation Principles
- 60 FPS target for smooth animation
- Ease-in/ease-out for natural movement
- Layered animation system (base + emotion + idle)
- Performance monitoring

### AI Integration Best Practices
- Prompt engineering for consistent personality
- Token limit management
- Response streaming for better UX
- Fallback responses for API failures

## Setup Instructions for New Developers

1. **Requirements**
   - Python 3.11 (via pyenv recommended)
   - Node.js 16+
   - vLLM instance or OpenAI API key

2. **Quick Start**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   # Configure backend/.env with vLLM endpoint
   # Add waifu images to frontend/public/models/
   ./run.sh
   ```

3. **Testing**
   ```bash
   ./test-vllm.py      # Test AI connection
   ./check-system.sh   # Verify system status
   ```

## Key Decisions & Constraints

1. **Why Three.js over Live2D**: Started with Three.js for rapid prototyping, but Live2D is the eventual goal
2. **Static Images**: Currently using static PNG/JPG with procedural animation rather than pre-rigged models
3. **Python 3.11**: Best compatibility with current dependencies
4. **Yarn over npm**: Resolves dependency conflicts in React ecosystem

## Future Architecture Considerations

1. **Microservices**: Separate animation, chat, and AI services
2. **WebRTC**: For voice/video features
3. **Redis**: For session management and caching
4. **CDN**: For model/asset delivery
5. **Analytics**: User interaction tracking (privacy-conscious)

## Success Metrics

- Smooth 60 FPS animation
- <200ms chat response time
- Natural, personality-consistent dialogue
- Engaging progression system
- High user retention

## Current Limitations

1. Animation is basic mesh deformation, not true character animation
2. No voice synthesis yet
3. No state persistence between sessions
4. Limited to 2 default waifus
5. No mobile optimization

## Next Sprint Priorities

1. Implement basic Live2D or improve skeletal animation
2. Add voice synthesis
3. Create outfit system
4. Implement affection/progression system
5. Add more waifu personas

---

**Note for AI Assistant**: This is an adult-oriented project. Maintain professionalism while implementing features appropriate for the target audience. Focus on creating an engaging, interactive experience with high-quality animation and believable AI personalities.

**Repository**: Located at `/home/shaun/scratch-space/adult-waifu-animation/`
