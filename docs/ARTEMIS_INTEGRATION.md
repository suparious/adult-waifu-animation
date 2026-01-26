# Artemis API Gateway Integration

Complete guide for deploying the Waifu Animation Chat with SolidRusT's Artemis API Gateway for production AI inference.

## Overview

Artemis is SolidRusT Networks' production AI gateway that provides:
- **Zero GPU requirement** - Hosted inference infrastructure
- **Automatic failover** - Seamless fallback to cloud providers
- **Usage tracking** - Integrated billing via PAM Platform
- **High availability** - Multi-tier redundancy
- **Cost efficiency** - Free self-hosted primary, paid cloud backup

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Waifu Animation Chat Backend                            │
│  ├─ FastAPI WebSocket server                            │
│  └─ LLM Client (OpenAI-compatible)                      │
└────────────────┬────────────────────────────────────────┘
                 │ HTTPS
                 │ X-API-Key: srt_prod_xxx
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Artemis API Gateway                                      │
│  https://artemis.hq.solidrust.net                       │
│  ├─ /v1/chat/completions (LiteLLM proxy)               │
│  ├─ /v1/embeddings (bge-m3)                             │
│  └─ PAM authentication middleware                       │
└────────────────┬────────────────────────────────────────┘
                 │ Intelligent routing
                 ▼
┌─────────────────────────────────────────────────────────┐
│ LiteLLM Failover Chain                                  │
│  ├─ Primary: vLLM (Qwen3-4B, self-hosted, FREE)        │
│  ├─ Secondary: OpenAI GPT-4o-mini ($0.15/1M tokens)    │
│  └─ Tertiary: Anthropic Haiku ($0.25/1M tokens)        │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **SolidRusT API Key**
   - Register at https://console.solidrust.ai
   - Navigate to API Keys section
   - Generate new key with `chat.completions` scope
   - Key format: `srt_prod_...` or `srt_test_...`

2. **Python Environment**
   - Python 3.11+ (see `PYTHON_VERSION_GUIDE.md`)
   - Backend dependencies installed (`pip install -r backend/requirements.txt`)

## Quick Start

### 1. Configure Environment

```bash
cd backend
cp .env.artemis .env
```

Edit `.env` and replace the placeholder API key:

```env
# LLM Configuration for Artemis API Gateway
LLM_PROVIDER=openai
LLM_API_URL=https://artemis.hq.solidrust.net/v1/chat/completions
LLM_MODEL=vllm-primary

# Your SolidRusT API Key (REQUIRED)
LLM_API_KEY=srt_prod_YOUR_ACTUAL_KEY_HERE

# LLM Parameters (optional, these are good defaults)
LLM_TEMPERATURE=0.85
LLM_MAX_TOKENS=200
LLM_TIMEOUT=30.0
```

### 2. Test Connection

```bash
# From backend directory
source venv/bin/activate  # or venv\Scripts\activate on Windows
python tests/test-vllm.py
```

Expected output:
```
Testing Artemis connection...
✓ Connection successful
✓ Model: vllm-primary
✓ Response latency: 1.2s
✓ Provider: openai (via Artemis)
```

### 3. Run the Application

```bash
# From project root
./run.sh
```

Or manually:
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

Access at http://localhost:3000

## Configuration Options

### Model Selection

Artemis provides multiple model aliases:

| Model Alias | Backend | Context | Speed | Cost |
|-------------|---------|---------|-------|------|
| `vllm-primary` | Qwen3-4B (self-hosted) | 32k | Fast | FREE |
| `gpt-4o-mini` | OpenAI GPT-4o-mini | 128k | Fast | $0.15/1M |
| `claude-haiku` | Anthropic Claude Haiku | 200k | Medium | $0.25/1M |

**Recommended:** Use `vllm-primary` for normal operation. LiteLLM automatically fails over to paid models if vLLM is unavailable.

### Temperature & Sampling

```env
# Conservative (more predictable)
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=150

# Balanced (default)
LLM_TEMPERATURE=0.85
LLM_MAX_TOKENS=200

# Creative (more varied responses)
LLM_TEMPERATURE=1.0
LLM_MAX_TOKENS=250
```

### Timeout Settings

```env
# Fast responses only (may fail on slow connections)
LLM_TIMEOUT=10.0

# Balanced (default)
LLM_TIMEOUT=30.0

# Patient (for long responses or slow networks)
LLM_TIMEOUT=60.0
```

## API Key Management

### Key Scopes

