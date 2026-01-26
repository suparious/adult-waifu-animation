# adult-waifu-animation

## Project Role
Interactive VTuber-style animated chat application with AI-powered conversations,
emotion-based animations, and relationship progression.

**Personal Project**: This is a fun personal project exploring Three.js, WebSockets, and AI integration.

---

## Architecture

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + WebSocket | Chat server, emotion detection, state management |
| **Frontend** | React + Three.js | 3D rendering, animations, real-time chat UI |
| **AI** | OpenAI-compatible API | Character responses via Artemis/vLLM/LiteLLM |
| **TTS** | Browser Web Speech API | Voice synthesis (upgradeable to ElevenLabs) |
| **Storage** | SQLite | Affection/progression persistence |

---

## SolidRusT Integration Status

| Feature | Status | Issue | Notes |
|---------|--------|-------|-------|
| LLM via Artemis | ✅ Ready | #1 | X-API-Key header added, use `.env.artemis` |
| PAM Auth | ❌ Not Started | #2 | Future: API key from PAM |
| K8s Deployment | ❌ Not Started | #5 | Future: Kustomize manifests |
| Persistent Storage | ❌ Not Started | #6 | Future: PostgreSQL migration |
| Conversation Memory | ❌ Not Started | #7 | Future: Embeddings via data-layer |

---

## Key Files

### Backend
| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI WebSocket server, main entry point |
| `backend/llm_config.py` | Multi-provider LLM abstraction (vLLM, Ollama, OpenAI/Artemis) |
| `backend/affection_manager.py` | Relationship progression and state persistence |
| `backend/emotion_detector.py` | Analyzes text for emotion keywords |
| `backend/models.py` | Waifu persona definitions |

### Frontend
| File | Purpose |
|------|---------|
| `frontend/src/config.js` | Centralized configuration |
| `frontend/src/components/WaifuCanvas.js` | Three.js 3D rendering |
| `frontend/src/components/ChatInterface.js` | Chat UI and WebSocket handling |
| `frontend/src/hooks/useWebSocket.js` | WebSocket connection hook |

### Configuration
| File | Purpose |
|------|---------|
| `backend/.env.artemis` | Artemis API configuration (recommended) |
| `backend/.env.vllm` | Direct vLLM configuration |
| `backend/.env.ollama` | Ollama local configuration |
| `backend/.env.openai` | OpenAI API configuration |

---

## Development Setup

```bash
# Clone and setup
cd /Users/shaun/repos/adult-waifu-animation
chmod +x *.sh
./setup.sh

# Configure for Artemis (SolidRusT production)
cp backend/.env.artemis backend/.env
# Edit backend/.env with your API key from console.solidrust.ai

# Run
./run.sh
```

**URLs:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- WebSocket: ws://localhost:8000/ws/{client_id}

---

## Environment Variables

### Artemis Configuration (Recommended)
```bash
LLM_PROVIDER=openai
LLM_API_URL=https://artemis.hq.solidrust.net/v1/chat/completions
LLM_API_KEY=srt_prod_xxx  # Get from https://console.solidrust.ai
LLM_MODEL=vllm-primary
```

### Parameters
| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | vllm | Provider: vllm, ollama, openai |
| `LLM_API_URL` | localhost:8001 | API endpoint |
| `LLM_API_KEY` | none | API key (required for Artemis/OpenAI) |
| `LLM_MODEL` | none | Model name |
| `LLM_TEMPERATURE` | 0.85 | Response creativity (0.0-1.0) |
| `LLM_MAX_TOKENS` | 200 | Max response length |
| `LLM_TIMEOUT` | 30.0 | Request timeout in seconds |
| `ENABLE_VOICE_SYNTHESIS` | false | Enable browser TTS |
| `ENABLE_ADVANCED_PHYSICS` | true | Enable physics simulation |
| `MAX_AFFECTION_LEVEL` | 100 | Max affection points |

---

## Common Tasks

### Run Application
```bash
./run.sh              # Start both backend and frontend
./run-backend.sh      # Backend only (port 8000)
./run-frontend.sh     # Frontend only (port 3000)
```

### Test LLM Connection
```bash
cd backend
source venv/bin/activate
python -c "
import asyncio
from llm_config import LLMClient
async def test():
    async with LLMClient() as client:
        result = await client.test_connection()
        print(result)
asyncio.run(test())
"
```

### Add New Waifu
1. Add image to `frontend/public/models/name.png` (1024x2048 portrait PNG)
2. Add persona definition in `backend/models.py`
3. Restart backend

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/models` | List available waifu models |
| GET | `/api/models/{id}` | Get specific model details |
| GET | `/api/affection/{model_id}` | Get affection level |
| POST | `/api/affection/{model_id}` | Update affection |
| WS | `/ws/{client_id}` | Real-time chat connection |

---

## Affection System

Progressive relationship system that unlocks content:

| Level | Range | Unlocks |
|-------|-------|---------|
| Stranger | 0-15 | Basic interactions |
| Acquaintance | 16-35 | Friendly dialogue |
| Friend | 36-55 | Casual animations |
| Close Friend | 56-75 | Personal conversations |
| Romantic | 76-90 | Intimate interactions |
| Soulmate | 91-100 | All content unlocked |

See `docs/AFFECTION_SYSTEM.md` for details.

---

## Emotion Detection

The system detects emotions from text and triggers corresponding animations:

| Emotion | Triggers | Animation |
|---------|----------|-----------|
| happy | love, happy, joy | Cheerful bounce |
| shy | embarrass, blush | Look away, fidget |
| flirty | sexy, hot, kiss | Wink, playful |
| angry | angry, mad, hate | Frustrated gestures |
| sad | sad, lonely, miss | Downcast, slow |
| excited | wow, amazing | Energetic bounce |

---

## Future Phases

### Phase 2: Containerization
- Dockerfile for backend (Python 3.11)
- Dockerfile for frontend (Node.js build → nginx)
- docker-compose.yml for local testing

### Phase 3: K8s Deployment
- Kustomize manifests in srt-hq-k8s
- HTTPRoute for Gateway API
- SealedSecret for API keys

### Phase 4: Enhanced Features
- ElevenLabs/Azure TTS (Issue #3)
- Image generation for outfits (Issue #4)
- PostgreSQL for persistence (Issue #6)
- Embeddings for memory (Issue #7)

---

## Troubleshooting

### LLM Not Responding
1. Check backend logs for connection errors
2. Verify API key is set in `.env`
3. Test endpoint: `curl https://artemis.hq.solidrust.net/health`
4. Check model name matches LiteLLM alias (`vllm-primary`)

### WebSocket Disconnects
1. Check browser console for errors
2. Verify backend is running on port 8000
3. Check CORS settings in `.env`

### Animations Not Loading
1. Verify images exist in `frontend/public/models/`
2. Check image format (PNG, 1024x2048)
3. Clear browser cache

See `docs/TROUBLESHOOTING.md` for more.

---

## Related Documentation

| Doc | Purpose |
|-----|---------|
| `docs/AFFECTION_SYSTEM.md` | Relationship progression details |
| `docs/VOICE_SYNTHESIS.md` | TTS implementation |
| `docs/FRONTEND_CONFIG.md` | Frontend configuration guide |
| `docs/IMAGE_SETUP_GUIDE.md` | Waifu image requirements |
| `docs/LLM_CONFIG_UPDATE.md` | LLM provider setup |

---

**Version**: 1.0 | **Updated**: January 2026
