#!/usr/bin/env python3
"""
Test script for the Affection/Progression System
Tests affection calculations, database operations, and milestone unlocks
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from affection_manager import AffectionManager
from database import Database
import asyncio
import json


def test_affection_calculations():
    """Test affection change calculations"""
    print("Testing Affection Calculations...")
    
    manager = AffectionManager()
    
    # Test cases
    test_cases = [
        ("You're so beautiful!", "happy", {"personality_traits": {"flirtatiousness": 0.8}}, 0),
        ("I love you", "affectionate", {"personality_traits": {"affection": 0.9}}, 25),
        ("Let's spend time together", "neutral", {"personality_traits": {"affection": 0.5}}, 50),
        ("You're stupid", "neutral", {"personality_traits": {"confidence": 0.5}}, 10),
        ("Here's a gift for you", "happy", {"personality_traits": {"playfulness": 0.7}}, 30),
    ]
    
    for message, emotion, personality, current_level in test_cases:
        change, reason = manager.calculate_affection_change(message, emotion, personality, current_level)
        print(f"  Message: '{message}' | Emotion: {emotion} | Level: {current_level}")
        print(f"  -> Change: {change:+d} | Reason: {reason}")
        print()


def test_database_operations():
    """Test database operations"""
    print("Testing Database Operations...")
    
    # Use test database
    test_db = Database("test_waifu_chat.db")
    
    # Test session creation
    session_id = "test-session-123"
    session = test_db.get_or_create_session(session_id)
    print(f"  Created session: {session['session_id']}")
    
    # Test affection updates
    waifu_id = "luna"
    
    # Test multiple affection changes
    changes = [5, 3, -2, 10, 5]
    for change in changes:
        new_level, unlocked = test_db.update_affection(session_id, waifu_id, change)
        print(f"  Affection change: {change:+d} -> New level: {new_level}")
        if unlocked:
            print(f"    Unlocked: {', '.join(unlocked)}")
    
    # Test getting affection level
    level = test_db.get_affection_level(session_id, waifu_id)
    print(f"  Final affection level: {level}")
    
    # Test unlocked content
    unlocked_content = test_db.get_unlocked_content(session_id, waifu_id)
    print(f"  Unlocked content: {json.dumps(unlocked_content, indent=2)}")
    
    # Test session stats
    stats = test_db.get_session_stats(session_id)
    print(f"  Session stats: {json.dumps(stats, indent=2)}")
    
    # Clean up test database
    os.remove("test_waifu_chat.db")
    print("  Test database cleaned up")


async def test_milestone_messages():
    """Test milestone messages and progression"""
    print("\nTesting Milestone Messages...")
    
    manager = AffectionManager()
    test_db = Database("test_milestones.db")
    
    session_id = "milestone-test"
    waifu_id = "sakura"
    test_db.get_or_create_session(session_id)
    
    # Simulate progression through milestones
    messages = [
        "You're so cute!",
        "I love spending time with you",
        "You make me so happy",
        "I want to be closer to you",
        "I love you so much"
    ]
    
    current_level = 0
    for i in range(5):
        for message in messages:
            result = manager.process_interaction(
                session_id, waifu_id, message, 
                "*blushes* Thank you...", "shy",
                {"personality_traits": {"shyness": 0.9, "affection": 0.8}}
            )
            
            if result['is_milestone']:
                print(f"  Milestone reached at level {result['new_level']}!")
                print(f"  Message: {result['milestone_message']}")
                print(f"  Unlocked: {', '.join(result['unlocked'])}")
                print()
            
            current_level = result['new_level']
            
            # Stop if we reach max level
            if current_level >= 100:
                break
    
    print(f"  Final level: {current_level}")
    
    # Clean up
    os.remove("test_milestones.db")


def test_response_modifiers():
    """Test affection-based response modifiers"""
    print("\nTesting Response Modifiers...")
    
    manager = AffectionManager()
    
    levels = [0, 10, 25, 50, 75, 90, 100]
    for level in levels:
        modifier = manager.get_affection_response_modifier(level)
        dialogue_level = manager.get_dialogue_level(level)
        print(f"  Level {level}: {dialogue_level}")
        print(f"    -> {modifier}")
        print()


def main():
    """Run all tests"""
    print("=" * 60)
    print("Affection System Test Suite")
    print("=" * 60)
    print()
    
    test_affection_calculations()
    print("\n" + "-" * 60 + "\n")
    
    test_database_operations()
    print("\n" + "-" * 60 + "\n")
    
    test_response_modifiers()
    print("\n" + "-" * 60 + "\n")
    
    # Run async test
    asyncio.run(test_milestone_messages())
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
