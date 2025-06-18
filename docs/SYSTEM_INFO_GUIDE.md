# System Info Display Feature

## Overview
The waifu chat now displays the current LLM configuration and version information in the UI header, making it easy to see which model you're using at a glance.

## What's Displayed

The system info appears under the main title and shows:
- **Provider**: The LLM provider (OPENAI, VLLM, OLLAMA, etc.)
- **Model**: A user-friendly model name
- **Version**: The application version

Example: `🤖 OPENAI • GPT-4.1 Mini • v1.0.0-beta`

## Configuration

### Application Version
Edit the version in `backend/main.py`:
```python
APP_VERSION = "1.0.0-beta"  # Change this to update version
```

### LLM Configuration
The system automatically detects your LLM settings from the `.env` file:

```env
# Provider options: vllm, ollama, openai, custom
LLM_PROVIDER=openai
LLM_MODEL=gpt-4.1-mini
LLM_API_URL=https://api.openai.com/v1/chat/completions
```

## Model Name Display

The system intelligently formats model names:

### OpenAI Models
- `gpt-4.1-mini` → "GPT-4.1 Mini"
- `gpt-4-turbo` → "GPT-4 Turbo"
- `o1-mini` → "O1 Mini"

### vLLM/HuggingFace Models
- `solidrust/dolphin-2.9.2-qwen2-7b-AWQ` → "Dolphin 2.9.2"
- `meta-llama/Llama-2-7b-chat-hf` → "LLaMA 2"
- `mistralai/Mistral-7B-v0.1` → "Mistral 7B"

### Ollama Models
- `CognitiveComputations/dolphin-mistral:latest` → "Dolphin Mistral"
- `llama2:13b` → "Llama2"

## Testing

Run the test script to verify the system info endpoint:
```bash
./test-system-info.py
```

This will show you exactly what information is being returned by the backend.

## Troubleshooting

### System info not showing?
1. Check that the backend is running
2. Verify the `/api/system-info` endpoint works using the test script
3. Check browser console for errors
4. Ensure CORS is properly configured

### Wrong model name displayed?
1. Check your `.env` file configuration
2. Restart the backend after changes: `./run-backend.sh`
3. The frontend updates every 60 seconds, or refresh the page

### Custom model names
To add custom model name mappings, edit the `get_system_info()` function in `backend/main.py`.

## API Endpoint

The system info is available at:
```
GET http://localhost:8000/api/system-info
```

Response format:
```json
{
  "version": "1.0.0-beta",
  "llm": {
    "provider": "OPENAI",
    "model": "gpt-4.1-mini",
    "model_display": "GPT-4.1 Mini",
    "api_url": "https://api.openai.com",
    "temperature": 0.7,
    "max_tokens": 8192
  },
  "features": {
    "voice_synthesis": false,
    "advanced_physics": true,
    "max_affection_level": 100
  },
  "timestamp": "2024-01-01T12:00:00.000000"
}
```
