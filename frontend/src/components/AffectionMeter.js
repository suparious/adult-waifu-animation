import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import config from '../config';

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
`;

const shimmer = keyframes`
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
`;

const AffectionContainer = styled.div`
  position: absolute;
  top: ${config.ui.layout.spacing.large}px;
  right: ${config.ui.layout.spacing.large}px;
  background: ${config.ui.colors.background.glass};
  padding: 15px 20px;
  border-radius: ${config.ui.layout.borderRadius.large}px;
  backdrop-filter: blur(${config.ui.animations.glassBlur}px);
  min-width: 200px;
  z-index: 10;
`;

const AffectionHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
`;

const HeartIcon = styled.div`
  font-size: 24px;
  animation: ${props => props.isMilestone ? pulse : 'none'} 1s ease-in-out infinite;
  color: ${props => {
    if (props.level >= 75) return '#ff1493';
    if (props.level >= 50) return '#ff69b4';
    if (props.level >= 25) return '#ff86b7';
    return '#ffb6c1';
  }};
`;

const WaifuName = styled.h3`
  margin: 0;
  font-size: 16px;
  color: ${config.ui.colors.text.primary};
`;

const AffectionBarContainer = styled.div`
  position: relative;
  width: 100%;
  height: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: ${config.ui.layout.borderRadius.medium}px;
  overflow: hidden;
  margin-bottom: 5px;
`;

const AffectionBar = styled.div`
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: ${props => props.level}%;
  background: linear-gradient(90deg, 
    ${props => props.level >= 75 ? '#ff1493' : '#ff69b4'} 0%, 
    ${props => props.level >= 50 ? '#ff1493' : '#ff86b7'} 100%
  );
  transition: width 0.5s ease;
  border-radius: ${config.ui.layout.borderRadius.medium}px;
  
  ${props => props.isAnimating && `
    background: linear-gradient(90deg, 
      ${props.level >= 75 ? '#ff1493' : '#ff69b4'} 0%, 
      ${props.level >= 50 ? '#ff1493' : '#ff86b7'} 50%,
      #fff 51%,
      ${props.level >= 50 ? '#ff1493' : '#ff86b7'} 52%,
      ${props.level >= 75 ? '#ff1493' : '#ff69b4'} 100%
    );
    background-size: 200% 100%;
    animation: ${shimmer} 1s linear;
  `}
`;

const AffectionLevel = styled.div`
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
`;

const AffectionChange = styled.div`
  font-size: 14px;
  color: ${props => props.change > 0 ? '#4CAF50' : '#f44336'};
  text-align: center;
  opacity: ${props => props.show ? 1 : 0};
  transform: translateY(${props => props.show ? 0 : 10}px);
  transition: all 0.3s ease;
`;

const DialogueLevel = styled.div`
  font-size: 12px;
  color: ${config.ui.colors.text.secondary};
  text-align: center;
  margin-top: 5px;
  font-style: italic;
`;

const UnlockNotification = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, 
    ${config.ui.colors.primary} 0%, 
    ${config.ui.colors.secondary} 100%
  );
  padding: 20px 40px;
  border-radius: ${config.ui.layout.borderRadius.large}px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  opacity: ${props => props.show ? 1 : 0};
  transform: translate(-50%, -50%) scale(${props => props.show ? 1 : 0.8});
  transition: all 0.3s ease;
  pointer-events: ${props => props.show ? 'auto' : 'none'};
`;

const UnlockTitle = styled.h2`
  margin: 0 0 10px 0;
  color: white;
  font-size: 24px;
  text-align: center;
`;

const UnlockContent = styled.div`
  color: white;
  font-size: 16px;
  text-align: center;
`;

const MilestoneMessage = styled.div`
  position: absolute;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: ${config.ui.colors.background.glass};
  padding: 15px 30px;
  border-radius: ${config.ui.layout.borderRadius.large}px;
  backdrop-filter: blur(${config.ui.animations.glassBlur}px);
  font-size: 18px;
  color: ${config.ui.colors.text.primary};
  text-align: center;
  opacity: ${props => props.show ? 1 : 0};
  transform: translateX(-50%) translateY(${props => props.show ? 0 : 20}px);
  transition: all 0.5s ease;
  max-width: 80%;
  z-index: 100;
