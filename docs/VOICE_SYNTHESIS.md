# Voice Synthesis Feature Documentation

## Overview
The voice synthesis feature brings waifus to life by converting their text responses into spoken audio. This dramatically enhances user engagement and creates a more intimate, immersive experience.

## Current Implementation (v1.0)

### Features
- **Web Speech API Integration**: Uses browser-native text-to-speech
- **Emotion-Aware Speech**: Dynamic voice parameters based on detected emotions
- **Personality-Based Voices**: Each waifu has unique voice characteristics
- **Visual Feedback**: Audio waveform visualization and character animations during speech
- **User Controls**: Volume slider and on/off toggle

### Voice Parameters by Emotion
- **Happy**: Faster rate (1.1x), higher pitch (1.1x)
- **Shy**: Slower rate (0.9x), lower pitch (0.95x), quieter volume (0.7x)
- **Flirty**: Slightly slower (0.95x), higher pitch (1.05x)
- **Excited**: Much faster (1.2x), higher pitch (1.15x), louder (1.1x)
- **Seductive**: Much slower (0.8x), lower pitch (0.9x), softer (0.8x)
- **Affectionate**: Normal speed, warm tone

### Waifu Voice Profiles
- **Luna (Cyberpunk)**: Energetic voice, higher pitch (1.3x), faster rate (1.1x)
- **Sakura (Shy)**: Soft voice, gentle pitch (1.2x), slower rate (0.9x)

## Usage

### Enabling/Disabling
Users can toggle voice synthesis using the voice button in the UI. Volume is adjustable via slider.

### Browser Compatibility
- Chrome/Edge: Full support with multiple voice options
- Firefox: Limited voice selection
- Safari: Basic support
- Mobile: Varies by device

## Future Enhancements

### Phase 2: ElevenLabs Integration
```python
# Add to backend/.env
VOICE_SYNTHESIS_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=your-api-key
ELEVENLABS_VOICE_LUNA=voice-id-for-luna
ELEVENLABS_VOICE_SAKURA=voice-id-for-sakura
```

### Phase 3: Advanced Features
1. **Voice Cloning**: Custom voices for each waifu
2. **Emotion Sounds**: Giggles, sighs, moans for NSFW content
3. **Multi-language Support**: Japanese, Chinese, Korean voices
4. **SSML Support**: Advanced speech markup for better control
5. **Voice Input**: Speech-to-text for hands-free interaction

### Phase 4: NSFW Audio
1. **Breathing Patterns**: Based on arousal level
2. **Pleasure Sounds**: Contextual audio responses
3. **Voice Acting**: Professional recordings for key phrases
4. **Audio Triggers**: Sound effects for actions

## API Reference

### Frontend Components

#### VoiceSynthesis Component
```javascript
<VoiceSynthesis
  message={waifuMessage}        // Last message object
  waifuId={selectedModel}       // Current waifu ID
  emotion={currentEmotion}      // Detected emotion
  waifuPersonality={personality} // Full personality text
  onSpeakingChange={callback}   // Speaking state callback
/>
```

#### VoiceSynthesisManager Class
- `speak(text, waifuId, emotion, personality, onStart, onEnd)`
- `stop()`
- `setEnabled(enabled)`
- `setVolume(volume)`

### Backend Configuration
```python
# Environment variables
ENABLE_VOICE_SYNTHESIS=true
VOICE_SYNTHESIS_PROVIDER=webspeech  # or 'elevenlabs'
```

## Troubleshooting

### No Voice Output
1. Check browser console for errors
2. Ensure browser supports Web Speech API
3. Try different browser
4. Check system audio settings

### Wrong Voice Selected
1. Limited voice options on some systems
2. Falls back to first available female voice
3. Install additional system voices if needed

### Performance Issues
1. Disable voice during intense animations
2. Reduce particle effects if stuttering
3. Use production build for better performance

## Code Integration Points

### Adding New Emotions
1. Add emotion to `getEmotionModifiers()` in VoiceSynthesis.js
2. Define rate, pitch, and volume multipliers
3. Test with different voice combinations

### Custom Voice Providers
1. Create new provider class extending VoiceSynthesisManager
2. Implement speak(), stop(), and configuration methods
3. Add provider selection logic

### Audio Visualization
1. Modify WaveformBar component for different effects
2. Add frequency analysis for more accurate visualization
3. Integrate with Three.js scene for 3D effects

## Best Practices
1. Always provide visual feedback when speaking
2. Allow users to interrupt speech
3. Respect user's volume preferences
4. Preload voices for faster first speech
5. Handle errors gracefully with fallbacks
