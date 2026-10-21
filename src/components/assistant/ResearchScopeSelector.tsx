import React from 'react';
import { cn } from '../../utils/cn';
import { Target, ChevronDown } from 'lucide-react';

interface ResearchScopeSelectorProps {
  activeScope: string;
  onChangeScope: (scope: string) => void;
  allowedScopes: string[];
}

export const ResearchScopeSelector: React.FC<ResearchScopeSelectorProps> = ({ 
  activeScope, 
  onChangeScope, 
  allowedScopes 
}) => {
  const scopeLabels: Record<string, string> = {
    all_research: 'All Research',
    selected_papers: 'Selected Papers',
    single_paper: 'Single Paper',
    current_evidence: 'Current Evidence',
    uploaded_documents: 'Uploaded Documents',
  };

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1">
        <Target className="w-3.5 h-3.5" /> Scope:
      </span>
      <div className="relative inline-block text-left">
        <select
          value={activeScope}
          onChange={(e) => onChangeScope(e.target.value)}
          className={cn(
            "appearance-none bg-white border border-slate-200 rounded-lg pl-3 pr-8 py-1.5 text-xs font-bold text-slate-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 cursor-pointer"
          )}
          aria-label="Research Scope Selection"
        >
          {allowedScopes.map((scope) => (
            <option key={scope} value={scope}>
              {scopeLabels[scope] || scope}
            </option>
          ))}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-500">
          <ChevronDown className="w-3 h-3" />
        </div>
      </div>
    </div>
  );
};
