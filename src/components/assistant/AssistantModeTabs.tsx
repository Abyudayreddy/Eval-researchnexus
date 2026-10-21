import React from 'react';
import { cn } from '../../utils/cn';
import { BookOpen, FileText, BarChart2, Library, UploadCloud } from 'lucide-react';

interface AssistantModeTabsProps {
  activeMode: string;
  onChangeMode: (mode: string) => void;
}

export const AssistantModeTabs: React.FC<AssistantModeTabsProps> = ({ activeMode, onChangeMode }) => {
  const tabs = [
    { id: 'research', label: 'Research', icon: BookOpen },
    { id: 'paper', label: 'Paper', icon: FileText },
    { id: 'compare', label: 'Compare', icon: BarChart2 },
    { id: 'evidence', label: 'Evidence', icon: Library },
    { id: 'upload', label: 'Upload', icon: UploadCloud },
  ];

  return (
    <div className="flex border-b border-slate-200 bg-white">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeMode === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onChangeMode(tab.id)}
            className={cn(
              "flex items-center gap-2 px-6 py-3 text-sm font-bold border-b-2 transition-all",
              isActive 
                ? "border-emerald-500 text-emerald-600 bg-emerald-50/10" 
                : "border-transparent text-slate-500 hover:text-slate-700 hover:bg-slate-50"
            )}
            aria-label={`${tab.label} Mode`}
          >
            <Icon className={cn("w-4 h-4", isActive ? "text-emerald-500" : "text-slate-400")} />
            {tab.label}
          </button>
        );
      })}
    </div>
  );
};
