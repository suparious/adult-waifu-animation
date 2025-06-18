import React, { useState, useEffect, useRef, useCallback } from 'react';
import styled from 'styled-components';
import WaifuCanvas from './components/WaifuCanvas';
import ChatInterface from './components/ChatInterface';
import ModelSelector from './components/ModelSelector';
import VoiceSynthesis from './components/VoiceSynthesis';
import config from './config';
import './App.css';

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  background: ${config.ui.colors.background.main};
  color: ${config.ui.colors.text.primary};
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
`;

const AnimationSection = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
`;

const ChatSection = styled.div`
  width: ${config.ui.layout.chatWidth}px;
  background: ${config.ui.colors.background.overlay};
  backdrop-filter: blur(${config.ui.animations.glassBlur}px);
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
  background: linear-gradient(180deg, ${config.ui.colors.background.glass} 0%, transparent 100%);
  z-index: 10;
`;

const Title = styled.h1`
  margin: 0;
  font-size: 24px;
  background: linear-gradient(45deg, ${config.ui.colors.primary}, ${config.ui.colors.secondary});
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const TitleSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

const SystemInfo = styled.div`
  font-size: 12px;
  color: ${config.ui.colors.text.muted};
  font-weight: normal;
  display: flex;
  gap: 8px;
  align-items: center;
  
  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .provider {
    color: ${config.ui.colors.secondary};
    font-weight: 500;
  }
  
  .model {
    color: ${config.ui.colors.primary};
  }
  
  .version {
    color: ${config.ui.colors.tertiary};
    font-size: 11px;
    opacity: 0.8;
  }
  
  .separator {
    opacity: 0.3;
  }
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
  const [systemInfo, setSystemInfo] = useState(null);
  const [lastWaifuMessage, setLastWaifuMessage] = useState(null);
  const [currentEmotion, setCurrentEmotion] = useState('neutral');
  const [waifuPersonality, setWaifuPersonality] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const wsRef = useRef(null);
  const clientIdRef = useRef(`client-${Date.now()}`);

  // Fetch system info
  useEffect(() => {
  const fetchSystemInfo = async () => {
  try {
  const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.systemInfo}`);
  const data = await response.json();
  setSystemInfo(data);
  } catch (error) {
  console.error('Failed to fetch system info:', error);
  }
  };
  
  fetchSystemInfo();
  // Refresh system info every 60 seconds
  const interval = setInterval(fetchSystemInfo, 60000);
  
  return () => clearInterval(interval);
  }, []);

  const connectWebSocket = useCallback(() => {
    const wsUrl = `${config.api.websocketUrl}${config.api.endpoints.websocket}/${clientIdRef.current}`;
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      if (config.debug.logWebSocketMessages) {
        console.log('Connected to server');
      }
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (config.debug.logWebSocketMessages) {
        console.log('WS Message:', data);
      }
      handleServerMessage(data);
    };

    ws.onclose = () => {
      if (config.debug.logWebSocketMessages) {
        console.log('Disconnected from server');
      }
      setIsConnected(false);
      // Attempt to reconnect after configured delay
      setTimeout(connectWebSocket, config.api.reconnectDelay);
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
        const waifuMessage = {
          sender: 'waifu',
          text: data.message,
          timestamp: new Date(data.timestamp),
          emotion: data.emotion
        };
        setMessages(prev => [...prev, waifuMessage]);
        setLastWaifuMessage(waifuMessage);
        setCurrentEmotion(data.emotion || 'neutral');
        
        // Update animation state
        if (data.animation) {
          setAnimationState(data.animation.state);
          // Handle animation sequence
          playAnimationSequence(data.animation.sequence);
        }
        break;
      
      case 'model_changed':
        setSelectedModel(data.model);
        // Fetch model personality when changed
        fetchWaifuPersonality(data.model);
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

  const fetchWaifuPersonality = async (modelId) => {
    try {
      const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.models}/${modelId}`);
      const data = await response.json();
      if (!data.error) {
        setWaifuPersonality(data.personality);
      }
    } catch (error) {
      console.error('Failed to fetch waifu personality:', error);
    }
  };

  // Fetch initial waifu personality
  useEffect(() => {
    fetchWaifuPersonality(selectedModel);
  }, [selectedModel]);

  return (
    <AppContainer>
      <AnimationSection>
        <Header>
          <TitleSection>
            <Title>Waifu Animation Chat</Title>
            {systemInfo ? (
              <SystemInfo>
                <span className="provider">
                  🤖 {systemInfo.llm.provider}
                </span>
                <span className="separator">•</span>
                <span className="model">
                  {systemInfo.llm.model_display}
                </span>
                <span className="separator">•</span>
                <span className="version">
                  v{systemInfo.version}
                </span>
              </SystemInfo>
            ) : (
              <SystemInfo>
                <span style={{ opacity: 0.5 }}>Loading system info...</span>
              </SystemInfo>
            )}
          </TitleSection>
          <ModelSelector 
            selectedModel={selectedModel}
            onModelChange={changeModel}
          />
        </Header>
        <WaifuCanvas 
          modelId={selectedModel}
          animationState={animationState}
          isSpeaking={isSpeaking}
        />
        <VoiceSynthesis
          message={lastWaifuMessage}
          waifuId={selectedModel}
          emotion={currentEmotion}
          waifuPersonality={waifuPersonality}
          onSpeakingChange={setIsSpeaking}
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
