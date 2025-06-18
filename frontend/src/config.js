/**
 * Frontend Configuration
 * Central place for all frontend settings and parameters
 */

// Check if we're in development or production
const isDevelopment = process.env.NODE_ENV === 'development';

// Base configuration
const baseConfig = {
  // API Configuration
  api: {
    baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    websocketUrl: process.env.REACT_APP_WS_URL || 'ws://localhost:8000',
    endpoints: {
      models: '/api/models',
      systemInfo: '/api/system-info',
      websocket: '/ws'
    },
    timeout: 30000, // 30 seconds
    reconnectDelay: 3000, // 3 seconds
    maxReconnectAttempts: 10
  },

  // Animation Configuration
  animation: {
    // Base animation parameters
    base: {
      breathingSpeed: 1.0,
      breathingIntensity: 0.02,
      swaySpeed: 0.5,
      swayIntensity: 0.1,
      idleRotationSpeed: 0.3,
      idleRotationAmount: 0.05
    },
    
    // Emotion-specific animation parameters
    emotions: {
      neutral: {
        breathingSpeed: 1.0,
        breathingIntensity: 0.02,
        bounceSpeed: 0,
        bounceIntensity: 0
      },
      happy: {
        breathingSpeed: 1.5,
        breathingIntensity: 0.03,
        bounceSpeed: 2,
        bounceIntensity: 0.1,
        swayIntensity: 0.15
      },
      shy: {
        breathingSpeed: 0.8,
        breathingIntensity: 0.01,
        swaySpeed: 0.3,
        swayIntensity: 0.05
      },
      flirty: {
        breathingSpeed: 1.2,
        breathingIntensity: 0.025,
        swaySpeed: 1.0,
        swayIntensity: 0.2
      },
      excited: {
        breathingSpeed: 2.0,
        breathingIntensity: 0.04,
        bounceSpeed: 3,
        bounceIntensity: 0.15
      },
      seductive: {
        breathingSpeed: 0.8,
        breathingIntensity: 0.04,
        swaySpeed: 0.8,
        swayIntensity: 0.25
      },
      affectionate: {
        breathingSpeed: 1.0,
        breathingIntensity: 0.03,
        swaySpeed: 0.6,
        swayIntensity: 0.1
      }
    },
    
    // Speaking animation
    speaking: {
      breathingMultiplier: 1.3,
      intensityMultiplier: 1.2,
      headBobSpeed: 8,
      headBobAmount: 0.01,
      headRotationSpeed: 6,
      headRotationAmount: 0.02,
      emissiveIntensity: 0.2
    },
    
    // Animation timing
    timing: {
      transitionDuration: 1000, // ms
      sequenceDelay: 100, // ms between sequence steps
      defaultActionDuration: 2000 // ms
    }
  },

  // Voice Configuration
  voice: {
    // Default settings
    enabled: true,
    defaultVolume: 0.8,
    
    // Waifu-specific base voice parameters
    waifuProfiles: {
      luna: {
        rate: 1.1,
        pitch: 1.3,
        preferredVoices: ['female', 'woman', 'girl', 'Google UK English Female', 'Microsoft Zira'],
        fallbackLang: 'en-US'
      },
      sakura: {
        rate: 0.9,
        pitch: 1.2,
        preferredVoices: ['female', 'woman', 'Google US English', 'Microsoft Haruka', 'Kyoko'],
        fallbackLang: 'en-US'
      }
    },
    
    // Emotion modifiers for voice
    emotionModifiers: {
      neutral: { rateMultiplier: 1.0, pitchMultiplier: 1.0, volumeMultiplier: 1.0 },
      happy: { rateMultiplier: 1.1, pitchMultiplier: 1.1, volumeMultiplier: 1.0 },
      shy: { rateMultiplier: 0.9, pitchMultiplier: 0.95, volumeMultiplier: 0.7 },
      flirty: { rateMultiplier: 0.95, pitchMultiplier: 1.05, volumeMultiplier: 0.9 },
      excited: { rateMultiplier: 1.2, pitchMultiplier: 1.15, volumeMultiplier: 1.1 },
      seductive: { rateMultiplier: 0.8, pitchMultiplier: 0.9, volumeMultiplier: 0.8 },
      affectionate: { rateMultiplier: 0.95, pitchMultiplier: 1.0, volumeMultiplier: 0.85 }
    },
    
    // Voice visualization
    visualization: {
      waveformBars: 8,
      waveformWidth: 200,
      waveformHeight: 200,
      baseBarHeight: 40,
      barHeightVariation: 20,
      animationSpeed: 0.5,
      amplitudeRange: [1.5, 2.0]
    }
  },

  // Visual/3D Configuration
  visual: {
    // Camera settings
    camera: {
      position: [0, 0, 8],
      fov: 75,
      near: 0.1,
      far: 1000,
      controls: {
        enablePan: false,
        minDistance: 5,
        maxDistance: 12,
        minPolarAngle: Math.PI / 3,
        maxPolarAngle: Math.PI / 2
      }
    },
    
    // Lighting
    lighting: {
      ambient: {
        intensity: 0.5,
        color: '#ffffff'
      },
      directional: {
        position: [5, 5, 5],
        intensity: 1,
        color: '#ffffff'
      },
      point: {
        position: [-5, 5, -5],
        intensity: 0.5,
        color: '#ff6ec7'
      }
    },
    
    // Scene settings
    scene: {
      backgroundColor: '#1a0033',
      fog: {
        color: '#1a0033',
        near: 10,
        far: 30
      }
    },
    
    // Waifu mesh settings
    mesh: {
      geometry: {
        width: 3,
        height: 6,
        widthSegments: 8,
        heightSegments: 16
      },
      material: {
        emissiveColor: '#ff6ec7',
        defaultEmissiveIntensity: 0.1,
        side: 'double' // 'front', 'back', or 'double'
      }
    },
    
    // Particle effects
    particles: {
      enabled: true,
      count: isDevelopment ? 50 : 100, // Fewer particles in dev for performance
      size: 0.05,
      spread: 20,
      rotationSpeed: 0.001,
      colors: {
        min: [1, 0.5, 0.7],
        max: [1, 0.5, 1]
      }
    },
    
    // Wave deformation (for hair/cloth physics)
    waveDeformation: {
      enabled: true,
      amplitudeX: 0.02,
      amplitudeY: 0.01,
      frequencyX: 2,
      frequencyY: 3,
      speed: 2,
      upperBodyThreshold: 0 // Y position above which deformation applies
    }
  },

  // UI Configuration
  ui: {
    // Theme colors
    colors: {
      primary: '#ff6ec7',
      secondary: '#ff9472',
      tertiary: '#9f7aea',
      background: {
        main: 'linear-gradient(135deg, #1a0033 0%, #330066 100%)',
        overlay: 'rgba(0, 0, 0, 0.5)',
        glass: 'rgba(0, 0, 0, 0.7)'
      },
      text: {
        primary: '#ffffff',
        secondary: 'rgba(255, 255, 255, 0.8)',
        muted: 'rgba(255, 255, 255, 0.6)'
      }
    },
    
    // Layout
    layout: {
      chatWidth: 400,
      headerHeight: 80,
      animationSectionFlex: 1,
      borderRadius: {
        small: 8,
        medium: 15,
        large: 20
      },
      spacing: {
        small: 10,
        medium: 15,
        large: 20
      }
    },
    
    // Animations
    animations: {
      transitionDuration: '0.3s',
      hoverScale: 1.05,
      glassBlur: 10
    },
    
    // Voice controls
    voiceControls: {
      position: {
        bottom: 20,
        right: 20
      },
      volumeSliderWidth: 80
    }
  },

  // Performance Configuration
  performance: {
    // Frame rate
    targetFPS: 60,
    
    // Level of detail
    lod: {
      high: {
        particleCount: 150,
        meshSegments: { width: 8, height: 16 },
        enablePhysics: true,
        enableWaveDeformation: true
      },
      medium: {
        particleCount: 100,
        meshSegments: { width: 6, height: 12 },
        enablePhysics: true,
        enableWaveDeformation: true
      },
      low: {
        particleCount: 50,
        meshSegments: { width: 4, height: 8 },
        enablePhysics: false,
        enableWaveDeformation: false
      }
    },
    
    // Auto-adjust based on performance
    autoAdjust: true,
    fpsThreshold: 30, // Switch to lower LOD if FPS drops below this
    measurementInterval: 5000 // Check performance every 5 seconds
  },

  // Feature Flags
  features: {
    voice: true,
    particles: true,
    physics: true,
    waveDeformation: true,
    debugMode: isDevelopment,
    showFPS: isDevelopment,
    experimentalFeatures: false
  },

  // Development/Debug Settings
  debug: {
    logWebSocketMessages: isDevelopment,
    logAnimationStates: false,
    logVoiceEvents: false,
    showPerformanceStats: isDevelopment,
    mockResponses: false, // Use mock responses when backend is down
    slowMotion: false, // Slow down animations for debugging
    slowMotionFactor: 0.5
  }
};

// Attempt to load local overrides
let localConfig = {};
try {
  // This will fail in production builds, which is fine
  localConfig = require('./config.local.js').default || {};
} catch (e) {
  // No local config found, use defaults
}

// Deep merge function
function deepMerge(target, source) {
  const output = { ...target };
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach(key => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          Object.assign(output, { [key]: source[key] });
        } else {
          output[key] = deepMerge(target[key], source[key]);
        }
      } else {
        Object.assign(output, { [key]: source[key] });
      }
    });
  }
  return output;
}

function isObject(item) {
  return item && typeof item === 'object' && !Array.isArray(item);
}

// Merge base config with local overrides
const config = deepMerge(baseConfig, localConfig);

// Freeze the config to prevent accidental mutations
function deepFreeze(obj) {
  Object.freeze(obj);
  Object.getOwnPropertyNames(obj).forEach(prop => {
    if (obj[prop] !== null && (typeof obj[prop] === 'object' || typeof obj[prop] === 'function') && !Object.isFrozen(obj[prop])) {
      deepFreeze(obj[prop]);
    }
  });
  return obj;
}

// Export frozen config
export default deepFreeze(config);

// Export individual sections for convenience
export const { api, animation, voice, visual, ui, performance, features, debug } = config;
