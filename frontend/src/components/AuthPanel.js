import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import config from '../config';

const AuthContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const AuthCard = styled.div`
  background: ${config.ui.colors.background.glass};
  backdrop-filter: blur(20px);
  border-radius: ${config.ui.layout.borderRadius.large}px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const Title = styled.h2`
  margin: 0 0 10px 0;
  font-size: 28px;
  background: linear-gradient(45deg, ${config.ui.colors.primary}, ${config.ui.colors.secondary});
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
`;

const Subtitle = styled.p`
  margin: 0 0 30px 0;
  color: ${config.ui.colors.text.muted};
  text-align: center;
  font-size: 14px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  font-size: 14px;
  color: ${config.ui.colors.text.secondary};
`;

const Input = styled.input`
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: ${config.ui.layout.borderRadius.small}px;
  padding: 12px 16px;
  font-size: 16px;
  color: ${config.ui.colors.text.primary};
  transition: all ${config.ui.animations.transitionDuration};
  
  &:focus {
    outline: none;
    border-color: ${config.ui.colors.primary};
    box-shadow: 0 0 0 3px rgba(255, 110, 199, 0.2);
  }
  
  &::placeholder {
    color: ${config.ui.colors.text.muted};
  }
`;

const Button = styled.button`
  background: linear-gradient(45deg, ${config.ui.colors.primary}, ${config.ui.colors.secondary});
  border: none;
  border-radius: ${config.ui.layout.borderRadius.small}px;
  padding: 14px 24px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all ${config.ui.animations.transitionDuration};
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(255, 110, 199, 0.4);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const GuestButton = styled.button`
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: ${config.ui.layout.borderRadius.small}px;
  padding: 12px 24px;
  font-size: 14px;
  color: ${config.ui.colors.text.secondary};
  cursor: pointer;
  transition: all ${config.ui.animations.transitionDuration};
  
  &:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.3);
  }
`;

const ErrorMessage = styled.div`
  background: rgba(255, 100, 100, 0.1);
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: ${config.ui.layout.borderRadius.small}px;
  padding: 12px;
  color: #ff6b6b;
  font-size: 14px;
  text-align: center;
`;

const SuccessMessage = styled.div`
  background: rgba(100, 255, 150, 0.1);
  border: 1px solid rgba(100, 255, 150, 0.3);
  border-radius: ${config.ui.layout.borderRadius.small}px;
  padding: 12px;
  color: #6bff9b;
  font-size: 14px;
  text-align: center;
`;

const Divider = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  color: ${config.ui.colors.text.muted};
  font-size: 12px;
  
  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
  }
`;

const Link = styled.a`
  color: ${config.ui.colors.primary};
  text-decoration: none;
  font-size: 14px;
  text-align: center;
  display: block;
  margin-top: 20px;
  
  &:hover {
    text-decoration: underline;
  }
`;

const UserInfo = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: ${config.ui.layout.borderRadius.small}px;
  padding: 15px;
  margin-bottom: 20px;
  
  .name {
    font-weight: 600;
    color: ${config.ui.colors.text.primary};
  }
  
  .tier {
    font-size: 12px;
    color: ${config.ui.colors.secondary};
    text-transform: uppercase;
  }
`;

function AuthPanel({ onAuthenticated, onGuestMode, isVisible }) {
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  // Check for stored session on mount
  useEffect(() => {
    const storedSession = localStorage.getItem('waifu_session');
    if (storedSession) {
      try {
        const session = JSON.parse(storedSession);
        if (session.expires_at && new Date(session.expires_at) > new Date()) {
          onAuthenticated(session);
        } else {
          localStorage.removeItem('waifu_session');
        }
      } catch (e) {
        localStorage.removeItem('waifu_session');
      }
    }
  }, [onAuthenticated]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${config.api.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ api_key: apiKey }),
      });
      
      const data = await response.json();
      
      if (response.ok && data.session_token) {
        setSuccess('Authentication successful!');
        localStorage.setItem('waifu_session', JSON.stringify(data));
        setTimeout(() => onAuthenticated(data), 1000);
      } else {
        setError(data.error || 'Invalid API key. Please check and try again.');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleGuestMode = () => {
    const guestSession = {
      session_token: `guest-${Date.now()}`,
      user: {
        user_id: 'guest',
        name: 'Guest User',
        subscription_tier: 'free'
      },
      is_guest: true
    };
    localStorage.setItem('waifu_session', JSON.stringify(guestSession));
    onGuestMode(guestSession);
  };
  
  if (!isVisible) return null;
  
  return (
    <AuthContainer>
      <AuthCard>
        <Title>Welcome Back</Title>
        <Subtitle>Enter your API key to continue with your saved data</Subtitle>
        
        <Form onSubmit={handleSubmit}>
          <InputGroup>
            <Label htmlFor="apiKey">API Key</Label>
            <Input
              id="apiKey"
              type="password"
              placeholder="srt_prod_xxxxxxxx"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              disabled={isLoading}
            />
          </InputGroup>
          
          {error && <ErrorMessage>{error}</ErrorMessage>}
          {success && <SuccessMessage>{success}</SuccessMessage>}
          
          <Button type="submit" disabled={isLoading || !apiKey}>
            {isLoading ? 'Authenticating...' : 'Login'}
          </Button>
          
          <Divider>or</Divider>
          
          <GuestButton type="button" onClick={handleGuestMode}>
            Continue as Guest
          </GuestButton>
        </Form>
        
        <Link href="https://console.solidrust.ai" target="_blank" rel="noopener noreferrer">
          Get your API key at console.solidrust.ai
        </Link>
      </AuthCard>
    </AuthContainer>
  );
}

export default AuthPanel;
