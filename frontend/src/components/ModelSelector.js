import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const SelectorContainer = styled.div`
  position: relative;
`;

const CurrentModel = styled(motion.button)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 10px 20px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: #ff6ec7;
  }
`;

const ModelImage = styled.img`
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ff6ec7;
`;

const DropdownMenu = styled(motion.div)`
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  overflow: hidden;
  min-width: 250px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
`;

const ModelOption = styled(motion.div)`
  padding: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  
  &:last-child {
    border-bottom: none;
  }
  
  &:hover {
    background: rgba(255, 110, 199, 0.2);
  }
  
  ${props => props.$selected && `
    background: rgba(255, 110, 199, 0.3);
  `}
`;

const ModelInfo = styled.div`
  flex: 1;
`;

const ModelName = styled.div`
  font-weight: 600;
  font-size: 16px;
  color: white;
  margin-bottom: 4px;
`;

const ModelPersonality = styled.div`
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
`;

const ModelThumbnail = styled.img`
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  
  ${props => props.$selected && `
    border-color: #ff6ec7;
  `}
`;

const ArrowIcon = styled.span`
  display: inline-block;
  transition: transform 0.3s ease;
  ${props => props.$open && `transform: rotate(180deg);`}
`;

// Placeholder images for models
const modelImages = {
  luna: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9InVybCgjZ3JhZGllbnQxKSIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDEiIHgxPSIwIiB5MT0iMCIgeDI9IjQ4IiB5Mj0iNDgiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjZmY2ZWM3Ii8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iI2ZmOTQ3MiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPg==',
  sakura: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjQiIGZpbGw9InVybCgjZ3JhZGllbnQyKSIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDIiIHgxPSIwIiB5MT0iMCIgeDI9IjQ4IiB5Mj0iNDgiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjZmZiNmQ5Ii8+CjxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iI2ZmNjZhMyIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPg=='
};

function ModelSelector({ selectedModel, onModelChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [models, setModels] = useState([]);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/models');
      setModels(response.data.models);
    } catch (error) {
      console.error('Failed to fetch models:', error);
      // Fallback models for demo
      setModels([
        {
          id: 'luna',
          name: 'Luna',
          personality: 'Playful and flirty cyberpunk girl',
          image_path: modelImages.luna
        },
        {
          id: 'sakura',
          name: 'Sakura',
          personality: 'Sweet and shy girl who gets flustered easily',
          image_path: modelImages.sakura
        }
      ]);
    }
  };

  const handleModelSelect = (modelId) => {
    onModelChange(modelId);
    setIsOpen(false);
  };

  const currentModelData = models.find(m => m.id === selectedModel) || models[0];

  return (
    <SelectorContainer>
      <CurrentModel
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {currentModelData && (
          <>
            <ModelImage 
              src={modelImages[currentModelData.id] || currentModelData.image_path} 
              alt={currentModelData.name}
            />
            <span>{currentModelData.name}</span>
          </>
        )}
        <ArrowIcon $open={isOpen}>▼</ArrowIcon>
      </CurrentModel>
      
      <AnimatePresence>
        {isOpen && (
          <DropdownMenu
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {models.map((model) => (
              <ModelOption
                key={model.id}
                $selected={model.id === selectedModel}
                onClick={() => handleModelSelect(model.id)}
                whileHover={{ x: 5 }}
              >
                <ModelThumbnail
                  src={modelImages[model.id] || model.image_path}
                  alt={model.name}
                  $selected={model.id === selectedModel}
                />
                <ModelInfo>
                  <ModelName>{model.name}</ModelName>
                  <ModelPersonality>{model.personality}</ModelPersonality>
                </ModelInfo>
              </ModelOption>
            ))}
          </DropdownMenu>
        )}
      </AnimatePresence>
    </SelectorContainer>
  );
}

export default ModelSelector;
