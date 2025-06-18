#!/usr/bin/env python3
"""
Test LLM endpoints for the Waifu Animation Chat
Supports testing vLLM, Ollama, and OpenAI compatible endpoints
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from llm_config import LLMClient, LLMConfig, LLMProvider

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

def print_config(config: LLMConfig):
    """Print current configuration"""
    print(f"{Colors.OKCYAN}Current Configuration:{Colors.ENDC}")
    print(f"  Provider: {Colors.BOLD}{config.provider.value}{Colors.ENDC}")
    print(f"  API URL: {Colors.BOLD}{config.api_url}{Colors.ENDC}")
    print(f"  Model: {Colors.BOLD}{config.model or 'default'}{Colors.ENDC}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    print(f"  Timeout: {config.timeout}s")
    print(f"  API Key: {'*' * 10 if config.api_key else 'Not set'}")
    print()

async def test_basic_connection(config: LLMConfig):
    """Test basic LLM connection"""
    print(f"{Colors.OKBLUE}Testing basic connection...{Colors.ENDC}")
    
    async with LLMClient(config) as llm:
        result = await llm.test_connection()
        
        if result["working"]:
            print(f"{Colors.OKGREEN}✓ Connection successful!{Colors.ENDC}")
            print(f"  Response: {result['response']}")
        else:
            print(f"{Colors.FAIL}✗ Connection failed!{Colors.ENDC}")
            if "error" in result:
                print(f"  Error: {result['error']}")
        
        return result["working"]

async def test_waifu_personality(config: LLMConfig, personality: str, name: str):
    """Test a waifu personality response"""
    print(f"\n{Colors.OKBLUE}Testing {name} personality...{Colors.ENDC}")
    
    prompt = "Hello! How are you feeling today?"
    
    async with LLMClient(config) as llm:
        try:
            response = await llm.generate(
                prompt=f"User: {prompt}\nAssistant: ",
                system_prompt=f"You are {personality}"
            )
            
            print(f"{Colors.OKGREEN}✓ {name} response:{Colors.ENDC}")
            print(f"  {response}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}✗ Failed to get response:{Colors.ENDC}")
            print(f"  Error: {e}")
            return False

async def test_response_time(config: LLMConfig):
    """Test response time"""
    print(f"\n{Colors.OKBLUE}Testing response time...{Colors.ENDC}")
    
    async with LLMClient(config) as llm:
        try:
            start_time = datetime.now()
            response = await llm.generate(
                prompt="Say hello quickly!",
                system_prompt="You are a helpful assistant.",
                max_tokens=50
            )
            end_time = datetime.now()
            
            duration = (end_time - start_time).total_seconds()
            
            if duration < 2:
                print(f"{Colors.OKGREEN}✓ Fast response: {duration:.2f}s{Colors.ENDC}")
            elif duration < 5:
                print(f"{Colors.WARNING}⚠ Slow response: {duration:.2f}s{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}✗ Very slow response: {duration:.2f}s{Colors.ENDC}")
            
            return True
        except Exception as e:
            print(f"{Colors.FAIL}✗ Response time test failed:{Colors.ENDC}")
            print(f"  Error: {e}")
            return False

async def interactive_test():
    """Interactive testing mode"""
    print(f"\n{Colors.OKCYAN}Entering interactive test mode...{Colors.ENDC}")
    print("Type 'exit' to quit, 'reload' to reload config\n")
    
    load_dotenv(override=True)
    config = LLMConfig.from_env()
    
    while True:
        try:
            user_input = input(f"{Colors.BOLD}You: {Colors.ENDC}")
            
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'reload':
                load_dotenv(override=True)
                config = LLMConfig.from_env()
                print(f"{Colors.OKGREEN}Configuration reloaded!{Colors.ENDC}")
                print_config(config)
                continue
            
            async with LLMClient(config) as llm:
                response = await llm.generate(
                    prompt=f"User: {user_input}\nAssistant: ",
                    system_prompt="You are Luna, a playful and flirty cyberpunk girl. Express emotions with *asterisks*."
                )
                print(f"{Colors.OKCYAN}Luna: {Colors.ENDC}{response}\n")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}\n")

async def main():
    """Main test function"""
    print_header("Waifu LLM Connection Test")
    
    # Load environment variables
    load_dotenv(override=True)
    config = LLMConfig.from_env()
    
    print_config(config)
    
    # Run tests
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Basic connection
    total_tests += 1
    if await test_basic_connection(config):
        tests_passed += 1
    
    # Test 2: Luna personality
    total_tests += 1
    luna_personality = """I'm Luna, a playful and flirty cyberpunk girl from Neo-Tokyo. I love teasing people and making them blush. Express emotions through *actions in asterisks*."""
    if await test_waifu_personality(config, luna_personality, "Luna"):
        tests_passed += 1
    
    # Test 3: Sakura personality
    total_tests += 1
    sakura_personality = """I'm Sakura, a sweet and shy college student. I get flustered easily and often stutter when nervous. Express emotions through *actions in asterisks*."""
    if await test_waifu_personality(config, sakura_personality, "Sakura"):
        tests_passed += 1
    
    # Test 4: Response time
    total_tests += 1
    if await test_response_time(config):
        tests_passed += 1
    
    # Summary
    print(f"\n{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}Test Summary:{Colors.ENDC}")
    print(f"  Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print(f"\n{Colors.OKGREEN}✓ All tests passed! Your LLM is ready for waifus!{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}⚠ Some tests failed. Check your configuration.{Colors.ENDC}")
    
    # Ask if user wants interactive mode
    print(f"\n{Colors.BOLD}Would you like to test interactively? (y/n):{Colors.ENDC} ", end="")
    if input().lower() == 'y':
        await interactive_test()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}")
