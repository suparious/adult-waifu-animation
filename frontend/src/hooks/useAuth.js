import { useState, useCallback, useEffect } from 'react';
import config from '../config';

/**
 * Custom hook for managing authentication state
 */
export function useAuth() {
  const [session, setSession] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Check for stored session on mount
  useEffect(() => {
    const storedSession = localStorage.getItem('waifu_session');
    if (storedSession) {
      try {
        const parsed = JSON.parse(storedSession);
        if (parsed.expires_at && new Date(parsed.expires_at) > new Date()) {
          setSession(parsed);
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem('waifu_session');
        }
      } catch (e) {
        localStorage.removeItem('waifu_session');
      }
    }
    setIsLoading(false);
  }, []);
  
  /**
   * Login with API key
   */
  const login = useCallback(async (apiKey) => {
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
        localStorage.setItem('waifu_session', JSON.stringify(data));
        setSession(data);
        setIsAuthenticated(true);
        return { success: true, session: data };
      } else {
        const errorMessage = data.error || 'Authentication failed';
        setError(errorMessage);
        return { success: false, error: errorMessage };
      }
    } catch (err) {
      const errorMessage = 'Connection error. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  /**
   * Login as guest
   */
  const loginAsGuest = useCallback(() => {
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
    setSession(guestSession);
    setIsAuthenticated(true);
    return guestSession;
  }, []);
  
  /**
   * Logout and clear session
   */
  const logout = useCallback(async () => {
    if (session && !session.is_guest) {
      try {
        await fetch(`${config.api.baseUrl}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.session_token}`,
          },
        });
      } catch (e) {
        console.error('Logout error:', e);
      }
    }
    
    localStorage.removeItem('waifu_session');
    setSession(null);
    setIsAuthenticated(false);
  }, [session]);
  
  /**
   * Get the user ID (for session management)
   */
  const getUserId = useCallback(() => {
    if (!session) return null;
    return session.user?.user_id || session.session_token;
  }, [session]);
  
  /**
   * Get the session token for API calls
   */
  const getSessionToken = useCallback(() => {
    return session?.session_token || null;
  }, [session]);
  
  /**
   * Check if user is a guest
   */
  const isGuest = useCallback(() => {
    return session?.is_guest || false;
  }, [session]);
  
  /**
   * Get user display name
   */
  const getUserName = useCallback(() => {
    return session?.user?.name || 'User';
  }, [session]);
  
  return {
    session,
    isAuthenticated,
    isLoading,
    error,
    login,
    loginAsGuest,
    logout,
    getUserId,
    getSessionToken,
    isGuest,
    getUserName,
    setSession,
  };
}

export default useAuth;
