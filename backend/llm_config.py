"""
LLM Configuration and Provider Management
Supports vLLM, Ollama, OpenAI, and other compatible APIs
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import httpx
import json
from pathlib import Path

class LLMProvider(Enum):
    VLLM = "vllm"
    OLLAMA = "ollama"
    OPENAI = "openai"
    CUSTOM = "custom"

@dataclass
class LLMConfig:
    provider: LLMProvider
    api_url: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.85
    max_tokens: int = 200
    timeout: float = 30.0
    
    @classmethod
    def from_env(cls) -> 'LLMConfig':
        """Load configuration from environment variables"""
        provider = os.getenv("LLM_PROVIDER", "vllm").lower()
        
        # Map provider string to enum
        provider_map = {
            "vllm": LLMProvider.VLLM,
            "ollama": LLMProvider.OLLAMA,
            "openai": LLMProvider.OPENAI,
            "custom": LLMProvider.CUSTOM
        }
        
        return cls(
            provider=provider_map.get(provider, LLMProvider.VLLM),
            api_url=os.getenv("LLM_API_URL", "http://localhost:8001/v1/completions"),
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("LLM_MODEL"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.85")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "200")),
            timeout=float(os.getenv("LLM_TIMEOUT", "30.0"))
        )
    
    @classmethod
    def from_file(cls, config_path: Path) -> 'LLMConfig':
        """Load configuration from a JSON file"""
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        provider = config.get("provider", "vllm").lower()
        provider_map = {
            "vllm": LLMProvider.VLLM,
            "ollama": LLMProvider.OLLAMA,
            "openai": LLMProvider.OPENAI,
            "custom": LLMProvider.CUSTOM
        }
        
        return cls(
            provider=provider_map.get(provider, LLMProvider.VLLM),
            api_url=config["api_url"],
            api_key=config.get("api_key"),
            model=config.get("model"),
            temperature=config.get("temperature", 0.85),
            max_tokens=config.get("max_tokens", 200),
            timeout=config.get("timeout", 30.0)
        )

class LLMClient:
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.from_env()
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
    
    async def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        """Generate a response from the LLM"""
        if self.config.provider == LLMProvider.OLLAMA:
            return await self._generate_ollama(prompt, system_prompt, **kwargs)
        elif self.config.provider == LLMProvider.OPENAI:
            return await self._generate_openai(prompt, system_prompt, **kwargs)
        else:  # vLLM or custom
            return await self._generate_vllm(prompt, system_prompt, **kwargs)
    
    async def _generate_vllm(self, prompt: str, system_prompt: str, **kwargs) -> str:
        """Generate using vLLM or compatible API"""
        # Build full prompt
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        # Prepare request
        headers = {}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        
        payload = {
            "prompt": full_prompt,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", 0.9),
            "stop": kwargs.get("stop", ["\nUser:", "\nHuman:", "\n\n"]),
            "presence_penalty": kwargs.get("presence_penalty", 0.6),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.3)
        }
        
        if self.config.model:
            payload["model"] = self.config.model
        
        response = await self._client.post(
            self.config.api_url,
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["text"].strip()
        else:
            raise Exception(f"vLLM API error: {response.status_code} - {response.text}")
    
    async def _generate_ollama(self, prompt: str, system_prompt: str, **kwargs) -> str:
        """Generate using Ollama API"""
        # Ollama uses a different API format
        api_url = self.config.api_url
        if not api_url.endswith("/api/generate"):
            # Adjust URL for Ollama format
            base_url = api_url.replace("/v1/completions", "").rstrip("/")
            api_url = f"{base_url}/api/generate"
        
        payload = {
            "model": self.config.model or "llama2",
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
                "stop": kwargs.get("stop", ["\nUser:", "\nHuman:"])
            }
        }
        
        response = await self._client.post(api_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result["response"].strip()
        else:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
    
    async def _generate_openai(self, prompt: str, system_prompt: str, **kwargs) -> str:
        """Generate using OpenAI API or Artemis (OpenAI-compatible)"""
        headers = {
            "Content-Type": "application/json"
        }
        if self.config.api_key:
            # Standard OpenAI Authorization header
            headers["Authorization"] = f"Bearer {self.config.api_key}"
            # Artemis uses X-API-Key for authentication
            headers["X-API-Key"] = self.config.api_key
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.config.model or "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "presence_penalty": kwargs.get("presence_penalty", 0.6),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.3)
        }
        
        response = await self._client.post(
            self.config.api_url,
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test the LLM connection and return status"""
        try:
            response = await self.generate(
                "Say 'Hello, I'm working!' in exactly those words.",
                "You are a helpful assistant that follows instructions exactly."
            )
            
            return {
                "status": "success",
                "provider": self.config.provider.value,
                "api_url": self.config.api_url,
                "model": self.config.model,
                "response": response,
                "working": "Hello, I'm working!" in response
            }
        except Exception as e:
            return {
                "status": "error",
                "provider": self.config.provider.value,
                "api_url": self.config.api_url,
                "model": self.config.model,
                "error": str(e),
                "working": False
            }

# Global config instance that can be reloaded
_current_config: Optional[LLMConfig] = None

def get_llm_config() -> LLMConfig:
    """Get current LLM configuration, loading from env if needed"""
    global _current_config
    if _current_config is None:
        reload_config()
    return _current_config

def reload_config():
    """Reload configuration from environment or file"""
    global _current_config
    
    # Check if there's a config file
    config_file = Path(__file__).parent / "llm_config.json"
    if config_file.exists():
        _current_config = LLMConfig.from_file(config_file)
    else:
        _current_config = LLMConfig.from_env()
    
    return _current_config

def set_config(config: LLMConfig):
    """Set configuration programmatically"""
    global _current_config
    _current_config = config
