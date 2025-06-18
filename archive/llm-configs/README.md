# Example LLM Configurations for Waifu Chat

This directory contains example configurations for different LLM providers.
Copy the one you want to use to `backend/.env` and modify as needed.

## Quick Setup

1. Choose your LLM provider
2. Copy the appropriate `.env.example` file to `backend/.env`
3. Update the configuration with your specific endpoints and models
4. Run `./test-llm.py` to verify the connection

## Supported Providers

- **vLLM**: High-performance inference server
- **Ollama**: Local model hosting
- **OpenAI**: Cloud-based GPT models
- **Custom**: Any OpenAI-compatible API

## Testing Different Endpoints

To quickly test different LLMs without restarting:

1. Edit `backend/.env` with new settings
2. The backend will automatically reload the configuration
3. Use `./test-llm.py` to verify the new endpoint works

## Troubleshooting

If your LLM isn't responding:

1. Check that the LLM server is running
2. Verify the API URL is correct
3. Ensure any required API keys are set
4. Run `./test-llm.py` for detailed diagnostics