`;

function AffectionMeter({ waifuId, waifuName, affectionData, onUnlock }) {
  const [level, setLevel] = useState(0);
  const [previousLevel, setPreviousLevel] = useState(0);
  const [showChange, setShowChange] = useState(false);
  const [changeAmount, setChangeAmount] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [showUnlock, setShowUnlock] = useState(false);
  const [unlockContent, setUnlockContent] = useState([]);
  const [showMilestone, setShowMilestone] = useState(false);
  const [milestoneMessage, setMilestoneMessage] = useState('');
  const [dialogueLevel, setDialogueLevel] = useState('friendly');

  useEffect(() => {
    if (affectionData) {
      // Update levels
      if (affectionData.new_level !== level) {
        setPreviousLevel(level);
        setLevel(affectionData.new_level);
        setIsAnimating(true);
        setTimeout(() => setIsAnimating(false), 1000);
      }

      // Show change indicator
      if (affectionData.change !== 0) {
        setChangeAmount(affectionData.change);
        setShowChange(true);
        setTimeout(() => setShowChange(false), 3000);
      }

      // Handle unlocks
      if (affectionData.unlocked && affectionData.unlocked.length > 0) {
        setUnlockContent(affectionData.unlocked);
        setShowUnlock(true);
        setTimeout(() => setShowUnlock(false), 5000);
        if (onUnlock) {
          onUnlock(affectionData.unlocked);
        }
      }

      // Handle milestone
      if (affectionData.is_milestone && affectionData.milestone_message) {
        setMilestoneMessage(affectionData.milestone_message);
        setShowMilestone(true);
        setTimeout(() => setShowMilestone(false), 7000);
      }

      // Update dialogue level
      if (affectionData.dialogue_level) {
        setDialogueLevel(affectionData.dialogue_level);
      }
    }
  }, [affectionData, level, onUnlock]);

  const getDialogueLevelText = (level) => {
    const levels = {
      'friendly': 'Getting to know you',
      'flirty': 'Feeling playful',
      'intimate': 'Growing closer',
      'passionate': 'Deeply connected',
      'devoted': 'Completely yours'
    };
    return levels[level] || 'Friendly';
  };

  const formatUnlockText = (unlock) => {
    const [type, id] = unlock.split(':');
    const typeNames = {
      'animation': '✨ Animation',
      'dialogue': '💬 Dialogue',
      'outfit': '👗 Outfit',
      'voice': '🎵 Voice',
      'achievement': '🏆 Achievement'
    };
    return `${typeNames[type] || type}: ${id.replace(/_/g, ' ')}`;
  };

  return (
    <>
      <AffectionContainer>
        <AffectionHeader>
          <HeartIcon level={level} isMilestone={affectionData?.is_milestone}>
            {level >= 90 ? '💖' : level >= 75 ? '💕' : level >= 50 ? '💗' : level >= 25 ? '💓' : '💝'}
          </HeartIcon>
          <WaifuName>{waifuName}'s Affection</WaifuName>
        </AffectionHeader>
        
        <AffectionBarContainer>
          <AffectionBar level={level} isAnimating={isAnimating} />
          <AffectionLevel>{level}/100</AffectionLevel>
        </AffectionBarContainer>
        
        <AffectionChange show={showChange} change={changeAmount}>
          {changeAmount > 0 ? `+${changeAmount}` : changeAmount} {affectionData?.reason || ''}
        </AffectionChange>
        
        <DialogueLevel>{getDialogueLevelText(dialogueLevel)}</DialogueLevel>
      </AffectionContainer>

      <UnlockNotification show={showUnlock}>
        <UnlockTitle>🎉 New Content Unlocked!</UnlockTitle>
        <UnlockContent>
          {unlockContent.map((unlock, index) => (
            <div key={index}>{formatUnlockText(unlock)}</div>
          ))}
        </UnlockContent>
      </UnlockNotification>

      <MilestoneMessage show={showMilestone}>
        {milestoneMessage}
      </MilestoneMessage>
    </>
  );
}

export default AffectionMeter;
