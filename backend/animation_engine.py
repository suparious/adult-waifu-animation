"""
Enhanced Animation System for Waifu Models
Provides sophisticated procedural animations with physics
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import json

class AnimationType(Enum):
    IDLE = "idle"
    TALK = "talk"
    EMOTION = "emotion"
    SPECIAL = "special"
    PHYSICS = "physics"

class BodyPart(Enum):
    HEAD = "head"
    CHEST = "chest"
    HIPS = "hips"
    LEFT_ARM = "left_arm"
    RIGHT_ARM = "right_arm"
    HAIR = "hair"
    EYES = "eyes"
    MOUTH = "mouth"

@dataclass
class AnimationKeyframe:
    time: float
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    scale: Tuple[float, float, float]
    easing: str = "linear"

@dataclass
class PhysicsParams:
    gravity: float = 9.8
    mass: float = 1.0
    stiffness: float = 0.5
    damping: float = 0.8
    wind_strength: float = 0.1

class WaifuAnimationEngine:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.current_state = {}
        self.animation_queue = []
        self.physics_params = PhysicsParams()
        self.bone_positions = self._initialize_bones()
        self.time = 0.0
        
    def _initialize_bones(self) -> Dict[BodyPart, Dict]:
        """Initialize bone positions and properties"""
        return {
            BodyPart.HEAD: {
                "position": np.array([0, 1.6, 0]),
                "rotation": np.array([0, 0, 0]),
                "velocity": np.array([0, 0, 0]),
                "mass": 2.0
            },
            BodyPart.CHEST: {
                "position": np.array([0, 1.2, 0]),
                "rotation": np.array([0, 0, 0]),
                "velocity": np.array([0, 0, 0]),
                "mass": 5.0
            },
            BodyPart.HIPS: {
                "position": np.array([0, 0.8, 0]),
                "rotation": np.array([0, 0, 0]),
                "velocity": np.array([0, 0, 0]),
                "mass": 8.0
            },
            BodyPart.LEFT_ARM: {
                "position": np.array([-0.3, 1.2, 0]),
                "rotation": np.array([0, 0, 0]),
                "velocity": np.array([0, 0, 0]),
                "mass": 1.5
            },
            BodyPart.RIGHT_ARM: {
                "position": np.array([0.3, 1.2, 0]),
                "rotation": np.array([0, 0, 0]),
                "velocity": np.array([0, 0, 0]),
                "mass": 1.5
            },
            BodyPart.HAIR: {
                "position": np.array([0, 1.8, -0.1]),
                "rotation": np.array([0, 0, 0]),
                "velocity": np.array([0, 0, 0]),
                "mass": 0.5,
                "segments": self._create_hair_segments()
            }
        }
    
    def _create_hair_segments(self, count: int = 10) -> List[Dict]:
        """Create segmented hair for physics simulation"""
        segments = []
        for i in range(count):
            segments.append({
                "position": np.array([0, 1.8 - i * 0.05, -0.1 - i * 0.02]),
                "velocity": np.array([0, 0, 0]),
                "mass": 0.1
            })
        return segments
    
    def generate_idle_animation(self, intensity: float = 0.5) -> List[AnimationKeyframe]:
        """Generate idle breathing and swaying animation"""
        keyframes = []
        duration = 4.0  # 4 second loop
        
        for t in np.linspace(0, duration, 20):
            # Breathing
            breath = np.sin(t * np.pi / 2) * 0.02 * intensity
            
            # Gentle sway
            sway = np.sin(t * 0.5) * 0.05 * intensity
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(sway, 0, 0),
                rotation=(0, sway * 0.5, 0),
                scale=(1 - breath * 0.5, 1 + breath, 1),
                easing="ease-in-out"
            ))
        
        return keyframes
    
    def generate_emotion_animation(self, emotion: str, intensity: float) -> List[AnimationKeyframe]:
        """Generate emotion-specific animations"""
        animations = {
            "happy": self._happy_animation,
            "shy": self._shy_animation,
            "flirty": self._flirty_animation,
            "excited": self._excited_animation,
            "seductive": self._seductive_animation,
            "affectionate": self._affectionate_animation
        }
        
        if emotion in animations:
            return animations[emotion](intensity)
        
        return self.generate_idle_animation(intensity)
    
    def _happy_animation(self, intensity: float) -> List[AnimationKeyframe]:
        """Bouncy, energetic animation"""
        keyframes = []
        duration = 2.0
        
        for t in np.linspace(0, duration, 15):
            bounce = abs(np.sin(t * np.pi * 2)) * 0.1 * intensity
            tilt = np.sin(t * np.pi) * 15 * intensity  # degrees
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(0, bounce, 0),
                rotation=(0, 0, tilt),
                scale=(1, 1, 1),
                easing="ease-out"
            ))
        
        return keyframes
    
    def _shy_animation(self, intensity: float) -> List[AnimationKeyframe]:
        """Subtle, withdrawn animation"""
        keyframes = []
        duration = 3.0
        
        for t in np.linspace(0, duration, 15):
            # Look away
            look_away = np.sin(t * 0.5) * 20 * intensity
            # Fidget
            fidget = np.sin(t * 5) * 0.02 * intensity
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(fidget, 0, 0),
                rotation=(0, look_away, 0),
                scale=(0.98, 0.98, 0.98),
                easing="ease-in-out"
            ))
        
        return keyframes
    
    def _flirty_animation(self, intensity: float) -> List[AnimationKeyframe]:
        """Playful, seductive animation"""
        keyframes = []
        duration = 3.5
        
        for t in np.linspace(0, duration, 20):
            # Hip sway
            hip_sway = np.sin(t * 2) * 0.15 * intensity
            # Head tilt
            head_tilt = np.sin(t * 1.5 + np.pi/4) * 10 * intensity
            # Subtle lean
            lean = np.sin(t) * 0.05 * intensity
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(hip_sway, 0, lean),
                rotation=(head_tilt * 0.5, 0, head_tilt),
                scale=(1, 1, 1),
                easing="ease-in-out"
            ))
        
        return keyframes
    
    def _excited_animation(self, intensity: float) -> List[AnimationKeyframe]:
        """Very energetic, jumpy animation"""
        keyframes = []
        duration = 1.5
        
        for t in np.linspace(0, duration, 15):
            # Jumping motion
            jump = abs(np.sin(t * np.pi * 3)) * 0.2 * intensity
            # Arm movement simulation
            arm_swing = np.sin(t * np.pi * 4) * 20 * intensity
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(0, jump, 0),
                rotation=(0, arm_swing * 0.3, 0),
                scale=(1.05, 0.95 + jump * 0.2, 1.05),
                easing="ease-out"
            ))
        
        return keyframes
    
    def _seductive_animation(self, intensity: float) -> List[AnimationKeyframe]:
        """Slow, sultry animation"""
        keyframes = []
        duration = 5.0
        
        for t in np.linspace(0, duration, 25):
            # Slow body wave
            wave = np.sin(t * 0.8) * 0.1 * intensity
            # Subtle chest movement
            chest = np.sin(t * 1.2 + np.pi/3) * 0.03 * intensity
            # Hip circle
            hip_x = np.sin(t) * 0.08 * intensity
            hip_z = np.cos(t) * 0.08 * intensity
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(hip_x, chest, hip_z),
                rotation=(wave * 10, 0, wave * 5),
                scale=(1 + chest * 0.3, 1 - chest * 0.1, 1),
                easing="ease-in-out"
            ))
        
        return keyframes
    
    def _affectionate_animation(self, intensity: float) -> List[AnimationKeyframe]:
        """Warm, loving animation"""
        keyframes = []
        duration = 4.0
        
        for t in np.linspace(0, duration, 20):
            # Gentle lean forward
            lean = np.sin(t * 0.5) * 0.1 * intensity
            # Soft head movement
            head = np.sin(t * 0.8) * 8 * intensity
            
            keyframes.append(AnimationKeyframe(
                time=t,
                position=(0, 0, lean),
                rotation=(head * 0.5, head, 0),
                scale=(1, 1, 1),
                easing="ease-in-out"
            ))
        
        return keyframes
    
    def apply_physics(self, delta_time: float) -> Dict:
        """Apply physics simulation to hair and clothing"""
        wind = self._calculate_wind()
        
        # Update hair physics
        if BodyPart.HAIR in self.bone_positions:
            hair = self.bone_positions[BodyPart.HAIR]
            for i, segment in enumerate(hair["segments"]):
                # Apply forces
                force = np.array([0, -self.physics_params.gravity * segment["mass"], 0])
                force += wind * (1 - i / len(hair["segments"]))  # Less wind on lower segments
                
                # Update velocity
                segment["velocity"] += force * delta_time
                segment["velocity"] *= self.physics_params.damping
                
                # Update position
                segment["position"] += segment["velocity"] * delta_time
                
                # Constraint to previous segment
                if i > 0:
                    prev_segment = hair["segments"][i-1]
                    direction = segment["position"] - prev_segment["position"]
                    distance = np.linalg.norm(direction)
                    target_distance = 0.05
                    
                    if distance > target_distance:
                        direction /= distance
                        segment["position"] = prev_segment["position"] + direction * target_distance
        
        return self._serialize_physics_state()
    
    def _calculate_wind(self) -> np.ndarray:
        """Calculate wind force with some randomness"""
        base_wind = np.array([
            np.sin(self.time * 0.5) * 0.3,
            0,
            np.cos(self.time * 0.7) * 0.2
        ])
        
        # Add turbulence
        turbulence = np.random.normal(0, 0.1, 3)
        
        return (base_wind + turbulence) * self.physics_params.wind_strength
    
    def _serialize_physics_state(self) -> Dict:
        """Convert physics state to serializable format"""
        state = {}
        
        for part, data in self.bone_positions.items():
            state[part.value] = {
                "position": data["position"].tolist(),
                "rotation": data["rotation"].tolist()
            }
            
            if "segments" in data:
                state[part.value]["segments"] = [
                    {"position": seg["position"].tolist()}
                    for seg in data["segments"]
                ]
        
        return state
    
    def blend_animations(self, animations: List[Tuple[List[AnimationKeyframe], float]]) -> List[AnimationKeyframe]:
        """Blend multiple animations together with weights"""
        if not animations:
            return []
        
        # Get the longest animation duration
        max_duration = max(anim[0][-1].time for anim in animations if anim[0])
        
        # Sample at regular intervals
        sample_times = np.linspace(0, max_duration, 30)
        blended_keyframes = []
        
        for t in sample_times:
            blended_pos = np.zeros(3)
            blended_rot = np.zeros(3)
            blended_scale = np.ones(3)
            total_weight = 0
            
            for keyframes, weight in animations:
                if keyframes:
                    # Find interpolated value at time t
                    frame = self._interpolate_at_time(keyframes, t)
                    if frame:
                        blended_pos += np.array(frame.position) * weight
                        blended_rot += np.array(frame.rotation) * weight
                        blended_scale *= np.power(np.array(frame.scale), weight)
                        total_weight += weight
            
            if total_weight > 0:
                blended_pos /= total_weight
                blended_rot /= total_weight
                
                blended_keyframes.append(AnimationKeyframe(
                    time=t,
                    position=tuple(blended_pos),
                    rotation=tuple(blended_rot),
                    scale=tuple(blended_scale),
                    easing="linear"
                ))
        
        return blended_keyframes
    
    def _interpolate_at_time(self, keyframes: List[AnimationKeyframe], time: float) -> Optional[AnimationKeyframe]:
        """Interpolate keyframe values at a specific time"""
        if not keyframes:
            return None
        
        # Find surrounding keyframes
        prev_frame = None
        next_frame = None
        
        for frame in keyframes:
            if frame.time <= time:
                prev_frame = frame
            elif frame.time > time and next_frame is None:
                next_frame = frame
                break
        
        if prev_frame is None:
            return keyframes[0]
        if next_frame is None:
            return keyframes[-1]
        
        # Linear interpolation
        t = (time - prev_frame.time) / (next_frame.time - prev_frame.time)
        
        # Apply easing
        if prev_frame.easing == "ease-in":
            t = t * t
        elif prev_frame.easing == "ease-out":
            t = 1 - (1 - t) * (1 - t)
        elif prev_frame.easing == "ease-in-out":
            t = 3 * t * t - 2 * t * t * t
        
        # Interpolate values
        pos = tuple(
            prev_frame.position[i] + (next_frame.position[i] - prev_frame.position[i]) * t
            for i in range(3)
        )
        rot = tuple(
            prev_frame.rotation[i] + (next_frame.rotation[i] - prev_frame.rotation[i]) * t
            for i in range(3)
        )
        scale = tuple(
            prev_frame.scale[i] + (next_frame.scale[i] - prev_frame.scale[i]) * t
            for i in range(3)
        )
        
        return AnimationKeyframe(time=time, position=pos, rotation=rot, scale=scale)
    
    async def update(self, delta_time: float) -> Dict:
        """Main update loop for animation system"""
        self.time += delta_time
        
        # Update physics
        physics_state = self.apply_physics(delta_time)
        
        # Process animation queue
        current_animations = []
        for anim_type, anim_data in self.animation_queue:
            if anim_type == AnimationType.IDLE:
                current_animations.append((self.generate_idle_animation(anim_data["intensity"]), 1.0))
            elif anim_type == AnimationType.EMOTION:
                current_animations.append((
                    self.generate_emotion_animation(anim_data["emotion"], anim_data["intensity"]),
                    anim_data.get("weight", 1.0)
                ))
        
        # Blend animations
        blended = self.blend_animations(current_animations)
        
        # Combine with physics
        return {
            "animation": self._serialize_keyframes(blended),
            "physics": physics_state,
            "time": self.time
        }
    
    def _serialize_keyframes(self, keyframes: List[AnimationKeyframe]) -> List[Dict]:
        """Convert keyframes to serializable format"""
        return [
            {
                "time": kf.time,
                "position": kf.position,
                "rotation": kf.rotation,
                "scale": kf.scale,
                "easing": kf.easing
            }
            for kf in keyframes
        ]
    
    def add_animation(self, animation_type: AnimationType, data: Dict):
        """Add animation to the queue"""
        self.animation_queue.append((animation_type, data))
    
    def clear_animations(self):
        """Clear all animations except idle"""
        self.animation_queue = [
            (anim_type, data) 
            for anim_type, data in self.animation_queue 
            if anim_type == AnimationType.IDLE
        ]
    
    def set_physics_params(self, params: Dict):
        """Update physics parameters"""
        for key, value in params.items():
            if hasattr(self.physics_params, key):
                setattr(self.physics_params, key, value)
