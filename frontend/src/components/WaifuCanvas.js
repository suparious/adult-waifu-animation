import React, { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';
import { motion } from 'framer-motion';
import styled from 'styled-components';

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
function AnimatedWaifu({ modelId, animationState }) {
  const meshRef = useRef();
  const [texture, setTexture] = useState(null);
  const [modelData, setModelData] = useState(null);
  const [time, setTime] = useState(0);
  
  // Animation parameters based on state
  const animParams = useRef({
    breathingSpeed: 1,
    breathingIntensity: 0.02,
    swaySpeed: 0.5,
    swayIntensity: 0.1,
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
    
    // Base breathing
    animParams.current.breathingSpeed = 1 + intensity * 0.5;
    animParams.current.breathingIntensity = 0.02 + intensity * 0.03;
    
    // Emotion-specific parameters
    switch (emotion) {
      case 'happy':
        animParams.current.bounceSpeed = 2;
        animParams.current.bounceIntensity = 0.1 * intensity;
        break;
      case 'flirty':
        animParams.current.swaySpeed = 1;
        animParams.current.swayIntensity = 0.2 * intensity;
        break;
      case 'excited':
        animParams.current.bounceSpeed = 3;
        animParams.current.bounceIntensity = 0.15 * intensity;
        animParams.current.breathingSpeed = 2;
        break;
      case 'shy':
        animParams.current.swaySpeed = 0.3;
        animParams.current.swayIntensity = 0.05;
        animParams.current.breathingIntensity = 0.01;
        break;
      case 'seductive':
        animParams.current.swaySpeed = 0.8;
        animParams.current.swayIntensity = 0.25 * intensity;
        animParams.current.breathingSpeed = 0.8;
        animParams.current.breathingIntensity = 0.04;
        break;
      default:
        // Reset to neutral
        animParams.current.bounceSpeed = 0;
        animParams.current.bounceIntensity = 0;
    }
  }, [animationState]);

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
    mesh.rotation.y = Math.sin(time * 0.3) * 0.05;
  });

  // Create geometry with bones for more complex animation
  const geometry = new THREE.PlaneGeometry(3, 6, 8, 16);
  
  // Add wave deformation to vertices for cloth/hair physics
  useFrame((state) => {
    if (!meshRef.current) return;
    const positions = meshRef.current.geometry.attributes.position;
    const vertex = new THREE.Vector3();
    
    for (let i = 0; i < positions.count; i++) {
      vertex.fromBufferAttribute(positions, i);
      const waveX = Math.sin(vertex.y * 2 + time * 2) * 0.02;
      const waveY = Math.sin(vertex.x * 3 + time * 3) * 0.01;
      
      // Apply wave only to upper part (hair/clothes)
      if (vertex.y > 0) {
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
        side={THREE.DoubleSide}
        emissive="#ff6ec7"
        emissiveIntensity={0.1}
      />
    </mesh>
  );
}

// Main Canvas Component
function WaifuCanvas({ modelId, animationState }) {
  return (
    <CanvasContainer>
      <Canvas>
        <PerspectiveCamera makeDefault position={[0, 0, 8]} />
        <OrbitControls 
          enablePan={false}
          minDistance={5}
          maxDistance={12}
          minPolarAngle={Math.PI / 3}
          maxPolarAngle={Math.PI / 2}
        />
        
        {/* Lighting */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <pointLight position={[-5, 5, -5]} intensity={0.5} color="#ff6ec7" />
        
        {/* Background */}
        <color attach="background" args={['#1a0033']} />
        
        {/* Fog for depth */}
        <fog attach="fog" args={['#1a0033', 10, 30]} />
        
        {/* Animated Waifu */}
        <AnimatedWaifu modelId={modelId} animationState={animationState} />
        
        {/* Particle effects */}
        <ParticleField />
      </Canvas>
    </CanvasContainer>
  );
}

// Particle effects for ambiance
function ParticleField() {
  const particles = useRef();
  const particleCount = 100;
  
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  
  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 20;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
    
    colors[i * 3] = 1;
    colors[i * 3 + 1] = Math.random() * 0.5 + 0.5;
    colors[i * 3 + 2] = Math.random() * 0.5 + 0.7;
  }
  
  useFrame((state) => {
    if (!particles.current) return;
    particles.current.rotation.y += 0.001;
    particles.current.rotation.x += 0.0005;
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
      <pointsMaterial size={0.05} vertexColors sizeAttenuation={false} />
    </points>
  );
}

export default WaifuCanvas;
