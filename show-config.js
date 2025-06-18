#!/usr/bin/env node
/**
 * Test script to demonstrate frontend configuration usage
 * Run this to see all available configuration options
 */

// Note: This is a demonstration script to show config structure
// The actual config is used in the React app

const config = {
  // API Configuration
  api: {
    baseUrl: 'http://localhost:8000',
    websocketUrl: 'ws://localhost:8000',
    reconnectDelay: 3000
  },

  // Animation Parameters
  animation: {
    base: {
      breathingSpeed: 1.0,
      breathingIntensity: 0.02,
      swaySpeed: 0.5,
      swayIntensity: 0.1
    },
    emotions: {
      happy: { bounceSpeed: 2, bounceIntensity: 0.1 },
      shy: { swaySpeed: 0.3, breathingIntensity: 0.01 },
      flirty: { swaySpeed: 1.0, swayIntensity: 0.2 },
      excited: { bounceSpeed: 3, breathingSpeed: 2.0 },
      seductive: { breathingSpeed: 0.8, swayIntensity: 0.25 }
    }
  },

  // Voice Configuration
  voice: {
    enabled: true,
    defaultVolume: 0.8,
    waifuProfiles: {
      luna: { rate: 1.1, pitch: 1.3 },
      sakura: { rate: 0.9, pitch: 1.2 }
    }
  },

  // Visual Settings
  visual: {
    particles: {
      count: 100,
      size: 0.05,
      spread: 20
    },
    mesh: {
      geometry: {
        width: 3,
        height: 6,
        widthSegments: 8,
        heightSegments: 16
      }
    }
  },

  // UI Theme
  ui: {
    colors: {
      primary: '#ff6ec7',
      secondary: '#ff9472',
      tertiary: '#9f7aea'
    }
  }
};

console.log('🎮 Waifu Animation Chat - Frontend Configuration Demo\n');
console.log('📁 Configuration Structure:\n');

// Display config sections
Object.keys(config).forEach(section => {
  console.log(`📌 ${section.toUpperCase()}`);
  console.log(JSON.stringify(config[section], null, 2));
  console.log('');
});

console.log('💡 To customize your settings:\n');
console.log('1. Copy frontend/src/config.local.js.example to config.local.js');
console.log('2. Edit config.local.js with your preferred values');
console.log('3. Restart the frontend server\n');

console.log('📝 Example custom config.local.js:\n');
console.log(`export default {
  // Use a different backend server
  api: {
    baseUrl: 'http://192.168.1.100:8000',
    websocketUrl: 'ws://192.168.1.100:8000'
  },
  
  // Reduce particles for better performance
  visual: {
    particles: {
      count: 25
    }
  },
  
  // Make Luna's voice even higher pitched
  voice: {
    waifuProfiles: {
      luna: {
        pitch: 1.5
      }
    }
  },
  
  // Enable debug logging
  debug: {
    logWebSocketMessages: true,
    logVoiceEvents: true
  }
};`);

console.log('\n✅ Configuration system ready to use!');
console.log('📖 See docs/FRONTEND_CONFIG.md for complete documentation\n');
