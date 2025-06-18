"""
Affection Management System
Handles affection calculations, unlocks, and progression mechanics
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import re
from database import get_db

class AffectionManager:
    """Manages affection levels and progression mechanics"""
    
    # Affection change rules
    AFFECTION_RULES = {
        # Positive interactions
        "compliment": {
            "keywords": ["beautiful", "gorgeous", "pretty", "cute", "lovely", "stunning", "hot", "sexy"],
            "base_change": 3,
            "multiplier": 1.0
        },
        "love_declaration": {
            "keywords": ["love you", "i love", "in love", "adore you", "care about you"],
            "base_change": 5,
            "multiplier": 1.5
        },
        "affectionate": {
            "keywords": ["hug", "cuddle", "kiss", "hold", "embrace", "snuggle", "caress"],
            "base_change": 3,
            "multiplier": 1.2
        },
        "gift": {
            "keywords": ["gift", "present", "flowers", "chocolate", "jewelry", "surprise"],
            "base_change": 4,
            "multiplier": 1.3
        },
        "quality_time": {
            "keywords": ["spend time", "be with you", "together", "date", "talk with you"],
            "base_change": 2,
            "multiplier": 1.0
        },
        "protective": {
            "keywords": ["protect you", "keep you safe", "care for you", "worry about you"],
            "base_change": 3,
            "multiplier": 1.1
        },
        
        # Negative interactions
        "rude": {
            "keywords": ["stupid", "dumb", "ugly", "hate", "annoying", "worthless", "useless"],
            "base_change": -5,
            "multiplier": 1.0
        },
        "dismissive": {
            "keywords": ["whatever", "don't care", "boring", "not interested", "go away"],
            "base_change": -3,
            "multiplier": 1.0
        },
        "inappropriate": {
            "keywords": ["shut up", "leave me alone", "get lost", "buzz off"],
            "base_change": -4,
            "multiplier": 1.0
        }
    }
    
    # Emotion to affection modifiers
    EMOTION_MODIFIERS = {
        "affectionate": 1.5,
        "flirty": 1.3,
        "happy": 1.2,
        "playful": 1.1,
        "excited": 1.2,
        "shy": 1.0,
        "neutral": 0.8,
        "seductive": 1.4
    }
    
    # Milestone messages
    MILESTONE_MESSAGES = {
        10: "I'm starting to feel comfortable with you... 💕",
        25: "*blushes* You make me feel special... I'd like to get closer to you.",
        40: "I think about you when you're not here... Is that weird? 🥰",
        50: "*looks into your eyes* I... I really care about you. More than I expected.",
        65: "*whispers* Being with you feels so right... I want to show you more of me.",
        75: "My heart races whenever I see you... I think I'm falling for you. 💗",
        90: "*breathing heavily* I need you... I want to be yours completely.",
        100: "I love you with all my heart. You're everything to me. Forever yours. 💝"
    }
    
    def __init__(self):
        self.db = get_db()
        self._time_bonus_cache = {}
    
    def calculate_affection_change(self, message: str, emotion: str, 
                                 waifu_personality: Dict, current_level: int) -> Tuple[int, str]:
        """
        Calculate affection change based on message content and context
        Returns: (change_amount, reason)
        """
        message_lower = message.lower()
        total_change = 0
        reasons = []
        
        # Check for keyword matches
        for rule_name, rule in self.AFFECTION_RULES.items():
            if any(keyword in message_lower for keyword in rule["keywords"]):
                base_change = rule["base_change"]
                
                # Apply emotion modifier
                emotion_mod = self.EMOTION_MODIFIERS.get(emotion, 1.0)
                
                # Apply personality compatibility
                personality_mod = self._calculate_personality_modifier(
                    rule_name, waifu_personality, current_level
                )
                
                # Calculate final change
                change = int(base_change * rule["multiplier"] * emotion_mod * personality_mod)
                
                if change != 0:
                    total_change += change
                    reasons.append(f"{rule_name} ({'+' if change > 0 else ''}{change})")
        
        # Time-based bonus (for continued conversation)
        time_bonus = self._calculate_time_bonus(emotion)
        if time_bonus > 0:
            total_change += time_bonus
            reasons.append(f"engagement bonus (+{time_bonus})")
        
        # Level-based scaling (harder to gain at higher levels)
        if total_change > 0 and current_level > 50:
            scale_factor = 1.0 - ((current_level - 50) / 100)  # 50% reduction at level 100
            total_change = max(1, int(total_change * scale_factor))
        
        # Cap changes
        total_change = max(-10, min(10, total_change))
        
        reason = ", ".join(reasons) if reasons else "normal interaction"
        return total_change, reason
    
    def _calculate_personality_modifier(self, interaction_type: str, 
                                      personality: Dict, current_level: int) -> float:
        """Calculate modifier based on personality compatibility"""
        # Extract personality traits from the waifu personality dict
        traits = personality.get('personality_traits', {})
        
        modifiers = {
            "compliment": 1.0 + (traits.get('flirtatiousness', 0.5) * 0.3),
            "love_declaration": 1.0 + (traits.get('affection', 0.5) * 0.4),
            "affectionate": 1.0 + (traits.get('affection', 0.5) * 0.3),
            "gift": 1.0 + (traits.get('playfulness', 0.5) * 0.2),
            "quality_time": 1.0 + (traits.get('affection', 0.5) * 0.2),
            "protective": 1.0 + ((1 - traits.get('confidence', 0.5)) * 0.3),  # Shy waifus like protection
        }
        
        base_mod = modifiers.get(interaction_type, 1.0)
        
        # Add progression bonus (more receptive at higher affection)
        progression_bonus = (current_level / 100) * 0.2
        
        return base_mod + progression_bonus
    
    def _calculate_time_bonus(self, emotion: str) -> int:
        """Calculate bonus for continued engagement"""
        now = datetime.now()
        cache_key = f"{emotion}_{now.minute}"
        
        # Simple time-based bonus (resets each minute)
        if cache_key not in self._time_bonus_cache:
            self._time_bonus_cache.clear()  # Clear old entries
            self._time_bonus_cache[cache_key] = 1 if emotion in ["happy", "flirty", "affectionate"] else 0
        
        return self._time_bonus_cache[cache_key]
    
    def process_interaction(self, session_id: str, waifu_id: str, user_message: str,
                          waifu_response: str, emotion: str, waifu_data: Dict) -> Dict:
        """
        Process an interaction and update affection
        Returns: {
            'previous_level': int,
            'new_level': int,
            'change': int,
            'reason': str,
            'unlocked': List[str],
            'milestone_message': Optional[str],
            'is_milestone': bool
        }
        """
        # Get current affection level
        current_level = self.db.get_affection_level(session_id, waifu_id)
        
        # Calculate affection change
        change, reason = self.calculate_affection_change(
            user_message, emotion, waifu_data, current_level
        )
        
        # Update affection and check for unlocks
        new_level, unlocked = self.db.update_affection(session_id, waifu_id, change)
        
        # Save interaction to history
        self.db.save_interaction(
            session_id, waifu_id, user_message, waifu_response, emotion, change
        )
        
        # Check for milestone message
        milestone_message = None
        is_milestone = False
        
        for milestone, message in self.MILESTONE_MESSAGES.items():
            if current_level < milestone <= new_level:
                milestone_message = message
                is_milestone = True
                break
        
        return {
            'previous_level': current_level,
            'new_level': new_level,
            'change': change,
            'reason': reason,
            'unlocked': unlocked,
            'milestone_message': milestone_message,
            'is_milestone': is_milestone
        }
    
    def get_affection_response_modifier(self, affection_level: int) -> str:
        """Get response modifier based on affection level"""
        if affection_level < 10:
            return "You should respond politely but with some distance, as you don't know them well yet."
        elif affection_level < 25:
            return "You're warming up to them. Be friendly and show growing interest."
        elif affection_level < 50:
            return "You feel comfortable with them. Be more open, playful, and occasionally flirty."
        elif affection_level < 75:
            return "You have strong feelings for them. Be affectionate, caring, and openly flirty. Share personal thoughts."
        elif affection_level < 90:
            return "You're deeply in love. Be passionate, intimate, and express your desire to be closer."
        else:
            return "You're completely devoted. Express deep love, be extremely affectionate, intimate, and passionate. Nothing holds you back."
    
    def check_content_unlock(self, session_id: str, waifu_id: str, 
                           content_type: str, content_id: str) -> bool:
        """Check if specific content is unlocked"""
        unlocked = self.db.get_unlocked_content(session_id, waifu_id)
        return content_id in unlocked.get(content_type, [])
    
    def get_available_animations(self, session_id: str, waifu_id: str, 
                               base_animations: List[str]) -> List[str]:
        """Get list of available animations including unlocked ones"""
        unlocked = self.db.get_unlocked_content(session_id, waifu_id)
        unlocked_animations = unlocked.get('animation', [])
        
        # Combine base animations with unlocked ones
        all_animations = list(set(base_animations + unlocked_animations))
        return all_animations
    
    def get_dialogue_level(self, affection_level: int) -> str:
        """Get appropriate dialogue level based on affection"""
        if affection_level < 25:
            return "friendly"
        elif affection_level < 50:
            return "flirty"
        elif affection_level < 75:
            return "intimate"
        elif affection_level < 90:
            return "passionate"
        else:
            return "devoted"

# Singleton instance
_affection_manager = None

def get_affection_manager() -> AffectionManager:
    """Get affection manager singleton instance"""
    global _affection_manager
    if _affection_manager is None:
        _affection_manager = AffectionManager()
    return _affection_manager
