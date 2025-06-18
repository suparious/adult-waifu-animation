# Frontend Configuration Guide

The frontend configuration system provides a centralized place to manage all settings and parameters for the Waifu Animation Chat application.

## Configuration File Location

The main configuration file is located at:
```
frontend/src/config.js
```

## Using Local Overrides

You can create local configuration overrides that won't be committed to git:

1. Copy the example file:
   ```bash
   cp frontend/src/config.local.js.example frontend/src/config.local.js
   ```

2. Edit `config.local.js` with your custom settings

3. The file is automatically git-ignored

## Configuration Structure

### API Configuration (`config.api`)
```javascript
api: {
  baseUrl: 'http://localhost:8000',      // Backend API URL
  websocketUrl: 'ws://localhost:8000',   // WebSocket URL
  endpoints: {                           // API endpoints
    models: '/api/models',
    systemInfo: '/api/system-info',
    websocket: '/ws'
  },
  timeout: 30000,                        // Request timeout (ms)
  reconnectDelay: 3000,                  // WebSocket reconnect delay
  maxReconnectAttempts: 10               // Max reconnection attempts
}
```

### Animation Configuration (`config.animation`)

#### Base Animation Parameters
```javascript
base: {
  breathingSpeed: 1.0,        // Base breathing animation speed
  breathingIntensity: 0.02,   // How much the model expands/contracts
  swaySpeed: 0.5,            // Side-to-side sway speed
  swayIntensity: 0.1,        // Amount of sway
  idleRotationSpeed: 0.3,    // Idle rotation speed
  idleRotationAmount: 0.05   // Idle rotation amount
}
```

#### Emotion-Specific Animations
Each emotion can override base parameters:
```javascript
emotions: {
  happy: {
    breathingSpeed: 1.5,
    bounceSpeed: 2,
    bounceIntensity: 0.1
  },
  // ... other emotions
}
```

#### Speaking Animation
```javascript
speaking: {
  breathingMultiplier: 1.3,    // Breathing speed increase when speaking
  headBobSpeed: 8,             // Head movement speed
  emissiveIntensity: 0.2       // Glow intensity when speaking
}
```

### Voice Configuration (`config.voice`)

#### Waifu Voice Profiles
```javascript
waifuProfiles: {
  luna: {
    rate: 1.1,              // Speech rate (1.0 = normal)
    pitch: 1.3,             // Voice pitch (1.0 = normal)
    preferredVoices: [...], // Preferred voice names
    fallbackLang: 'en-US'   // Fallback language
  }
}
```

#### Emotion Voice Modifiers
```javascript
emotionModifiers: {
  shy: {
    rateMultiplier: 0.9,    // Slower speech
    pitchMultiplier: 0.95,  // Slightly lower pitch
    volumeMultiplier: 0.7   // Quieter volume
  }
}
```

### Visual Configuration (`config.visual`)

#### Camera Settings
```javascript
camera: {
  position: [0, 0, 8],      // Initial camera position [x, y, z]
  fov: 75,                  // Field of view
  controls: {
    minDistance: 5,         // Minimum zoom distance
    maxDistance: 12,        // Maximum zoom distance
    // ... other orbit controls
  }
}
```

#### Particle Effects
```javascript
particles: {
  enabled: true,
  count: 100,               // Number of particles
  size: 0.05,              // Particle size
  spread: 20,              // How spread out particles are
  colors: {
    min: [1, 0.5, 0.7],   // Minimum RGB values
    max: [1, 0.5, 1]      // Maximum RGB values
  }
}
```

### UI Configuration (`config.ui`)

#### Theme Colors
```javascript
colors: {
  primary: '#ff6ec7',      // Main accent color
  secondary: '#ff9472',    // Secondary accent
  background: {
    main: 'linear-gradient(...)',  // Main background
    overlay: 'rgba(0, 0, 0, 0.5)', // Overlay backgrounds
    glass: 'rgba(0, 0, 0, 0.7)'   // Glass effect
  }
}
```

### Performance Configuration (`config.performance`)

