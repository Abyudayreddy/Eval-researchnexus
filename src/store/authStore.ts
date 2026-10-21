import { create } from 'zustand';
import { api } from '../utils/api';

interface User {
  id: string;
  email: string;
  name: string;
  title?: string;
  institution?: string;
  bio?: string;
  location?: string;
  website?: string;
  orcid?: string;
  google_scholar?: string;
  stats?: {
    papers_saved: number;
    projects_active: number;
    notes_written: number;
    streak_days: number;
  };
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setToken: (token: string) => void;
  setUser: (user: User) => void;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: localStorage.getItem('researchnexus_token'),
  user: null,
  isAuthenticated: !!localStorage.getItem('researchnexus_token'),
  isLoading: false,

  setToken: (token: string) => {
    localStorage.setItem('researchnexus_token', token);
    set({ token, isAuthenticated: true });
  },

  setUser: (user: User) => set({ user }),

  logout: () => {
    localStorage.removeItem('researchnexus_token');
    set({ token: null, user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    const { token, logout } = get();
    if (!token) {
      set({ isAuthenticated: false, isLoading: false });
      return;
    }
    
    set({ isLoading: true });
    try {
      const userData = await api.auth.me();
      set({ user: userData, isAuthenticated: true });
    } catch (error) {
      console.error("Auth check failed:", error);
      logout();
    } finally {
      set({ isLoading: false });
    }
  }
}));
