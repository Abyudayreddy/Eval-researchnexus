import React from 'react';
import { Library, ExternalLink, Bookmark, Info } from 'lucide-react';

interface EvidencePreviewProps {
  sourceType: string;
  title: string;
  section?: string;
  page?: string;
  text: string;
  onOpenPaper?: () => void;
  onExplain?: () => void;
  onSave?: () => void;
}

export const EvidencePreview: React.FC<EvidencePreviewProps> = ({
  sourceType,
  title,
  section,
  page,
  text,
  onOpenPaper,
  onExplain,
  onSave
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-3">
        <div className="flex items-center gap-2">
          <Library className="w-4 h-4 text-emerald-600" />
          <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md uppercase tracking-wider">
            {sourceType}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          {onOpenPaper && (
            <button 
              onClick={onOpenPaper} 
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-50 transition-colors"
              title="Open Paper"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </button>
          )}
          {onExplain && (
            <button 
              onClick={onExplain} 
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-50 transition-colors"
              title="Explain Evidence"
            >
              <Info className="w-3.5 h-3.5" />
            </button>
          )}
          {onSave && (
            <button 
              onClick={onSave} 
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-50 transition-colors"
              title="Save Evidence"
            >
              <Bookmark className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <h4 className="text-xs font-bold text-slate-800 line-clamp-1">{title}</h4>
        <p className="text-xs text-slate-600 leading-relaxed italic bg-slate-50 p-2.5 rounded-lg border border-slate-100">
          "{text}"
        </p>
        <div className="flex items-center gap-4 text-[10px] font-bold text-slate-400 uppercase">
          <span>Section: {section || 'N/A'}</span>
          <span>Page: {page || 'N/A'}</span>
        </div>
      </div>
    </div>
  );
};
