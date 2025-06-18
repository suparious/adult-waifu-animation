#!/usr/bin/env python3
"""
Test vLLM Connection
Verifies that your vLLM API is properly configured and accessible
"""

import asyncio
import httpx
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / "backend" / ".env"
load_dotenv(env_path)

async def test_vllm_connection():
    """Test the vLLM API connection"""
    
    # Get configuration
    vllm_url = os.getenv("VLLM_API_URL", "")
    vllm_key = os.getenv("VLLM_API_KEY", "")
    vllm_model = os.getenv("VLLM_MODEL", "")
    
    print("🔍 vLLM Connection Test")
    print("=" * 50)
    print(f"URL: {vllm_url}")
    print(f"Model: {vllm_model if vllm_model else 'Not specified'}")
    print(f"API Key: {'Configured' if vllm_key and vllm_key != 'your-api-key-here' else 'Not configured'}")
    print("=" * 50)
    
    if not vllm_url or vllm_url == "http://localhost:8001/v1/completions":
        print("❌ Error: vLLM URL not configured!")
        print("Please edit backend/.env and set VLLM_API_URL to your actual endpoint")
        return False
    
    # Test prompt
    test_prompt = "Hello! Please respond with a friendly greeting."
    
    try:
        print("\n📡 Testing connection...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {}
            if vllm_key and vllm_key != "your-api-key-here":
                headers["Authorization"] = f"Bearer {vllm_key}"
            
            payload = {
                "prompt": f"You are a friendly assistant.\n\nUser: {test_prompt}\nAssistant: ",
                "max_tokens": 50,
                "temperature": 0.7,
                "stop": ["\nUser:", "\n\n"]
            }
            
            if vllm_model:
                payload["model"] = vllm_model
            
            response = await client.post(vllm_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    ai_response = result["choices"][0]["text"].strip()
                    print("✅ Success! vLLM is working properly")
                    print(f"\n🤖 AI Response: {ai_response}")
                    return True
                else:
                    print("❌ Error: Unexpected response format")
                    print(f"Response: {result}")
                    return False
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                return False
                
    except httpx.ConnectError:
        print("❌ Error: Could not connect to vLLM server")
        print(f"Make sure vLLM is running at: {vllm_url}")
        return False
    except httpx.TimeoutException:
        print("❌ Error: Request timed out")
        print("The vLLM server might be overloaded or unreachable")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False

async def test_waifu_personality():
    """Test a waifu personality prompt"""
    
    vllm_url = os.getenv("VLLM_API_URL", "")
    vllm_key = os.getenv("VLLM_API_KEY", "")
    vllm_model = os.getenv("VLLM_MODEL", "")
    
    if not vllm_url or vllm_url == "http://localhost:8001/v1/completions":
        return
    
    print("\n\n🎭 Testing Waifu Personality...")
    print("=" * 50)
    
    personality = """You are Luna, a playful and flirty cyberpunk girl from Neo-Tokyo. You love teasing people and making them blush. Express emotions through actions in *asterisks* and use casual, flirty language."""
    
    test_prompt = "Hi Luna! How are you today?"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {}
            if vllm_key and vllm_key != "your-api-key-here":
                headers["Authorization"] = f"Bearer {vllm_key}"
            
            payload = {
                "prompt": f"{personality}\n\nUser: {test_prompt}\nAssistant: ",
                "max_tokens": 150,
                "temperature": 0.85,
                "stop": ["\nUser:", "\n\n"],
                "presence_penalty": 0.6,
                "frequency_penalty": 0.3
            }
            
            if vllm_model:
                payload["model"] = vllm_model
            
            response = await client.post(vllm_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    ai_response = result["choices"][0]["text"].strip()
                    print("✅ Personality test successful!")
                    print(f"\n🎀 Luna says: {ai_response}")
                    
                    # Check if response has personality markers
                    if "*" in ai_response:
                        print("\n✨ Good! Response includes emotion actions")
                    else:
                        print("\n⚠️  Tip: Response lacks emotion actions (*asterisks*)")
                        print("You may need to adjust your model or prompting")
                        
    except Exception as e:
        print(f"❌ Personality test failed: {e}")

def main():
    """Run all tests"""
    print("\n🎀 Waifu Animation Chat - vLLM Test Utility\n")
    
    # Check if .env exists
    if not env_path.exists():
        print("❌ Error: backend/.env file not found!")
        print("Please run ./setup.sh first")
        sys.exit(1)
    
    # Run tests
    loop = asyncio.get_event_loop()
    
    # Test basic connection
    success = loop.run_until_complete(test_vllm_connection())
    
    # If basic test passed, test personality
    if success:
        loop.run_until_complete(test_waifu_personality())
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Your vLLM is ready for waifu chat!")
        print("\nNext steps:")
        print("1. Your waifu images are already in place!")
        print("2. Visit http://localhost:3000")
        print("3. Start chatting with Luna or Sakura!")
    else:
        print("❌ Tests failed. Please check your vLLM configuration.")
        print("\nTroubleshooting:")
        print("1. Verify vLLM is running on erebus:8081")
        print("2. Check if the model name is correct")
        print("3. Ensure any API keys are properly set")
        print("4. Check vLLM server logs for errors")

if __name__ == "__main__":
    main()
