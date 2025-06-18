import React, { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import config from '../config';

const CanvasContainer = styled.div`
  flex: 1;
  position: relative;
  overflow: hidden;
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  z-index: 100;
`;

// Animated Waifu Mesh Component
function AnimatedWaifu({ modelId, animationState, isSpeaking }) {
  const meshRef = useRef();
  const [texture, setTexture] = useState(null);
  const [modelData, setModelData] = useState(null);
  const [time, setTime] = useState(0);
  
  // Animation parameters based on state
  const animParams = useRef({
    breathingSpeed: config.animation.base.breathingSpeed,
    breathingIntensity: config.animation.base.breathingIntensity,
    swaySpeed: config.animation.base.swaySpeed,
    swayIntensity: config.animation.base.swayIntensity,
    bounceSpeed: 0,
    bounceIntensity: 0
  });

  // Fetch model data
  useEffect(() => {
    fetch(`http://localhost:8000/api/models/${modelId}`)
      .then(res => res.json())
      .then(data => {
        if (!data.error) {
          setModelData(data);
        }
      })
      .catch(err => console.error('Failed to load model data:', err));
  }, [modelId]);

  // Load texture from actual image
  useEffect(() => {
    if (!modelData || !modelData.image_path) {
      // Create fallback texture immediately
      createFallbackTexture();
      return;
    }
    
    const loader = new THREE.TextureLoader();
    
    // Load the actual waifu image
    loader.load(
      modelData.image_path,
      // Success callback
      (loadedTexture) => {
        loadedTexture.minFilter = THREE.LinearFilter;
        loadedTexture.magFilter = THREE.LinearFilter;
        loadedTexture.format = THREE.RGBAFormat;
        setTexture(loadedTexture);
      },
      // Progress callback
      undefined,
      // Error callback
      (error) => {
        console.error('Failed to load texture:', error);
        createFallbackTexture();
      }
    );
  }, [modelData, modelId]);
  
  const createFallbackTexture = () => {
    // Create fallback gradient texture
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 1024;
    const ctx = canvas.getContext('2d');
    
    // Create a stylized waifu silhouette based on model colors
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    
    // Use model-specific colors if available
    const primaryColor = modelId === 'sakura' ? '#ffb6d9' : '#ff6ec7';
    const secondaryColor = modelId === 'sakura' ? '#ff66a3' : '#ff9472';
    
    gradient.addColorStop(0, primaryColor);
    gradient.addColorStop(0.5, secondaryColor);
    gradient.addColorStop(1, primaryColor);
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Add silhouette
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.beginPath();
    ctx.ellipse(256, 200, 80, 100, 0, 0, Math.PI * 2);
    ctx.fill();
    
    // Add character name
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.font = '48px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(modelData?.name || 'Waifu', 256, 512);
    
    const fallbackTexture = new THREE.CanvasTexture(canvas);
    setTexture(fallbackTexture);
  };

  // Update animation parameters based on state
  useEffect(() => {
    const { emotion, intensity } = animationState;
    const emotionConfig = config.animation.emotions[emotion] || config.animation.emotions.neutral;
    
    // Apply emotion-specific parameters
    Object.keys(emotionConfig).forEach(key => {
      if (key in animParams.current) {
        animParams.current[key] = emotionConfig[key];
      }
    });
    
    // Apply intensity scaling for certain parameters
    if (emotionConfig.bounceIntensity !== undefined) {
      animParams.current.bounceIntensity = emotionConfig.bounceIntensity * intensity;
    }
    if (emotionConfig.swayIntensity !== undefined) {
      animParams.current.swayIntensity = emotionConfig.swayIntensity * intensity;
    }

    // Add speaking animation modifiers
    if (isSpeaking) {
      animParams.current.breathingSpeed *= config.animation.speaking.breathingMultiplier;
      animParams.current.breathingIntensity *= config.animation.speaking.intensityMultiplier;
    }
  }, [animationState, isSpeaking]);

  // Animation loop
  useFrame((state, delta) => {
    if (!meshRef.current) return;
    
    setTime(t => t + delta);
    const mesh = meshRef.current;
    const params = animParams.current;
    
    // Breathing animation (scale)
    const breathing = Math.sin(time * params.breathingSpeed) * params.breathingIntensity;
    mesh.scale.y = 1 + breathing;
    mesh.scale.x = 1 - breathing * 0.5; // Inverse for natural look
    
    // Sway animation (rotation)
    const sway = Math.sin(time * params.swaySpeed) * params.swayIntensity;
    mesh.rotation.z = sway;
    
    // Bounce animation (position)
    if (params.bounceSpeed > 0) {
      const bounce = Math.abs(Math.sin(time * params.bounceSpeed)) * params.bounceIntensity;
      mesh.position.y = bounce;
    }
    
    // Subtle idle animation
    mesh.rotation.y = Math.sin(time * config.animation.base.idleRotationSpeed) * config.animation.base.idleRotationAmount;
    
    // Speaking animation - subtle head movement
    if (isSpeaking) {
      const speakBob = Math.sin(time * config.animation.speaking.headBobSpeed) * config.animation.speaking.headBobAmount;
      mesh.position.y += speakBob;
      mesh.rotation.x = Math.sin(time * config.animation.speaking.headRotationSpeed) * config.animation.speaking.headRotationAmount;
    }
  });

  // Create geometry with bones for more complex animation
  const geometry = new THREE.PlaneGeometry(
    config.visual.mesh.geometry.width,
    config.visual.mesh.geometry.height,
    config.visual.mesh.geometry.widthSegments,
    config.visual.mesh.geometry.heightSegments
  );
  
  // Add wave deformation to vertices for cloth/hair physics
  useFrame((state) => {
    if (!meshRef.current || !config.visual.waveDeformation.enabled) return;
    const positions = meshRef.current.geometry.attributes.position;
    const vertex = new THREE.Vector3();
    
    for (let i = 0; i < positions.count; i++) {
      vertex.fromBufferAttribute(positions, i);
      const waveX = Math.sin(vertex.y * config.visual.waveDeformation.frequencyX + time * config.visual.waveDeformation.speed) * config.visual.waveDeformation.amplitudeX;
      const waveY = Math.sin(vertex.x * config.visual.waveDeformation.frequencyY + time * config.visual.waveDeformation.speed) * config.visual.waveDeformation.amplitudeY;
      
      // Apply wave only to upper part (hair/clothes)
      if (vertex.y > config.visual.waveDeformation.upperBodyThreshold) {
        positions.setXYZ(i, vertex.x + waveX, vertex.y + waveY, vertex.z);
      }
    }
    
    positions.needsUpdate = true;
  });

  if (!texture) return null;

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial 
        map={texture}
        transparent
        side={config.visual.mesh.material.side === 'double' ? THREE.DoubleSide : 
              config.visual.mesh.material.side === 'front' ? THREE.FrontSide : THREE.BackSide}
        emissive={config.visual.mesh.material.emissiveColor}
        emissiveIntensity={isSpeaking ? config.animation.speaking.emissiveIntensity : config.visual.mesh.material.defaultEmissiveIntensity}
      />
    </mesh>
  );
}

