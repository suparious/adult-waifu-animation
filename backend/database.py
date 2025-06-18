"""
Database models and management for Waifu Animation Chat
Handles session persistence, affection tracking, and unlocked content
"""

import sqlite3
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
from contextlib import contextmanager

class Database:
    def __init__(self, db_path: str = "waifu_chat.db"):
        self.db_path = Path(db_path)
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Affection levels table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS affection_levels (
                    session_id TEXT NOT NULL,
                    waifu_id TEXT NOT NULL,
                    level INTEGER DEFAULT 0,
                    total_interactions INTEGER DEFAULT 0,
                    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (session_id, waifu_id),
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            # Unlocked content table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS unlocked_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    waifu_id TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    content_id TEXT NOT NULL,
                    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                    UNIQUE(session_id, waifu_id, content_type, content_id)
                )
            ''')
            
            # Interaction history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interaction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    waifu_id TEXT NOT NULL,
                    user_message TEXT,
                    waifu_response TEXT,
                    emotion TEXT,
                    affection_change INTEGER DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_affection_session ON affection_levels(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_unlocked_session ON unlocked_content(session_id, waifu_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_session ON interaction_history(session_id, timestamp)')
    
    def get_or_create_session(self, session_id: str) -> Dict:
        """Get existing session or create new one"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if session exists
            cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
            session = cursor.fetchone()
            
            if not session:
                # Create new session
                cursor.execute('INSERT INTO sessions (session_id) VALUES (?)', (session_id,))
                return {
                    'session_id': session_id,
                    'created_at': datetime.now(),
                    'last_active': datetime.now()
                }
            else:
                # Update last active
                cursor.execute('UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?', (session_id,))
                return dict(session)
    
    def get_affection_level(self, session_id: str, waifu_id: str) -> int:
        """Get current affection level for a waifu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT level FROM affection_levels 
                WHERE session_id = ? AND waifu_id = ?
            ''', (session_id, waifu_id))
            
            result = cursor.fetchone()
            return result['level'] if result else 0
    
    def update_affection(self, session_id: str, waifu_id: str, change: int) -> Tuple[int, List[str]]:
        """
        Update affection level and check for unlocks
        Returns: (new_level, list_of_newly_unlocked_content)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get current level
            current_level = self.get_affection_level(session_id, waifu_id)
            new_level = max(0, min(100, current_level + change))  # Clamp between 0-100
            
            # Update or insert affection level
            cursor.execute('''
                INSERT OR REPLACE INTO affection_levels 
                (session_id, waifu_id, level, total_interactions, last_interaction)
                VALUES (?, ?, ?, 
                    COALESCE((SELECT total_interactions FROM affection_levels 
                              WHERE session_id = ? AND waifu_id = ?), 0) + 1,
                    CURRENT_TIMESTAMP)
            ''', (session_id, waifu_id, new_level, session_id, waifu_id))
            
            # Check for newly unlocked content
            unlocked = []
            
            # Define unlock milestones
            milestones = {
                10: [("animation", "shy_smile"), ("dialogue", "friendly")],
                25: [("animation", "blow_kiss"), ("animation", "hair_flip"), ("dialogue", "flirty")],
                40: [("animation", "seductive_pose"), ("outfit", "casual"), ("dialogue", "affectionate")],
                50: [("animation", "body_stretch"), ("animation", "sultry_look"), ("dialogue", "intimate")],
                65: [("animation", "bedroom_eyes"), ("outfit", "nightwear"), ("dialogue", "suggestive")],
                75: [("animation", "special_dance"), ("voice", "breathy"), ("dialogue", "passionate")],
                90: [("animation", "intimate_pose"), ("outfit", "lingerie"), ("dialogue", "explicit")],
                100: [("animation", "love_confession"), ("achievement", "true_love"), ("dialogue", "devoted")]
            }
            
            # Check each milestone
            for milestone, contents in milestones.items():
                if current_level < milestone <= new_level:
                    for content_type, content_id in contents:
                        # Check if already unlocked
                        cursor.execute('''
                            SELECT id FROM unlocked_content 
                            WHERE session_id = ? AND waifu_id = ? 
                            AND content_type = ? AND content_id = ?
                        ''', (session_id, waifu_id, content_type, content_id))
                        
                        if not cursor.fetchone():
                            # Unlock new content
                            cursor.execute('''
                                INSERT INTO unlocked_content 
                                (session_id, waifu_id, content_type, content_id)
                                VALUES (?, ?, ?, ?)
                            ''', (session_id, waifu_id, content_type, content_id))
                            unlocked.append(f"{content_type}:{content_id}")
            
            return new_level, unlocked
    
    def get_unlocked_content(self, session_id: str, waifu_id: str) -> Dict[str, List[str]]:
        """Get all unlocked content for a waifu"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT content_type, content_id FROM unlocked_content
                WHERE session_id = ? AND waifu_id = ?
                ORDER BY unlocked_at
            ''', (session_id, waifu_id))
            
            unlocked = {}
            for row in cursor.fetchall():
                content_type = row['content_type']
                if content_type not in unlocked:
                    unlocked[content_type] = []
                unlocked[content_type].append(row['content_id'])
            
            return unlocked
    
    def save_interaction(self, session_id: str, waifu_id: str, user_message: str, 
                        waifu_response: str, emotion: str, affection_change: int):
        """Save interaction to history"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO interaction_history 
                (session_id, waifu_id, user_message, waifu_response, emotion, affection_change)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, waifu_id, user_message, waifu_response, emotion, affection_change))
    
    def get_session_stats(self, session_id: str) -> Dict:
        """Get statistics for a session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get affection levels for all waifus
            cursor.execute('''
                SELECT waifu_id, level, total_interactions 
                FROM affection_levels WHERE session_id = ?
            ''', (session_id,))
            
            affection_data = {}
            for row in cursor.fetchall():
                affection_data[row['waifu_id']] = {
                    'level': row['level'],
                    'interactions': row['total_interactions']
                }
            
            # Get total unlocked content count
            cursor.execute('''
                SELECT COUNT(*) as count FROM unlocked_content WHERE session_id = ?
            ''', (session_id,))
            unlock_count = cursor.fetchone()['count']
            
            # Get interaction count
            cursor.execute('''
                SELECT COUNT(*) as count FROM interaction_history WHERE session_id = ?
            ''', (session_id,))
            interaction_count = cursor.fetchone()['count']
            
            return {
                'affection_levels': affection_data,
                'total_unlocks': unlock_count,
                'total_interactions': interaction_count
            }
    
    def cleanup_old_sessions(self, days: int = 30):
        """Clean up sessions older than specified days"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM sessions 
                WHERE last_active < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            # Cascade deletions are handled by foreign keys
            return cursor.rowcount

# Singleton instance
_db_instance = None

def get_db() -> Database:
    """Get database singleton instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
