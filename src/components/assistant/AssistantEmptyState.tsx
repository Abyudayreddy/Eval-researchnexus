import React from 'react';
import { BookOpen, FileText, BarChart2, Library, UploadCloud } from 'lucide-react';

interface AssistantEmptyStateProps {
  mode: string;
}

export const AssistantEmptyState: React.FC<AssistantEmptyStateProps> = ({ mode }) => {
  const getEmptyStateContent = () => {
    switch (mode) {
      case 'research':
        return {
          title: 'Research Mode',
          desc: 'Ask a research question to begin.',
          icon: BookOpen
        };
      case 'paper':
        return {
          title: 'Paper Mode',
          desc: 'Select a paper to begin paper-level research.',
          icon: FileText
        };
      case 'compare':
        return {
          title: 'Compare Mode',
          desc: 'Select 2–5 papers to compare.',
          icon: BarChart2
        };
      case 'evidence':
        return {
          title: 'Evidence Mode',
          desc: 'Select evidence to investigate.',
          icon: Library
        };
      case 'upload':
        return {
          title: 'Upload Mode',
          desc: 'Upload a research document.',
          icon: UploadCloud
        };
      default:
        return {
          title: 'Research Workspace',
          desc: 'Select a mode to begin.',
          icon: BookOpen
        };
    }
  };

  const content = getEmptyStateContent();
  const Icon = content.icon;

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-slate-50/50 rounded-2xl border border-dashed border-slate-200">
      <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 mb-4">
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-1">{content.title}</h3>
      <p className="text-xs text-slate-500 max-w-sm">{content.desc}</p>
    </div>
  );
};
