import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }
`;

const Message = styled(motion.div)`
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  word-wrap: break-word;
  
  ${props => props.$sender === 'user' ? `
    align-self: flex-end;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 4px;
  ` : `
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    color: white;
    border-bottom-left-radius: 4px;
    border: 1px solid rgba(255, 110, 199, 0.3);
  `}
`;

const EmotionIndicator = styled.span`
  display: inline-block;
  margin-left: 8px;
  font-size: 14px;
  opacity: 0.8;
`;

const InputContainer = styled.form`
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  gap: 10px;
`;

const TextInput = styled.input`
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 12px 20px;
  color: white;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
  
  &:focus {
    background: rgba(255, 255, 255, 0.15);
    border-color: #ff6ec7;
    box-shadow: 0 0 0 2px rgba(255, 110, 199, 0.2);
  }
`;

const SendButton = styled(motion.button)`
  background: linear-gradient(135deg, #ff6ec7 0%, #ff9472 100%);
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  outline: none;
  color: white;
  font-size: 20px;
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const ConnectionStatus = styled.div`
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  opacity: 0.7;
`;

const StatusDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => props.$connected ? '#4ade80' : '#ef4444'};
  animation: ${props => props.$connected ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  align-self: flex-start;
  
  span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    animation: typing 1.4s infinite;
    
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
  
  @keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
  }
`;

// Emotion to emoji mapping
const emotionEmojis = {
  happy: '😊',
  shy: '😳',
  flirty: '😉',
  excited: '🤗',
  affectionate: '🥰',
  playful: '😜',
  seductive: '😏',
  neutral: '😌'
};

function ChatInterface({ messages, onSendMessage, isConnected }) {
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (inputValue.trim() && isConnected) {
      onSendMessage(inputValue);
      setInputValue('');
      
      // Show typing indicator
      setIsTyping(true);
      setTimeout(() => setIsTyping(false), 2000 + Math.random() * 2000);
    }
  };

  return (
    <ChatContainer>
      <ConnectionStatus>
        <StatusDot $connected={isConnected} />
        {isConnected ? 'Connected' : 'Disconnected'}
      </ConnectionStatus>
      
      <MessagesContainer>
        <AnimatePresence>
          {messages.map((message, index) => (
            <Message
              key={index}
              $sender={message.sender}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {message.text}
              {message.sender === 'waifu' && message.emotion && (
                <EmotionIndicator>
                  {emotionEmojis[message.emotion] || emotionEmojis.neutral}
                </EmotionIndicator>
              )}
            </Message>
          ))}
          
          {isTyping && (
            <TypingIndicator
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <span />
              <span />
              <span />
            </TypingIndicator>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </MessagesContainer>
      
      <InputContainer onSubmit={handleSubmit}>
        <TextInput
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          disabled={!isConnected}
        />
        <SendButton
          type="submit"
          disabled={!isConnected || !inputValue.trim()}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          ➤
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
}

export default ChatInterface;