Ensure your API key has the following scopes:
- `chat.completions` (required) - For chat inference
- `embeddings` (optional) - For future RAG features

### Key Types

| Type | Prefix | Use Case |
|------|--------|----------|
| **Production** | `srt_prod_` | Public deployments, production apps |
| **Test** | `srt_test_` | Development, local testing |
| **Limited** | `srt_limit_` | Rate-limited free tier |

### Security Best Practices

1. **Never commit API keys** to git repositories
   - `.env` is already in `.gitignore`
   - Use environment variables in production

2. **Rotate keys regularly**
   - Generate new keys monthly
   - Revoke old keys at https://console.solidrust.ai

3. **Use separate keys per environment**
   - Development: `srt_test_dev_xxx`
   - Staging: `srt_test_staging_xxx`
   - Production: `srt_prod_xxx`

## Failover Behavior

### Automatic Failover

LiteLLM (on Artemis) automatically handles failures:

```
┌─────────────┐
│ Your Request│
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│ Try vLLM (self-hosted, free)                │
│  ├─ Success? Return response ✓              │
│  └─ Fail? Continue to next tier...          │
└──────┬──────────────────────────────────────┘
       │ Timeout or error
       ▼
┌─────────────────────────────────────────────┐
│ Try OpenAI GPT-4o-mini                      │
│  ├─ Success? Return response ✓              │
│  │   (Cost: $0.15/1M input tokens)          │
│  └─ Fail? Continue to next tier...          │
└──────┬──────────────────────────────────────┘
       │ Timeout or error
       ▼
┌─────────────────────────────────────────────┐
│ Try Anthropic Claude Haiku                  │
│  ├─ Success? Return response ✓              │
│  │   (Cost: $0.25/1M input tokens)          │
│  └─ Fail? Return error to client            │
└─────────────────────────────────────────────┘
```

### Failover Triggers

- **Timeout** - Response takes longer than configured timeout
- **500 errors** - Server errors from upstream provider
- **Rate limits** - Provider capacity exceeded
- **Model offline** - Scheduled maintenance or GPU issues

### Cost Implications

**Typical usage** (vLLM healthy):
- 100% free inference via self-hosted vLLM
- $0.00 monthly cost

**During vLLM downtime** (failover to OpenAI):
- Example: 1M tokens/month = $0.15
- Average conversation: ~500 tokens
- 2000 conversations = $0.15

**Best practice:** Monitor vLLM uptime at https://console.solidrust.ai to minimize cloud fallback costs.

## Troubleshooting

### Error: "Invalid API key"

**Cause:** API key is incorrect, expired, or missing required scopes.

**Solution:**
1. Verify key at https://console.solidrust.ai/keys
2. Check key has `chat.completions` scope
3. Ensure no extra spaces in `.env` file:
   ```env
   # Wrong (space before key)
   LLM_API_KEY= srt_prod_xxx
   
   # Correct
   LLM_API_KEY=srt_prod_xxx
   ```

### Error: "Connection timeout"

**Cause:** Network latency or Artemis temporarily unavailable.

**Solution:**
1. Check internet connectivity
2. Increase timeout in `.env`:
   ```env
   LLM_TIMEOUT=60.0
   ```
3. Check Artemis status at https://console.solidrust.ai/status

### Error: "Rate limit exceeded"

**Cause:** Too many requests for your API key tier.

**Solution:**
1. Wait 1 minute for rate limit reset
2. Implement client-side throttling
3. Upgrade to higher tier at https://console.solidrust.ai/billing

### Slow Response Times

**Cause:** Failover to slower cloud providers.

**Diagnosis:**
1. Check which provider responded:
   - Backend logs show: `"provider": "openai"` or `"provider": "anthropic"`
   - vLLM should respond in <2s
   - Cloud providers: 2-5s

**Solution:**
1. Check vLLM health: https://console.solidrust.ai/status
2. If vLLM is down, wait for restoration or accept cloud latency
3. Reduce `LLM_MAX_TOKENS` for faster responses:
   ```env
   LLM_MAX_TOKENS=150  # Faster but shorter responses
   ```

### Demo Fallback Responses

If LLM is completely unavailable, the backend returns demo responses:

```python
"*winks playfully* Even without my full power, I still find you interesting~"
```

**This means:**
- All API providers failed
- Check API key validity
- Check internet connectivity
- Verify Artemis is operational

## Migration from Local vLLM

If you're currently using a local vLLM instance:

### 1. Backup Current Config
```bash
cd backend
cp .env .env.local-backup
```

