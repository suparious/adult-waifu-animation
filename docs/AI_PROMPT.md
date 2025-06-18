# AI Development Prompt - Waifu Animation Chat

Copy and paste this prompt to start a new conversation for continued development:

---

I have a working prototype of an interactive waifu animation chat system that needs further development. The project is located at `/home/shaun/scratch-space/adult-waifu-animation/`.

## Current State:
- **Working**: Basic chat with vLLM integration, procedural animation of static images, two waifu personas (Luna & Sakura)
- **Tech Stack**: FastAPI + React/Three.js, Python 3.11, uses yarn for frontend
- **Features**: Emotion-based animations, personality-driven chat, model switching

## What I Need:
I want to implement the next phase of features. Please:
1. First run `ls -la /home/shaun/scratch-space/adult-waifu-animation/` to see the project
2. Read the `PRD.md` file for full context and requirements
3. Check `TROUBLESHOOTING.md` for known issues
4. Review the current code structure

## Priority Features to Add:
1. Better animation system (considering Live2D integration)
2. Voice synthesis for waifu responses  
3. Affection/progression system
4. Outfit/appearance customization
5. State persistence between sessions

## Important Context:
- This is an adult-oriented (NSFW) application
- The app currently works but needs more sophisticated features
- I have vLLM running on erebus:8081
- Images go in `frontend/public/models/` as PNG/JPG files
- Use Python 3.11 (not 3.12+) for compatibility

Please analyze the current implementation and suggest which feature we should tackle first for maximum impact.

---

## Additional Files to Reference:
- `IMAGE_SETUP_GUIDE.md` - How to add waifu images
- `INTEGRATION_GUIDE.md` - vLLM and customization details  
- `backend/animation_engine.py` - Current animation system
- `backend/waifu_manager.py` - Persona management system

The goal is to evolve this from a working prototype into a polished, engaging waifu interaction platform with professional-quality animations and immersive features.
