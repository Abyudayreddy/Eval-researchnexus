import React, { useState, useRef, useEffect } from 'react';
import { Sun, Moon, Sparkles, Check } from 'lucide-react';
import { useThemeStore, ThemeMode } from '../store/themeStore';
import { cn } from '../utils/cn';

interface ThemeToggleProps {
  compact?: boolean;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ compact = false }) => {
  const { theme, setTheme } = useThemeStore();
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const themes: { id: ThemeMode; label: string; icon: any; desc: string; badge: string; iconColor: string }[] = [
    {
      id: 'light',
      label: 'Light',
      icon: Sun,
      desc: 'Clean academic white & crisp daylight typography',
      badge: 'Academic',
      iconColor: 'text-amber-500'
    },
    {
      id: 'dark',
      label: 'Dark',
      icon: Moon,
      desc: 'True black OLED & minimal green-accented surfaces',
      badge: 'True Black',
      iconColor: 'text-emerald-400'
    },
    {
      id: 'relax',
      label: 'Relax',
      icon: Sparkles,
      desc: 'Soft dusk lavender & warm misty neutral reading room',
      badge: 'Lavender',
      iconColor: 'text-purple-400'
    }
  ];

  const currentThemeObj = themes.find((t) => t.id === theme) || themes[0];
  const CurrentIcon = currentThemeObj.icon;

  if (compact) {
    return (
      <div className="relative" ref={containerRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle visual theme"
          className="p-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-card)] text-[var(--text-main)] hover:bg-[var(--bg-card-hover)] transition-all flex items-center justify-center gap-1.5 shadow-xs cursor-pointer"
          title={`Active Environment: ${currentThemeObj.label}`}
        >
          <CurrentIcon className={cn("w-4 h-4", currentThemeObj.iconColor)} />
        </button>

        {isOpen && (
          <div className="absolute right-0 mt-2 w-56 rounded-2xl shadow-2xl border border-[var(--border-color)] bg-[var(--bg-card)] text-[var(--text-main)] p-2 z-50 animate-in fade-in zoom-in-95 duration-150 backdrop-blur-md">
            <div className="px-2.5 py-1.5 text-[10px] font-black uppercase tracking-wider text-[var(--text-muted)]">
              Visual Environment
            </div>
            <div className="space-y-1">
              {themes.map((t) => {
                const Icon = t.icon;
                const isSelected = theme === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => {
                      setTheme(t.id);
                      setIsOpen(false);
                    }}
                    className={cn(
                      "w-full flex items-center justify-between px-2.5 py-2 rounded-xl text-left text-xs font-bold transition-all cursor-pointer",
                      isSelected
                        ? "bg-[var(--accent-soft)] text-[var(--accent-primary)] font-black"
                        : "text-[var(--text-main)] hover:bg-[var(--bg-card-hover)]"
                    )}
                  >
                    <div className="flex items-center gap-2">
                      <Icon className={cn("w-4 h-4", t.iconColor)} />
                      <span>{t.label}</span>
                    </div>
                    {isSelected && <Check className="w-3.5 h-3.5 text-[var(--accent-primary)]" />}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="relative inline-block" ref={containerRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="px-3 py-1.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-card)] text-[var(--text-main)] hover:bg-[var(--bg-card-hover)] text-xs font-bold transition-all flex items-center gap-2 shadow-xs cursor-pointer"
      >
        <CurrentIcon className={cn("w-3.5 h-3.5", currentThemeObj.iconColor)} />
        <span className="hidden sm:inline text-[11px] font-bold">{currentThemeObj.label}</span>
        <span className="text-[9px] px-1.5 py-0.2 rounded-md font-black uppercase tracking-wider bg-[var(--accent-soft)] text-[var(--accent-primary)]">
          {currentThemeObj.badge}
        </span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 rounded-2xl shadow-2xl border border-[var(--border-color)] bg-[var(--bg-card)] text-[var(--text-main)] p-2 z-50 animate-in fade-in zoom-in-95 duration-150 backdrop-blur-md">
          <div className="px-3 py-2 border-b border-[var(--border-subtle)] mb-1">
            <p className="text-[11px] font-black uppercase tracking-wider text-[var(--text-muted)]">Visual Atmosphere</p>
            <p className="text-[10px] text-[var(--text-muted)] font-medium">Choose your research environment</p>
          </div>
          <div className="space-y-1">
            {themes.map((t) => {
              const Icon = t.icon;
              const isSelected = theme === t.id;
              return (
                <button
                  key={t.id}
                  onClick={() => {
                    setTheme(t.id);
                    setIsOpen(false);
                  }}
                  className={cn(
                    "w-full flex items-start gap-2.5 px-3 py-2.5 rounded-xl text-left transition-all cursor-pointer group",
                    isSelected
                      ? "bg-[var(--accent-soft)] text-[var(--text-main)] font-bold border border-[var(--border-color)]"
                      : "text-[var(--text-main)] hover:bg-[var(--bg-card-hover)]"
                  )}
                >
                  <div className={cn(
                    "p-1.5 rounded-lg mt-0.5 shrink-0 transition-colors",
                    isSelected 
                      ? "bg-[var(--bg-card)] shadow-xs" 
                      : "bg-[var(--bg-surface)] group-hover:bg-[var(--bg-card)]"
                  )}>
                    <Icon className={cn("w-4 h-4", t.iconColor)} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold leading-tight">{t.label}</span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-[var(--accent-primary)] shrink-0" />}
                    </div>
                    <p className="text-[10px] text-[var(--text-muted)] font-medium leading-normal mt-0.5 line-clamp-1">{t.desc}</p>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
