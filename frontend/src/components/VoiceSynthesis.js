import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';

const VoiceControls = styled.div`
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(0, 0, 0, 0.7);
  padding: 10px 15px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  z-index: 100;
`;

const VoiceToggle = styled.button`
  background: ${props => props.enabled ? '#ff6ec7' : '#666'};
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 15px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;

  &:hover {
    background: ${props => props.enabled ? '#ff9472' : '#888'};
    transform: scale(1.05);
  }

  svg {
    width: 16px;
    height: 16px;
  }
`;

const VolumeSlider = styled.input`
  width: 80px;
  height: 4px;
  background: #333;
  outline: none;
  opacity: 0.7;
  transition: opacity 0.2s;
  cursor: pointer;

  &:hover {
    opacity: 1;
  }

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 12px;
    height: 12px;
    background: #ff6ec7;
    cursor: pointer;
    border-radius: 50%;
  }
`;

const VoiceIndicator = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  pointer-events: none;
  opacity: ${props => props.speaking ? 0.6 : 0};
  transition: opacity 0.3s ease;
`;

const WaveformBar = styled.div`
  position: absolute;
  bottom: 50%;
  left: ${props => props.position}%;
  width: 3px;
  height: ${props => props.height}px;
  background: linear-gradient(to top, #ff6ec7, #ff9472);
  border-radius: 2px;
  transform-origin: bottom;
  animation: ${props => props.speaking ? 'wave 0.5s ease-in-out infinite' : 'none'};
  animation-delay: ${props => props.delay}s;

  @keyframes wave {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(${props => props.amplitude}); }
  }
