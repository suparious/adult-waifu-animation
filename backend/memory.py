"""
Conversation Memory Module
Handles long-term memory via embeddings and semantic search
"""

import os
import httpx
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager
import numpy as np


@dataclass
class MemoryConfig:
    """Memory system configuration"""
    embeddings_url: str
    embeddings_model: str = "bge-m3"
    timeout: float = 30.0
    top_k: int = 5
    similarity_threshold: float = 0.7
    max_memory_age_days: int = 90
    enable_memory: bool = True
    
    @classmethod
    def from_env(cls) -> 'MemoryConfig':
        return cls(
            embeddings_url=os.getenv(
                "EMBEDDINGS_URL", 
                "https://artemis.hq.solidrust.net/v1/embeddings"
            ),
            embeddings_model=os.getenv("EMBEDDINGS_MODEL", "bge-m3"),
            timeout=float(os.getenv("EMBEDDINGS_TIMEOUT", "30.0")),
            top_k=int(os.getenv("MEMORY_TOP_K", "5")),
            similarity_threshold=float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.7")),
            max_memory_age_days=int(os.getenv("MEMORY_MAX_AGE_DAYS", "90")),
            enable_memory=os.getenv("ENABLE_MEMORY", "true").lower() == "true"
        )


@dataclass
class Memory:
    """A single memory entry"""
    id: Optional[int] = None
    user_id: str = ""
    waifu_id: str = ""
    content: str = ""
    category: str = "general"  # facts, emotions, topics, milestones
    embedding: Optional[List[float]] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    importance: float = 1.0  # 0.0 - 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "waifu_id": self.waifu_id,
            "content": self.content,
            "category": self.category,
            "timestamp": self.timestamp.isoformat(),
            "importance": self.importance
        }