#### Level of Detail (LOD)
```javascript
lod: {
  high: {
    particleCount: 150,
    enablePhysics: true
  },
  medium: {
    particleCount: 100,
    enablePhysics: true
  },
  low: {
    particleCount: 50,
    enablePhysics: false
  }
}
```

### Feature Flags (`config.features`)
```javascript
features: {
  voice: true,              // Enable voice synthesis
  particles: true,          // Enable particle effects
  physics: true,           // Enable physics simulation
  debugMode: false,        // Enable debug mode
  experimentalFeatures: false
}
```

### Debug Settings (`config.debug`)
```javascript
debug: {
  logWebSocketMessages: false,  // Log WebSocket traffic
  logAnimationStates: false,    // Log animation changes
  logVoiceEvents: false,        // Log voice synthesis events
  slowMotion: false,           // Slow down animations
  slowMotionFactor: 0.5        // Speed multiplier
}
```

## Common Customizations

### 1. Change Backend URL
```javascript
// config.local.js
export default {
  api: {
    baseUrl: 'http://192.168.1.100:8000',
    websocketUrl: 'ws://192.168.1.100:8000'
  }
};
```

### 2. Reduce Particles for Performance
```javascript
// config.local.js
export default {
  visual: {
    particles: {
      count: 25  // Reduce from 100 to 25
    }
  }
};
```

### 3. Adjust Voice Settings
```javascript
// config.local.js
export default {
  voice: {
    defaultVolume: 1.0,
    waifuProfiles: {
      luna: {
        pitch: 1.5  // Make Luna's voice even higher
      }
    }
  }
};
```

### 4. Change Animation Intensities
```javascript
// config.local.js
export default {
  animation: {
    base: {
      breathingIntensity: 0.05,  // More pronounced breathing
      swayIntensity: 0.2         // More swaying
    }
  }
};
```

### 5. Enable Debug Features
```javascript
// config.local.js
export default {
  debug: {
    logWebSocketMessages: true,
    logVoiceEvents: true,
    showPerformanceStats: true
  }
};
```

### 6. Customize Colors
```javascript
// config.local.js
export default {
  ui: {
    colors: {
      primary: '#00ff00',     // Green theme
      secondary: '#00ffff'    // Cyan secondary
    }
  }
};
```

## Performance Tuning

### For Low-End Devices
```javascript
export default {
  visual: {
    particles: { count: 25 },
    waveDeformation: { enabled: false },
    mesh: {
      geometry: {
        widthSegments: 4,
        heightSegments: 8
      }
    }
  },
  features: {
    physics: false
  }
};
```

### For High-End Devices
```javascript
export default {
  visual: {
    particles: { count: 200 },
    mesh: {
      geometry: {
        widthSegments: 16,
        heightSegments: 32
      }
    }
  },
  performance: {
    targetFPS: 120
  }
};
```

## Development vs Production

The config automatically detects the environment:
```javascript
const isDevelopment = process.env.NODE_ENV === 'development';
```

Different settings are applied based on environment:
- Development: Fewer particles, debug features enabled
- Production: Full particle count, debug features disabled

## Environment Variables

You can also use environment variables:
```javascript
api: {
  baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000'
}
```

Create a `.env.local` file:
```
REACT_APP_API_URL=https://api.example.com
```

## Tips

1. **Test changes incrementally** - Change one section at a time
2. **Use the browser console** - Enable debug logging to see effects
3. **Monitor performance** - Use browser dev tools to check FPS
4. **Keep backups** - Save working configurations before major changes
5. **Document your changes** - Add comments explaining why you changed values

## Troubleshooting

### Changes not taking effect
1. Make sure you're editing `config.local.js`, not `config.js`
2. Restart the development server after changes
3. Clear browser cache if needed

### Performance issues
1. Reduce particle count
2. Disable wave deformation
3. Lower mesh segment counts
4. Disable physics features

### Voice not working
1. Check `voice.enabled` is true
2. Verify browser supports Web Speech API
3. Check console for voice-related errors
4. Try different `preferredVoices` settings