`;

class VoiceSynthesisManager {
  constructor() {
    this.synthesis = window.speechSynthesis;
    this.voices = [];
    this.currentUtterance = null;
    this.enabled = true;
    this.volume = 0.8;
    this.loadVoices();
  }

  loadVoices() {
    // Load available voices
    const loadVoiceList = () => {
      this.voices = this.synthesis.getVoices();
    };

    loadVoiceList();
    if (this.synthesis.onvoiceschanged !== undefined) {
      this.synthesis.onvoiceschanged = loadVoiceList;
    }
  }

  getVoiceForWaifu(waifuId, personality) {
    // Select appropriate voice based on waifu personality
    const preferredVoices = {
      luna: {
        // Prefer younger, energetic female voices
        keywords: ['female', 'woman', 'girl', 'Google UK English Female', 'Microsoft Zira', 'Samantha'],
        fallbackLang: 'en-US'
      },
      sakura: {
        // Prefer softer, gentler female voices
        keywords: ['female', 'woman', 'Google US English', 'Microsoft Haruka', 'Kyoko', 'Ting-Ting'],
        fallbackLang: 'en-US'
      }
    };

    const prefs = preferredVoices[waifuId] || preferredVoices.luna;
    
    // Try to find a matching voice
    let selectedVoice = this.voices.find(voice => 
      prefs.keywords.some(keyword => voice.name.includes(keyword))
    );

    // Fallback to any female voice
    if (!selectedVoice) {
      selectedVoice = this.voices.find(voice => 
        voice.name.includes('female') || voice.name.includes('Female')
      );
    }

    // Final fallback to any voice in preferred language
    if (!selectedVoice) {
      selectedVoice = this.voices.find(voice => 
        voice.lang.startsWith(prefs.fallbackLang.split('-')[0])
      );
    }

    return selectedVoice || this.voices[0];
  }

  createUtterance(text, waifuId, emotion, personality) {
    // Remove action markers (*text*)
    const cleanText = text.replace(/\*[^*]+\*/g, '');
    
    const utterance = new SpeechSynthesisUtterance(cleanText);
    
    // Get appropriate voice
    const voice = this.getVoiceForWaifu(waifuId, personality);
    if (voice) {
      utterance.voice = voice;
    }

    // Base voice parameters from personality
    const baseParams = this.getBaseVoiceParams(waifuId, personality);
    
    // Apply emotion modifiers
    const emotionParams = this.getEmotionModifiers(emotion);
    
    // Combine parameters
    utterance.rate = baseParams.rate * emotionParams.rateMultiplier;
    utterance.pitch = baseParams.pitch * emotionParams.pitchMultiplier;
    utterance.volume = this.volume * emotionParams.volumeMultiplier;

    return utterance;
  }

  getBaseVoiceParams(waifuId, personality) {
    // Base parameters for each waifu
    const params = {
      luna: {
        rate: 1.1,      // Slightly faster, energetic
        pitch: 1.3,     // Higher pitch, playful
      },
      sakura: {
        rate: 0.9,      // Slower, thoughtful
        pitch: 1.2,     // Soft, feminine
      }
    };

    return params[waifuId] || params.luna;
  }

  getEmotionModifiers(emotion) {
    // Emotion-based voice modifiers
    const modifiers = {
      happy: {
        rateMultiplier: 1.1,
        pitchMultiplier: 1.1,
        volumeMultiplier: 1.0
      },
      shy: {
        rateMultiplier: 0.9,
        pitchMultiplier: 0.95,
        volumeMultiplier: 0.7
      },
      flirty: {
        rateMultiplier: 0.95,
        pitchMultiplier: 1.05,
        volumeMultiplier: 0.9
      },
      excited: {
        rateMultiplier: 1.2,
        pitchMultiplier: 1.15,
        volumeMultiplier: 1.1
      },
      seductive: {
        rateMultiplier: 0.8,
        pitchMultiplier: 0.9,
        volumeMultiplier: 0.8
      },
      affectionate: {
        rateMultiplier: 0.95,
        pitchMultiplier: 1.0,
        volumeMultiplier: 0.85
      },
      neutral: {
        rateMultiplier: 1.0,
        pitchMultiplier: 1.0,
        volumeMultiplier: 1.0
      }
    };

    return modifiers[emotion] || modifiers.neutral;
  }

  speak(text, waifuId, emotion, personality, onStart, onEnd) {
    if (!this.enabled || !text) return;

    // Cancel any ongoing speech
    this.synthesis.cancel();

    const utterance = this.createUtterance(text, waifuId, emotion, personality);
    
    utterance.onstart = () => {
      this.currentUtterance = utterance;
      if (onStart) onStart();
    };

    utterance.onend = () => {
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    utterance.onerror = (error) => {
      console.error('Speech synthesis error:', error);
      this.currentUtterance = null;
      if (onEnd) onEnd();
    };

    this.synthesis.speak(utterance);
  }

  stop() {
    this.synthesis.cancel();
    this.currentUtterance = null;
  }

  setEnabled(enabled) {
    this.enabled = enabled;
    if (!enabled) {
      this.stop();
    }
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(1, volume));
  }
}

function VoiceSynthesis({ message, waifuId, emotion, waifuPersonality, onSpeakingChange }) {
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [volume, setVolume] = useState(0.8);
  const [speaking, setSpeaking] = useState(false);
  const voiceManagerRef = useRef(null);

  useEffect(() => {
    // Initialize voice manager
    voiceManagerRef.current = new VoiceSynthesisManager();
    voiceManagerRef.current.setVolume(volume);
    
    return () => {
      // Cleanup
      if (voiceManagerRef.current) {
        voiceManagerRef.current.stop();
      }
    };
  }, []);

  useEffect(() => {
    // Speak new messages
    if (message && message.sender === 'waifu' && voiceEnabled) {
      const manager = voiceManagerRef.current;
      if (manager) {
        manager.speak(
          message.text,
          waifuId,
          emotion || 'neutral',
          waifuPersonality,
          () => {
            setSpeaking(true);
            if (onSpeakingChange) onSpeakingChange(true);
          },
          () => {
            setSpeaking(false);
            if (onSpeakingChange) onSpeakingChange(false);
          }
        );
      }
    }
  }, [message, waifuId, emotion, waifuPersonality, voiceEnabled, onSpeakingChange]);

  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (voiceManagerRef.current) {
      voiceManagerRef.current.setVolume(newVolume);
    }
  };

  const toggleVoice = () => {
    const newEnabled = !voiceEnabled;
    setVoiceEnabled(newEnabled);
    if (voiceManagerRef.current) {
      voiceManagerRef.current.setEnabled(newEnabled);
    }
  };

  return (
    <>
      {/* Voice Controls */}
      <VoiceControls>
        <VoiceToggle enabled={voiceEnabled} onClick={toggleVoice}>
          {voiceEnabled ? (
            <>
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
              </svg>
              Voice On
            </>
          ) : (
            <>
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-18-18zM12 4L9.91 6.09 12 8.18V4z"/>
              </svg>
              Voice Off
            </>
          )}
        </VoiceToggle>
        <VolumeSlider
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={volume}
          onChange={handleVolumeChange}
        />
      </VoiceControls>

      {/* Visual Voice Indicator */}
      <VoiceIndicator speaking={speaking}>
        {[...Array(8)].map((_, i) => (
          <WaveformBar
            key={i}
            speaking={speaking}
            position={12.5 * i + 6.25}
            height={40 + Math.sin(i) * 20}
            amplitude={1.5 + Math.sin(i * 0.5) * 0.5}
            delay={i * 0.05}
          />
        ))}
      </VoiceIndicator>
    </>
  );
}

export default VoiceSynthesis;
