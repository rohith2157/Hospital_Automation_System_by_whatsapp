import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    // Skip token verification for now to avoid blocking the UI
    setLoading(false);
    if (token) {
      // Clear invalid token
      localStorage.removeItem('token');
      setToken(null);
    }
  }, []);

  const login = async (username, password) => {
    try {
      const response = await authService.login(username, password);
      const { access_token, user: userData } = response;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const hasPermission = (module, action) => {
    if (!user) return false;
    
    // Superadmin has all permissions
    if (user.role === 'superadmin') return true;
    
    // For other roles, you might want to implement permission checks
    // based on your backend permissions table
    const rolePermissions = {
      admin: { 
        users: ['read', 'create', 'update'], 
        appointments: ['read', 'create', 'update', 'delete'],
        patients: ['read', 'create', 'update'],
        doctors: ['read', 'create', 'update'],
        campaigns: ['read', 'create', 'update'],
        feedback: ['read']
      },
      reception: {
        appointments: ['read', 'create', 'update'],
        patients: ['read', 'create', 'update'],
        doctors: ['read'],
        feedback: ['read', 'create']
      },
      campaign: {
        campaigns: ['read', 'create', 'update'],
        patients: ['read'],
        message_logs: ['read']
      },
      viewer: {
        appointments: ['read'],
        patients: ['read'],
        doctors: ['read'],
        feedback: ['read']
      }
    };

    const permissions = rolePermissions[user.role] || {};
    return permissions[module]?.includes(action) || false;
  };

  const value = {
    user,
    login,
    logout,
    loading,
    hasPermission,
    token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};