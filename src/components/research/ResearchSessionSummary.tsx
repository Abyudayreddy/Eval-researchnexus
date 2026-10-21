import React from 'react';
import { Download } from 'lucide-react';

interface ResearchSessionSummaryProps {
  sessionDetails?: any;
  onExport?: () => void;
}

export const ResearchSessionSummary: React.FC<ResearchSessionSummaryProps> = ({
  sessionDetails,
  onExport
}) => {
  if (!sessionDetails) return null;

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <span className="text-[10px] font-black uppercase tracking-wider px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded-full">
            Session Summary & Export
          </span>
          <h2 className="text-lg font-black text-slate-900 mt-1">{sessionDetails.title}</h2>
          <p className="text-xs text-slate-500 font-medium">{sessionDetails.description}</p>
        </div>

        {onExport && (
          <button
            onClick={onExport}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
          >
            <Download className="w-3.5 h-3.5" /> Export Session Package
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-center bg-slate-50 p-4 rounded-xl border border-slate-150 text-xs font-medium">
        <div>
          <span className="text-slate-400 block text-[10px] uppercase font-bold">Papers</span>
          <strong className="text-slate-900 text-base">{sessionDetails.stats?.paper_count || 0}</strong>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px] uppercase font-bold">Evidence Blocks</span>
          <strong className="text-slate-900 text-base">{sessionDetails.stats?.evidence_count || 0}</strong>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px] uppercase font-bold">Findings</span>
          <strong className="text-slate-900 text-base">{sessionDetails.stats?.finding_count || 0}</strong>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px] uppercase font-bold">Syntheses</span>
          <strong className="text-slate-900 text-base">{sessionDetails.stats?.synthesis_count || 0}</strong>
        </div>
      </div>
    </div>
  );
};
