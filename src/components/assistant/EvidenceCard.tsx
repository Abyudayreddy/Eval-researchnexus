import React from 'react';
import { Library, CheckCircle } from 'lucide-react';
import { cn } from '../../utils/cn';

interface EvidenceCardProps {
  paperTitle: string;
  section?: string;
  page?: string;
  text: string;
  provenance: 'LOCAL' | 'ONLINE' | 'UPLOADED' | 'MIXED';
  onShowProof?: () => void;
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({
  paperTitle,
  section,
  page,
  text,
  provenance,
  onShowProof
}) => {
  return (
    <div className="bg-slate-50/50 border border-slate-200 rounded-xl p-4 hover:border-slate-300 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1">
          <Library className="w-3.5 h-3.5 text-emerald-600" /> Grounding Evidence
        </span>
        <span className={cn(
          "text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider",
          provenance === 'LOCAL' && "text-slate-500 bg-slate-100",
          provenance === 'ONLINE' && "text-blue-600 bg-blue-50",
          provenance === 'UPLOADED' && "text-amber-600 bg-amber-50",
          provenance === 'MIXED' && "text-purple-600 bg-purple-50"
        )}>
          {provenance}
        </span>
      </div>
      <h5 className="text-[11px] font-extrabold text-slate-800 line-clamp-1 mb-1">{paperTitle}</h5>
      <p className="text-xs text-slate-600 leading-relaxed italic mb-3 bg-white p-2.5 rounded-lg border border-slate-150">
        "{text}"
      </p>
      <div className="flex items-center justify-between text-[9px] font-bold text-slate-400 uppercase tracking-wider">
        <div className="flex items-center gap-3">
          <span>Section: {section || 'N/A'}</span>
          <span>Page: {page || 'N/A'}</span>
        </div>
        {onShowProof && (
          <button 
            onClick={onShowProof}
            className="text-emerald-600 hover:text-emerald-700 flex items-center gap-1 font-bold"
            title="Verify evidence claim via mathematical/grounded proof"
          >
            <CheckCircle className="w-3 h-3" /> Show Proof
          </button>
        )}
      </div>
    </div>
  );
};
