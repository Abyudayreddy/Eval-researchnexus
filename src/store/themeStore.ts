import { create } from 'zustand';

export type ThemeMode = 'light' | 'dark' | 'relax';

interface ThemeState {
  theme: ThemeMode;
  setTheme: (theme: ThemeMode) => void;
  toggleTheme: () => void;
}

const THEME_STORAGE_KEY = 'researchnexus_theme_mode';

function applyThemeToDocument(theme: ThemeMode) {
  const root = document.documentElement;
  // Clean prior themes
  root.classList.remove('theme-light', 'theme-dark', 'theme-relax', 'dark');

  if (theme === 'dark') {
    root.classList.add('dark', 'theme-dark');
  } else if (theme === 'relax') {
    root.classList.add('theme-relax');
  } else {
    root.classList.add('theme-light');
  }
  root.setAttribute('data-theme', theme);
}

// Initial theme from storage or system preference
const initialTheme: ThemeMode = (() => {
  const saved = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode | null;
  if (saved && ['light', 'dark', 'relax'].includes(saved)) {
    return saved;
  }
  return 'light';
})();

// Immediately apply theme before first render
applyThemeToDocument(initialTheme);

export const useThemeStore = create<ThemeState>((set, get) => ({
  theme: initialTheme,
  setTheme: (theme: ThemeMode) => {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
    applyThemeToDocument(theme);
    set({ theme });
  },
  toggleTheme: () => {
    const current = get().theme;
    const next: ThemeMode = current === 'light' ? 'relax' : current === 'relax' ? 'dark' : 'light';
    get().setTheme(next);
  }
}));