class MemoryDatabase:
    """
    SQLite-based memory storage with vector similarity search
    Uses numpy for efficient cosine similarity calculation
    """
    
    def __init__(self, db_path: str = "waifu_memories.db"):
        self.db_path = Path(db_path)
        self.init_db()
    
    @contextmanager
    def get_connection(self):
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
        """Initialize memory tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Memories table with embedding storage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    waifu_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    embedding BLOB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    importance REAL DEFAULT 1.0,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_waifu ON memories(user_id, waifu_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(user_id, waifu_id, category)')
            
            # Memory summaries for long-term storage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    waifu_id TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    period_start TIMESTAMP,
                    period_end TIMESTAMP,
                    embedding BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def _serialize_embedding(self, embedding: List[float]) -> bytes:
        """Convert embedding list to bytes for storage"""
        return np.array(embedding, dtype=np.float32).tobytes()
    
    def _deserialize_embedding(self, data: bytes) -> List[float]:
        """Convert bytes back to embedding list"""
        return np.frombuffer(data, dtype=np.float32).tolist()
    
    def store_memory(self, memory: Memory) -> int:
        """Store a memory and return its ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            embedding_bytes = None
            if memory.embedding:
                embedding_bytes = self._serialize_embedding(memory.embedding)
            
            cursor.execute('''
                INSERT INTO memories 
                (user_id, waifu_id, content, category, embedding, timestamp, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory.user_id,
                memory.waifu_id,
                memory.content,
                memory.category,
                embedding_bytes,
                memory.timestamp,
                memory.importance
            ))
            
            return cursor.lastrowid
    
    def get_all_embeddings(self, user_id: str, waifu_id: str) -> List[Tuple[int, List[float], str]]:
        """Get all embeddings for a user-waifu pair"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, embedding, content FROM memories
                WHERE user_id = ? AND waifu_id = ? AND embedding IS NOT NULL
                ORDER BY timestamp DESC
            ''', (user_id, waifu_id))
            
            results = []
            for row in cursor.fetchall():
                if row['embedding']:
                    embedding = self._deserialize_embedding(row['embedding'])
                    results.append((row['id'], embedding, row['content']))
            
            return results
    
    def get_memories_by_ids(self, memory_ids: List[int]) -> List[Memory]:
        """Get memories by their IDs"""
        if not memory_ids:
            return []
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            placeholders = ','.join('?' * len(memory_ids))
            cursor.execute(f'''
                SELECT * FROM memories WHERE id IN ({placeholders})
            ''', memory_ids)
            
            memories = []
            for row in cursor.fetchall():
                embedding = None
                if row['embedding']:
                    embedding = self._deserialize_embedding(row['embedding'])
                
                memories.append(Memory(
                    id=row['id'],
                    user_id=row['user_id'],
                    waifu_id=row['waifu_id'],
                    content=row['content'],
                    category=row['category'],
                    embedding=embedding,
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    importance=row['importance']
                ))
            
            return memories
    
    def update_access(self, memory_id: int):
        """Update access count and last accessed time"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE memories 
                SET access_count = access_count + 1, last_accessed = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (memory_id,))
    
    def get_recent_memories(self, user_id: str, waifu_id: str, limit: int = 10) -> List[Memory]:
        """Get most recent memories"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM memories
                WHERE user_id = ? AND waifu_id = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (user_id, waifu_id, limit))
            
            return [Memory(
                id=row['id'],
                user_id=row['user_id'],
                waifu_id=row['waifu_id'],
                content=row['content'],
                category=row['category'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                importance=row['importance']
            ) for row in cursor.fetchall()]


class MemoryManager:
    """
    Manages conversation memory using embeddings
    
    Flow:
    1. User sends message
    2. Extract memorable content (facts, preferences, topics)
    3. Embed content using Artemis/vLLM embeddings
    4. Store in vector database
    5. On new messages, retrieve relevant memories
    6. Inject memories into system prompt
    """
    
    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig.from_env()
        self.db = MemoryDatabase()
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        self._api_key = os.getenv("LLM_API_KEY", "")
    
    async def close(self):
        await self._client.aclose()
    
    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get embedding for text from Artemis/vLLM embeddings endpoint
        """
        if not self.config.enable_memory:
            return None
        
        try:
            headers = {
                "Content-Type": "application/json"
            }
            if self._api_key:
                headers["X-API-Key"] = self._api_key
                headers["Authorization"] = f"Bearer {self._api_key}"
            
            response = await self._client.post(
                self.config.embeddings_url,
                json={
                    "input": text,
                    "model": self.config.embeddings_model
                },
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["data"][0]["embedding"]
            else:
                print(f"Embedding error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))
    
    async def store_memory(
        self, 
        user_id: str, 
        waifu_id: str, 
        content: str, 
        category: str = "general",
        importance: float = 1.0
    ) -> Optional[int]:
        """
        Store a new memory with embedding
        
        Categories:
        - facts: User's name, job, preferences, mentioned details
        - emotions: How past conversations felt
        - topics: What they've discussed before
        - milestones: Relationship progression events
        """
        if not self.config.enable_memory:
            return None
        
        # Get embedding for the content
        embedding = await self.get_embedding(content)
        
        memory = Memory(
            user_id=user_id,
            waifu_id=waifu_id,
            content=content,
            category=category,
            embedding=embedding,
            importance=importance
        )
        
        return self.db.store_memory(memory)
    
    async def retrieve_relevant_memories(
        self, 
        user_id: str, 
        waifu_id: str, 
        query: str,
        top_k: Optional[int] = None
    ) -> List[Memory]:
        """
        Retrieve memories most relevant to the current query
        """
        if not self.config.enable_memory:
            return []
        
        top_k = top_k or self.config.top_k
        
        # Get query embedding
        query_embedding = await self.get_embedding(query)
        if not query_embedding:
            # Fallback to recent memories
            return self.db.get_recent_memories(user_id, waifu_id, top_k)
        
        # Get all embeddings for this user-waifu pair
        all_embeddings = self.db.get_all_embeddings(user_id, waifu_id)
        
        if not all_embeddings:
            return []
        
        # Calculate similarities
        similarities = []
        for memory_id, embedding, content in all_embeddings:
            sim = self._cosine_similarity(query_embedding, embedding)
            if sim >= self.config.similarity_threshold:
                similarities.append((memory_id, sim, content))
        
        # Sort by similarity and take top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_memory_ids = [mid for mid, _, _ in similarities[:top_k]]
        
        # Get full memory objects
        memories = self.db.get_memories_by_ids(top_memory_ids)
        
        # Update access counts
        for memory in memories:
            if memory.id:
                self.db.update_access(memory.id)
        
        return memories
    
    def format_memories_for_prompt(self, memories: List[Memory], user_name: str = "User") -> str:
        """
        Format retrieved memories for injection into system prompt
        """
        if not memories:
            return ""
        
        # Group by category
        categorized = {}
        for memory in memories:
            if memory.category not in categorized:
                categorized[memory.category] = []
            categorized[memory.category].append(memory)
        
        lines = [f"\n[Memories of {user_name}:]"]
        
        # Format each category
        category_labels = {
            "facts": "Personal details",
            "emotions": "Emotional history",
            "topics": "Past conversations",
            "milestones": "Relationship milestones",
            "general": "Other memories"
        }
        
        for category, category_memories in categorized.items():
            label = category_labels.get(category, category.title())
            for mem in category_memories:
                lines.append(f"- {mem.content}")
        
        return "\n".join(lines)
    
    async def extract_memorable_content(
        self, 
        user_message: str, 
        waifu_response: str
    ) -> List[Dict[str, Any]]:
        """
        Extract memorable content from a conversation exchange
        Returns list of {content, category, importance}
        
        Uses simple heuristics - could be enhanced with LLM extraction
        """
        memories = []
        message_lower = user_message.lower()
        
        # Facts extraction (names, jobs, preferences)
        fact_patterns = [
            ("my name is", "facts", 0.9),
            ("i'm called", "facts", 0.9),
            ("call me", "facts", 0.9),
            ("i work as", "facts", 0.8),
            ("i'm a", "facts", 0.7),
            ("i like", "facts", 0.6),
            ("i love", "facts", 0.7),
            ("i hate", "facts", 0.6),
            ("i prefer", "facts", 0.6),
            ("favorite", "facts", 0.6),
        ]
        
        for pattern, category, importance in fact_patterns:
            if pattern in message_lower:
                # Extract the relevant part of the message
                content = user_message  # In production, extract more precisely
                memories.append({
                    "content": content,
                    "category": category,
                    "importance": importance
                })
                break  # One fact per message
        
        # Emotional content
        emotion_patterns = [
            ("stressed", "emotions", 0.7),
            ("happy", "emotions", 0.6),
            ("sad", "emotions", 0.7),
            ("excited", "emotions", 0.6),
            ("worried", "emotions", 0.7),
            ("lonely", "emotions", 0.8),
        ]
        
        for pattern, category, importance in emotion_patterns:
            if pattern in message_lower:
                memories.append({
                    "content": f"User felt {pattern} during conversation",
                    "category": category,
                    "importance": importance
                })
                break
        
        # Topics (for future reference)
        topic_patterns = [
            ("anime", "topics", 0.5),
            ("game", "topics", 0.5),
            ("movie", "topics", 0.5),
            ("music", "topics", 0.5),
            ("work", "topics", 0.5),
            ("school", "topics", 0.5),
        ]
        
        for pattern, category, importance in topic_patterns:
            if pattern in message_lower:
                memories.append({
                    "content": f"Discussed {pattern} with the user",
                    "category": category,
                    "importance": importance
                })
        
        return memories
    
    async def process_conversation(
        self,
        user_id: str,
        waifu_id: str,
        user_message: str,
        waifu_response: str
    ) -> List[int]:
        """
        Process a conversation and store any memorable content
        Returns list of stored memory IDs
        """
        if not self.config.enable_memory:
            return []
        
        # Extract memorable content
        extracted = await self.extract_memorable_content(user_message, waifu_response)
        
        # Store each memory
        memory_ids = []
        for item in extracted:
            memory_id = await self.store_memory(
                user_id=user_id,
                waifu_id=waifu_id,
                content=item["content"],
                category=item["category"],
                importance=item["importance"]
            )
            if memory_id:
                memory_ids.append(memory_id)
        
        return memory_ids


# Singleton instance
_memory_manager: Optional[MemoryManager] = None


def get_memory_manager() -> MemoryManager:
    """Get memory manager singleton"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager


async def init_memory_manager() -> MemoryManager:
    """Initialize memory manager"""
    return get_memory_manager()


async def shutdown_memory_manager():
    """Shutdown memory manager"""
    global _memory_manager
    if _memory_manager:
        await _memory_manager.close()
        _memory_manager = None
