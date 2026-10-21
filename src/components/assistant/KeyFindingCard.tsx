import React from 'react';
import { Target, Bookmark, Eye } from 'lucide-react';
import { cn } from '../../utils/cn';

interface KeyFindingCardProps {
  text: string;
  citations: number[];
  provenance: 'LOCAL' | 'ONLINE' | 'UPLOADED' | 'MIXED';
  onShowEvidence?: () => void;
  onSave?: () => void;
}

export const KeyFindingCard: React.FC<KeyFindingCardProps> = ({
  text,
  citations,
  provenance,
  onShowEvidence,
  onSave
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm relative hover:border-emerald-200 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1">
          <Target className="w-3.5 h-3.5 text-emerald-600" /> Key Finding
        </span>
        <span className={cn(
          "text-[9px] font-extrabold px-2 py-0.5 rounded border uppercase tracking-wider",
          provenance === 'LOCAL' && "bg-slate-50 text-slate-700 border-slate-200",
          provenance === 'ONLINE' && "bg-blue-50 text-blue-700 border-blue-200",
          provenance === 'UPLOADED' && "bg-amber-50 text-amber-700 border-amber-200",
          provenance === 'MIXED' && "bg-purple-50 text-purple-700 border-purple-200"
        )}>
          {provenance} Source
        </span>
      </div>
      <p className="text-xs font-semibold text-slate-700 leading-relaxed mb-3">
        {text}
      </p>
      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
        <div className="flex items-center gap-1">
          {citations.map((c) => (
            <span key={c} className="w-5 h-5 rounded bg-emerald-50 border border-emerald-100 text-[10px] font-bold text-emerald-700 flex items-center justify-center cursor-pointer hover:bg-emerald-100 transition-colors">
              [{c}]
            </span>
          ))}
        </div>
        <div className="flex items-center gap-2">
          {onShowEvidence && (
            <button 
              onClick={onShowEvidence}
              className="text-[10px] font-bold text-slate-500 hover:text-emerald-600 flex items-center gap-1 transition-colors"
            >
              <Eye className="w-3.5 h-3.5" /> Evidence
            </button>
          )}
          {onSave && (
            <button 
              onClick={onSave}
              className="text-[10px] font-bold text-slate-500 hover:text-emerald-600 flex items-center gap-1 transition-colors"
            >
              <Bookmark className="w-3.5 h-3.5" /> Save
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