// Main Canvas Component
function WaifuCanvas({ modelId, animationState, isSpeaking }) {
  return (
    <CanvasContainer>
      <Canvas>
        <PerspectiveCamera 
          makeDefault 
          position={config.visual.camera.position} 
          fov={config.visual.camera.fov}
          near={config.visual.camera.near}
          far={config.visual.camera.far}
        />
        <OrbitControls 
          enablePan={config.visual.camera.controls.enablePan}
          minDistance={config.visual.camera.controls.minDistance}
          maxDistance={config.visual.camera.controls.maxDistance}
          minPolarAngle={config.visual.camera.controls.minPolarAngle}
          maxPolarAngle={config.visual.camera.controls.maxPolarAngle}
        />
        
        {/* Lighting */}
        <ambientLight 
          intensity={config.visual.lighting.ambient.intensity} 
          color={config.visual.lighting.ambient.color}
        />
        <directionalLight 
          position={config.visual.lighting.directional.position} 
          intensity={config.visual.lighting.directional.intensity}
          color={config.visual.lighting.directional.color}
        />
        <pointLight 
          position={config.visual.lighting.point.position} 
          intensity={config.visual.lighting.point.intensity} 
          color={config.visual.lighting.point.color}
        />
        
        {/* Background */}
        <color attach="background" args={[config.visual.scene.backgroundColor]} />
        
        {/* Fog for depth */}
        <fog 
          attach="fog" 
          args={[
            config.visual.scene.fog.color, 
            config.visual.scene.fog.near, 
            config.visual.scene.fog.far
          ]} 
        />
        
        {/* Animated Waifu */}
        <AnimatedWaifu modelId={modelId} animationState={animationState} isSpeaking={isSpeaking} />
        
        {/* Particle effects */}
        {config.features.particles && <ParticleField />}
      </Canvas>
    </CanvasContainer>
  );
}

// Particle effects for ambiance
function ParticleField() {
  const particles = useRef();
  const particleCount = config.visual.particles.count;
  
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  
  for (let i = 0; i < particleCount; i++) {
    const spread = config.visual.particles.spread;
    positions[i * 3] = (Math.random() - 0.5) * spread;
    positions[i * 3 + 1] = (Math.random() - 0.5) * spread;
    positions[i * 3 + 2] = (Math.random() - 0.5) * spread;
    
    const [minR, minG, minB] = config.visual.particles.colors.min;
    const [maxR, maxG, maxB] = config.visual.particles.colors.max;
    
    colors[i * 3] = minR + Math.random() * (maxR - minR);
    colors[i * 3 + 1] = minG + Math.random() * (maxG - minG);
    colors[i * 3 + 2] = minB + Math.random() * (maxB - minB);
  }
  
  useFrame((state) => {
    if (!particles.current) return;
    const rotSpeed = config.visual.particles.rotationSpeed;
    particles.current.rotation.y += rotSpeed;
    particles.current.rotation.x += rotSpeed * 0.5;
  });
  
  return (
    <points ref={particles}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={particleCount}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial 
        size={config.visual.particles.size} 
        vertexColors 
        sizeAttenuation={false} 
      />
    </points>
  );
}

export default WaifuCanvas;
