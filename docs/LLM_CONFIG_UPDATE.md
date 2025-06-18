# LLM Configuration Update

I've updated the waifu chat system to support multiple LLM providers and make testing much easier!

## What's New

### 1. **Multi-Provider Support**
The system now supports:
- **vLLM** (your current setup)
- **Ollama** (for local models)
- **OpenAI** (GPT-3.5/GPT-4)
- **Custom** (any OpenAI-compatible API)

### 2. **Dynamic Configuration Reloading**
- Edit `backend/.env` and the changes take effect immediately
- No need to restart the backend server
- The system reloads config on each request

### 3. **New Test Tool**
Run `./test-llm.py` to:
- Test your LLM connection
- Verify waifu personalities work
- Check response times
- Interactive chat mode for testing

### 4. **Better Process Management**
- `./run.sh` now kills existing processes before starting
- Cleaner restarts without port conflicts

## Quick Start

### To Switch LLM Providers:

1. **For vLLM** (current):
   ```bash
   # Already configured in backend/.env
   LLM_PROVIDER=vllm
   LLM_API_URL=http://kratos:8081/v1/completions
   ```

2. **For Ollama**:
   ```bash
   # Copy example config
   cp llm-configs/.env.ollama backend/.env
   # Edit to set your model
   # Make sure Ollama is running: ollama serve
   ```

3. **For OpenAI**:
   ```bash
   # Copy example config
   cp llm-configs/.env.openai backend/.env
   # Add your API key
   ```

### Testing Your LLM:

```bash
# Test current configuration
./test-llm.py

# This will:
# - Show current config
# - Test basic connection
# - Test both waifu personalities
# - Measure response time
# - Offer interactive testing
```

### Troubleshooting:

If you're still seeing requests go to the old endpoint:

1. **Stop everything**: `Ctrl+C` in the terminal running `./run.sh`
2. **Edit** `backend/.env` with your desired config
3. **Restart**: `./run.sh`
4. **Test**: `./test-llm.py`

The system will now use your new LLM endpoint!

## Example Configurations

Check the `llm-configs/` directory for example `.env` files for each provider.

## Next Steps

Once your LLM is working properly, we can implement the voice synthesis feature to make your waifus speak! 🎤
