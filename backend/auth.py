"""
PAM Platform Authentication Module
Handles API key validation and user session management
"""

import os
import httpx
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import secrets
import hashlib
from functools import lru_cache


@dataclass
class AuthConfig:
    """Authentication configuration"""
    pam_url: str
    validate_endpoint: str = "/v1/keys/validate"
    graphql_endpoint: str = "/graphql"
    timeout: float = 10.0
    enable_auth: bool = True
    
    @classmethod
    def from_env(cls) -> 'AuthConfig':
        return cls(
            pam_url=os.getenv("PAM_URL", "https://console.solidrust.ai"),
            validate_endpoint=os.getenv("PAM_VALIDATE_ENDPOINT", "/v1/keys/validate"),
            graphql_endpoint=os.getenv("PAM_GRAPHQL_ENDPOINT", "/graphql"),
            timeout=float(os.getenv("PAM_TIMEOUT", "10.0")),
            enable_auth=os.getenv("ENABLE_AUTH", "false").lower() == "true"
        )


@dataclass
class User:
    """Authenticated user data"""
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    subscription_tier: str = "free"
    api_key_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "subscription_tier": self.subscription_tier,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class AuthSession:
    """Authenticated session with token"""
    session_token: str
    user: User
    expires_at: datetime
    
    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_token": self.session_token,
            "user": self.user.to_dict(),
            "expires_at": self.expires_at.isoformat()
        }


class AuthManager:
    """
    Manages authentication with PAM Platform
    
    Authentication flow:
    1. Client provides API key (from console.solidrust.ai)
    2. Backend validates key against PAM /v1/keys/validate
    3. On success, issues a session token for WebSocket auth
    4. Session data tied to user, not browser session
    """
    
    def __init__(self, config: Optional[AuthConfig] = None):
        self.config = config or AuthConfig.from_env()
        self._sessions: Dict[str, AuthSession] = {}
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
    
    async def close(self):
        """Close HTTP client"""
        await self._client.aclose()
    
    def _generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def _hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage/comparison"""
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]
    
    async def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Validate an API key against PAM Platform
        
        Returns user data on success, None on failure
        """
        if not self.config.enable_auth:
            # Auth disabled - return mock user
            return {
                "valid": True,
                "user_id": "guest",
                "email": None,
                "name": "Guest User",
                "subscription_tier": "free"
            }
        
        try:
            url = f"{self.config.pam_url}{self.config.validate_endpoint}"
            response = await self._client.post(
                url,
                json={"api_key": api_key},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    return data
            
            return None
            
        except Exception as e:
            print(f"Error validating API key: {e}")
            return None
    
    async def authenticate(self, api_key: str) -> Optional[AuthSession]:
        """
        Authenticate user with API key and create session
        
        Returns AuthSession on success, None on failure
        """
        # Validate API key with PAM
        validation_result = await self.validate_api_key(api_key)
        
        if not validation_result:
            return None
        
        # Create user object
        user = User(
            user_id=validation_result.get("user_id", "unknown"),
            email=validation_result.get("email"),
            name=validation_result.get("name"),
            subscription_tier=validation_result.get("subscription_tier", "free"),
            api_key_hash=self._hash_api_key(api_key),
            created_at=datetime.utcnow()
        )
        
        # Generate session token
        session_token = self._generate_session_token()
        
        # Create session with 24-hour expiry
        session = AuthSession(
            session_token=session_token,
            user=user,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        
        # Store session
        self._sessions[session_token] = session
        
        return session
    
    def get_session(self, session_token: str) -> Optional[AuthSession]:
        """
        Get session by token
        
        Returns None if session doesn't exist or is expired
        """
        session = self._sessions.get(session_token)
        
        if not session:
            return None
        
        if session.is_expired:
            # Clean up expired session
            del self._sessions[session_token]
            return None
        
        return session
    
    def invalidate_session(self, session_token: str) -> bool:
        """
        Invalidate (logout) a session
        
        Returns True if session was found and removed
        """
        if session_token in self._sessions:
            del self._sessions[session_token]
            return True
        return False
    
    def get_user_session(self, user_id: str) -> Optional[AuthSession]:
        """
        Get active session for a user ID
        
        Returns the most recent non-expired session for the user
        """
        for session in self._sessions.values():
            if session.user.user_id == user_id and not session.is_expired:
                return session
        return None
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions
        
        Returns count of removed sessions
        """
        expired = [token for token, session in self._sessions.items() if session.is_expired]
        for token in expired:
            del self._sessions[token]
        return len(expired)
    
    async def get_user_info(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed user info from PAM GraphQL endpoint
        
        Returns user details on success, None on failure
        """
        if not self.config.enable_auth:
            return {
                "id": "guest",
                "email": None,
                "name": "Guest User",
                "subscription": {"tier": "free"}
            }
        
        try:
            url = f"{self.config.pam_url}{self.config.graphql_endpoint}"
            query = """
            query GetCurrentUser {
                me {
                    id
                    email
                    name
                    subscription {
                        tier
                        status
                        currentPeriodEnd
                    }
                }
            }
            """
            
            response = await self._client.post(
                url,
                json={"query": query},
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": api_key
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("me")
            
            return None
            
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return None


# Singleton instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get auth manager singleton"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


async def init_auth_manager() -> AuthManager:
    """Initialize auth manager (call at app startup)"""
    return get_auth_manager()


async def shutdown_auth_manager():
    """Shutdown auth manager (call at app shutdown)"""
    global _auth_manager
    if _auth_manager:
        await _auth_manager.close()
        _auth_manager = None
