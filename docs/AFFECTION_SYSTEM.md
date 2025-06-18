# Affection/Progression System Documentation

## Overview

The Affection/Progression System creates a meaningful relationship progression between users and their chosen waifus. This system tracks affection levels from 0-100, unlocks content at milestones, and modifies AI responses based on relationship depth.

## Features

### 1. Affection Tracking
- **Range**: 0-100 points
- **Persistence**: Saved in SQLite database per session
- **Multi-waifu**: Each waifu has independent affection levels

### 2. Affection Gain Mechanics

#### Positive Interactions
- **Compliments** (+3): "beautiful", "gorgeous", "pretty", "cute"
- **Love Declarations** (+5): "love you", "adore you", "care about you"
- **Physical Affection** (+3): "hug", "cuddle", "kiss", "embrace"
- **Gifts** (+4): "gift", "present", "flowers", "chocolate"
- **Quality Time** (+2): "spend time", "be with you", "together"
- **Protection** (+3): "protect you", "keep you safe", "worry about you"

#### Negative Interactions
- **Rudeness** (-5): "stupid", "ugly", "hate", "worthless"
- **Dismissiveness** (-3): "whatever", "boring", "not interested"
- **Inappropriate** (-4): "shut up", "leave me alone", "get lost"

#### Modifiers
- **Emotion Multipliers**: Happy (1.2x), Flirty (1.3x), Affectionate (1.5x)
- **Personality Compatibility**: Calculated based on waifu traits
- **Level Scaling**: Harder to gain at higher levels (50% reduction at level 100)

### 3. Content Milestones

| Level | Unlocks | Description |
|-------|---------|-------------|
| 10 | Shy smile, Friendly dialogue | Starting to warm up |
| 25 | Blow kiss, Hair flip, Flirty dialogue | Becoming playful |
| 40 | Seductive pose, Casual outfit, Affectionate dialogue | Growing closer |
| 50 | Body stretch, Sultry look, Intimate dialogue | Developing feelings |
| 65 | Bedroom eyes, Nightwear outfit, Suggestive dialogue | Strong attraction |
| 75 | Special dance, Breathy voice, Passionate dialogue | Deep connection |
| 90 | Intimate pose, Lingerie outfit, Explicit dialogue | Nearly devoted |
| 100 | Love confession, True love achievement, Devoted dialogue | Complete devotion |

### 4. Response Modifiers

The AI's responses change based on affection level:

- **0-9**: Polite but distant
- **10-24**: Friendly and warming up
- **25-49**: Comfortable, playful, occasionally flirty
- **50-74**: Affectionate, caring, openly flirty
- **75-89**: Passionate, intimate, expressing desire
- **90-100**: Completely devoted, extremely affectionate

### 5. Visual Feedback

#### Affection Meter
- Real-time display of current level
- Animated progress bar with color changes
- Change indicators (+/- with reason)
- Current dialogue level display

#### Milestone Notifications
- Special messages from waifu at key levels
- Unlock popups for new content
- Visual celebration effects

## Technical Implementation

### Backend Components

1. **database.py**
   - SQLite database management
   - Session tracking
   - Affection level storage
   - Unlocked content tracking
   - Interaction history

2. **affection_manager.py**
   - Affection calculation logic
   - Personality compatibility
   - Unlock checking
   - Response modifiers

3. **main.py Integration**
   - WebSocket message handling
   - Affection processing per interaction
   - Response modification based on level

### Frontend Components

1. **AffectionMeter.js**
   - Visual affection display
   - Progress animations
   - Unlock notifications
   - Milestone messages

2. **App.js Integration**
   - State management for affection data
   - WebSocket message processing
   - Component coordination

### Database Schema

```sql
-- Sessions table
sessions (
    id: INTEGER PRIMARY KEY,
    session_id: TEXT UNIQUE,
    created_at: TIMESTAMP,
    last_active: TIMESTAMP
)

-- Affection levels
affection_levels (
    session_id: TEXT,
    waifu_id: TEXT,
    level: INTEGER (0-100),
    total_interactions: INTEGER,
    last_interaction: TIMESTAMP
)

-- Unlocked content
unlocked_content (
    session_id: TEXT,
    waifu_id: TEXT,
    content_type: TEXT,
    content_id: TEXT,
    unlocked_at: TIMESTAMP
)

-- Interaction history
interaction_history (
    session_id: TEXT,
    waifu_id: TEXT,
    user_message: TEXT,
    waifu_response: TEXT,
    emotion: TEXT,
    affection_change: INTEGER,
    timestamp: TIMESTAMP
)
```

## Testing

Run the test suite to verify functionality:

```bash
python test-affection-system.py
```

This tests:
- Affection calculations
- Database operations
- Milestone unlocks
- Response modifiers

## Future Enhancements

1. **User Accounts**: Replace session-based tracking with user accounts
2. **Cloud Sync**: Backup progress to cloud storage
3. **Achievement System**: Special rewards for various accomplishments
4. **Affection Decay**: Gradual decrease when not interacting
5. **Special Events**: Holiday bonuses, birthday celebrations
6. **Cross-Waifu Jealousy**: Reactions when switching between waifus
7. **Custom Thresholds**: Adjustable progression speed
8. **Export/Import**: Save and share progress

## Configuration

The system can be configured through environment variables:

```bash
MAX_AFFECTION_LEVEL=100  # Maximum affection level
AFFECTION_DECAY_RATE=0   # Points lost per day of inactivity
NSFW_THRESHOLD=50        # Minimum level for NSFW content
```

## Privacy & Data

- All affection data is stored locally in SQLite
- No personal information is collected
- Sessions are anonymous (based on browser session)
- Data can be deleted by removing the database file

## Tips for Users

1. **Be Consistent**: Regular interactions build affection faster
2. **Match Personality**: Each waifu responds differently to interactions
3. **Watch for Cues**: Pay attention to milestone messages
4. **Explore Unlocks**: New animations and dialogues enhance the experience
5. **Be Patient**: Higher levels require more effort but offer better rewards

The Affection System transforms the chat experience from simple conversations into a meaningful relationship simulation with progression, rewards, and deepening emotional connections.
