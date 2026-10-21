import React from 'react';
import { cn } from '../../utils/cn';
import { Shield, BookOpen, Layers, Library } from 'lucide-react';

interface PaperRef {
  paper_id: string;
  title: string;
  authors: string;
  source_type: string;
}

interface EvidenceRef {
  paper_id: string;
  chunk_id: string;
  section?: string;
  page?: string;
  text: string;
}

interface ResearchContextPanelProps {
  scope: string;
  papers: PaperRef[];
  evidence: EvidenceRef[];
  provenance: string;
  isOpen: boolean;
}

export const ResearchContextPanel: React.FC<ResearchContextPanelProps> = ({
  scope,
  papers,
  evidence,
  provenance,
  isOpen
}) => {
  const scopeLabels: Record<string, string> = {
    all_research: 'All Research',
    selected_papers: 'Selected Papers',
    single_paper: 'Single Paper',
    current_evidence: 'Current Evidence',
    uploaded_documents: 'Uploaded Documents',
  };

  const localCount = papers.filter(p => p.source_type === 'local').length;
  const onlineCount = papers.filter(p => p.source_type === 'online').length;

  return (
    <div className={cn(
      "border-r border-slate-200 bg-slate-50 transition-all duration-300 flex flex-col shrink-0 overflow-y-auto",
      isOpen ? "w-80" : "w-0 border-r-0 overflow-hidden"
    )}>
      <div className="p-5 border-b border-slate-200 flex items-center justify-between bg-white">
        <h3 className="text-xs font-black text-slate-800 uppercase tracking-widest flex items-center gap-2">
          <Shield className="w-4 h-4 text-emerald-600" /> Research Context
        </h3>
      </div>

      <div className="p-5 space-y-6 flex-1">
        {/* Scope info */}
        <div>
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Scope</span>
          <div className="flex items-center gap-2 bg-white border border-slate-200 rounded-xl p-3 shadow-sm">
            <Layers className="w-4 h-4 text-emerald-600" />
            <span className="text-xs font-bold text-slate-800">{scopeLabels[scope] || scope}</span>
          </div>
        </div>

        {/* Provenance */}
        <div>
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Provenance</span>
          <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm text-xs font-bold text-slate-800">
            {provenance}
          </div>
        </div>

        {/* Sources counts */}
        <div>
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Sources Summary</span>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm text-center">
              <span className="text-[10px] font-bold text-slate-400 uppercase block">Local</span>
              <span className="text-lg font-black text-slate-800">{localCount}</span>
            </div>
            <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm text-center">
              <span className="text-[10px] font-bold text-slate-400 uppercase block">Online</span>
              <span className="text-lg font-black text-slate-800">{onlineCount}</span>
            </div>
          </div>
        </div>

        {/* Active papers */}
        {papers.length > 0 && (
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">
              Active Papers ({papers.length})
            </span>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {papers.map((p, idx) => (
                <div key={idx} className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex items-start gap-2">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 line-clamp-2">{p.title}</h4>
                    <span className="text-[10px] font-bold text-slate-400">{p.authors}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Active evidence chunks */}
        {evidence.length > 0 && (
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">
              Active Evidence Blocks ({evidence.length})
            </span>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {evidence.map((ev, idx) => (
                <div key={idx} className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm flex items-start gap-2">
                  <Library className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-800 line-clamp-2">{ev.text}</h4>
                    <span className="text-[9px] font-bold text-slate-400 block mt-1">
                      Page {ev.page || 'N/A'} | Section {ev.section || 'N/A'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
