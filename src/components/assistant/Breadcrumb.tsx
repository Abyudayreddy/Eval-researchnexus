import React from 'react';
import { ChevronRight } from 'lucide-react';

interface BreadcrumbProps {
  mode: string;
  title?: string;
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({ mode, title }) => {
  const modeLabels: Record<string, string> = {
    research: 'Research Workspace',
    paper: 'Paper Workspace',
    compare: 'Comparison Board',
    evidence: 'Evidence Lab',
    upload: 'Corpus Ingestion',
  };

  return (
    <nav className="flex items-center gap-1.5 text-[11px] font-bold text-slate-400 uppercase tracking-widest" aria-label="Breadcrumb">
      <span>Assistant</span>
      <ChevronRight className="w-3 h-3 text-slate-300" />
      <span className="text-slate-600">{modeLabels[mode] || mode}</span>
      {title && (
        <>
          <ChevronRight className="w-3 h-3 text-slate-300" />
          <span className="text-slate-500 max-w-[200px] truncate">{title}</span>
        </>
      )}
    </nav>
  );
};