### 2. Switch to Artemis
```bash
cp .env.artemis .env
# Edit .env and add your API key
```

### 3. Test Both Configurations

**Local vLLM:**
```bash
cp .env.local-backup .env
python tests/test-vllm.py
```

**Artemis:**
```bash
cp .env.artemis .env
# Add API key
python tests/test-vllm.py
```

### 4. Compare Performance

| Metric | Local vLLM | Artemis |
|--------|------------|------|
| **Setup** | Complex (GPU, Docker) | Simple (API key) |
| **Latency** | <1s (local network) | 1-3s (internet) |
| **Availability** | Depends on local GPU | 99.9% (failover) |
| **Cost** | Electricity + hardware | Free (vLLM tier) |
| **Scaling** | Limited by GPU | Automatic |

## Production Deployment

### Environment Variables

For production deployments (Docker, K8s), use environment variables instead of `.env` files:

```yaml
# docker-compose.yml example
services:
  waifu-backend:
    image: waifu-animation-backend:latest
    environment:
      LLM_PROVIDER: openai
      LLM_API_URL: https://artemis.hq.solidrust.net/v1/chat/completions
      LLM_MODEL: vllm-primary
      LLM_API_KEY: ${SOLIDRUST_API_KEY}  # From secrets management
      LLM_TEMPERATURE: "0.85"
      LLM_MAX_TOKENS: "200"
      LLM_TIMEOUT: "30.0"
```

### Kubernetes Secrets

```yaml
# secret.yaml (use SealedSecrets or external secrets operator)
apiVersion: v1
kind: Secret
metadata:
  name: waifu-api-keys
type: Opaque
stringData:
  llm-api-key: srt_prod_YOUR_KEY_HERE

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: waifu-backend
spec:
  template:
    spec:
      containers:
      - name: backend
        env:
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: waifu-api-keys
              key: llm-api-key
        - name: LLM_PROVIDER
          value: "openai"
        - name: LLM_API_URL
          value: "https://artemis.hq.solidrust.net/v1/chat/completions"
```

## Health Monitoring

### Check LLM Connection

**Endpoint:** `GET /api/system-info`

```bash
curl http://localhost:8000/api/system-info
```

**Response:**
```json
{
  "version": "1.1.0-beta",
  "llm": {
    "provider": "OPENAI",
    "model": "vllm-primary",
    "model_display": "Qwen3-4B",
    "api_url": "https://artemis.hq.solidrust.net",
    "temperature": 0.85,
    "max_tokens": 200
  },
  "features": {
    "voice_synthesis": true,
    "advanced_physics": true,
    "max_affection_level": 100
  }
}
```

### Test Inference

```bash
python tests/test-vllm.py
```

### Monitor Usage

Track API usage at https://console.solidrust.ai/usage:
- Requests per day
- Tokens consumed
- Estimated costs (cloud failover)
- Provider distribution (vLLM vs. cloud)

## Benefits Summary

### For Development
- **Zero setup** - No GPU configuration required
- **Fast iteration** - No model loading wait times
- **Consistent** - Same API for all developers

### For Production
- **High availability** - Automatic failover to cloud providers
- **Cost efficient** - Free tier for self-hosted, minimal cloud costs
- **Scalable** - No GPU capacity planning
- **Observable** - Usage tracking and monitoring built-in

### For Users
- **Fast responses** - <2s typical latency
- **Reliable** - Multi-tier redundancy
- **Quality** - Best-in-class models (Qwen3, GPT-4o, Claude)

## Related Documentation

- **PAM API Keys:** https://console.solidrust.ai/docs/api-keys
- **Artemis API Reference:** https://artemis.hq.solidrust.net/docs
- **LiteLLM Proxy:** https://docs.litellm.ai/docs/proxy/
- **Model Comparison:** `docs/LLM_CONFIG_UPDATE.md`

## Support

- **Issues:** https://github.com/suparious/adult-waifu-animation/issues
- **SolidRusT Support:** support@solidrust.net
- **API Status:** https://console.solidrust.ai/status

## Next Steps

1. **Get API Key:** https://console.solidrust.ai
2. **Configure Backend:** Copy `.env.artemis` to `.env`
3. **Test Connection:** Run `python tests/test-vllm.py`
4. **Deploy:** See issue #5 for Kubernetes deployment

---

**Version:** 1.0  
**Last Updated:** 2026-01-26  
**Related Issues:** #1 (Artemis Integration), #5 (K8s Deployment)
