import React, { useState, useEffect, useRef, useCallback } from 'react';
import styled from 'styled-components';
import WaifuCanvas from './components/WaifuCanvas';
import ChatInterface from './components/ChatInterface';
import ModelSelector from './components/ModelSelector';
import './App.css';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #1a0033 0%, #330066 100%);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
`;

const AnimationSection = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
`;

const ChatSection = styled.div`
  width: 400px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
`;

const Header = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(180deg, rgba(0,0,0,0.7) 0%, transparent 100%);
  z-index: 10;
`;

const Title = styled.h1`
  margin: 0;
  font-size: 24px;
  background: linear-gradient(45deg, #ff6ec7, #ff9472);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

function App() {
  const [selectedModel, setSelectedModel] = useState('luna');
  const [animationState, setAnimationState] = useState({
    emotion: 'neutral',
    action: 'idle',
    intensity: 0.5
  });
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);
  const clientIdRef = useRef(`client-${Date.now()}`);

  const connectWebSocket = useCallback(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientIdRef.current}`);
    
    ws.onopen = () => {
      console.log('Connected to server');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleServerMessage(data);
    };

    ws.onclose = () => {
      console.log('Disconnected from server');
      setIsConnected(false);
      // Attempt to reconnect after 3 seconds
      setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    wsRef.current = ws;
  }, []);

  useEffect(() => {
    // Connect to WebSocket
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connectWebSocket]);

  const handleServerMessage = (data) => {
    switch (data.type) {
      case 'connection':
        console.log('Connection established:', data.message);
        break;
      
      case 'response':
        // Add AI response to messages
        setMessages(prev => [...prev, {
          sender: 'waifu',
          text: data.message,
          timestamp: new Date(data.timestamp),
          emotion: data.emotion
        }]);
        
        // Update animation state
        if (data.animation) {
          setAnimationState(data.animation.state);
          // Handle animation sequence
          playAnimationSequence(data.animation.sequence);
        }
        break;
      
      case 'model_changed':
        setSelectedModel(data.model);
        break;
      
      case 'state':
        setAnimationState(data.state);
        break;
      
      default:
        console.log('Unknown message type:', data.type);
    }
  };

  const playAnimationSequence = async (sequence) => {
    for (const action of sequence) {
      setAnimationState(prev => ({
        ...prev,
        action: action.action,
        intensity: action.intensity
      }));
      
      // Wait for animation duration
      await new Promise(resolve => setTimeout(resolve, action.duration * 1000));
    }
  };

  const sendMessage = (message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Add user message to chat
      setMessages(prev => [...prev, {
        sender: 'user',
        text: message,
        timestamp: new Date()
      }]);

      // Send to server
      wsRef.current.send(JSON.stringify({
        type: 'chat',
        message: message
      }));
    }
  };

  const changeModel = (modelId) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'change_model',
        model: modelId
      }));
    }
  };

  return (
    <AppContainer>
      <AnimationSection>
        <Header>
          <Title>Waifu Animation Chat</Title>
          <ModelSelector 
            selectedModel={selectedModel}
            onModelChange={changeModel}
          />
        </Header>
        <WaifuCanvas 
          modelId={selectedModel}
          animationState={animationState}
        />
      </AnimationSection>
      <ChatSection>
        <ChatInterface 
          messages={messages}
          onSendMessage={sendMessage}
          isConnected={isConnected}
        />
      </ChatSection>
    </AppContainer>
  );
}

export default App;
