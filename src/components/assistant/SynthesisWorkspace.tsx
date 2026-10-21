import React, { useState } from 'react';
import { Layers, FileText, ChevronDown, ChevronRight, CheckCircle2, Download, ShieldAlert, Sparkles } from 'lucide-react';

interface EvidenceRef {
  paper_id: string;
  chunk_id: string;
  text: string;
  section?: string;
  page?: string;
  source_type: string;
}

interface ResearchTheme {
  theme_id: string;
  name: string;
  description: string;
  paper_ids: string[];
  evidence_ids: string[];
  support_status: string;
  source_types: string[];
}

interface ContradictionCandidate {
  conflict_id: string;
  conflict_type: string;
  paper_a_id: string;
  paper_b_id: string;
  claim_a: string;
  claim_b: string;
  evidence_a_ids: string[];
  evidence_b_ids: string[];
  conflict_basis: string;
  support_status: string;
}

interface ResearchGapCandidate {
  gap_id: string;
  category: string;
  title: string;
  observed_coverage: string;
  missing_dimension: string;
  reason: string;
  evidence_strength: string;
  paper_ids: string[];
  evidence_ids: string[];
  support_status: string;
}

interface SynthesisResultData {
  synthesis_id?: string;
  context_snapshot_id?: string;
  context_hash?: string;
  scope?: string;
  analysis_scope?: string;
  coverage_statement?: string;
  themes?: ResearchTheme[];
  agreements?: string[];
  differences?: string[];
  limitations?: string[];
  potential_conflicts?: ContradictionCandidate[];
  gap_candidates?: ResearchGapCandidate[];
  evidence?: EvidenceRef[];
  latencies?: any;
}

interface SynthesisWorkspaceProps {
  papers: { id: string; title: string; authors?: string }[];
  resultData?: SynthesisResultData;
  isLoading?: boolean;
  onOpenProof?: (claimText: string) => void;
}

export const SynthesisWorkspace: React.FC<SynthesisWorkspaceProps> = ({
  papers,
  resultData,
  isLoading,
  onOpenProof
}) => {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    themes: true,
    agreements: true,
    differences: true,
    conflicts: true,
    gaps: true,
    directions: true
  });

  const toggleSection = (section: string) => {
    setOpenSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const handleExport = () => {
    if (!resultData) return;
    const jsonStr = JSON.stringify(resultData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `synthesis_export_${resultData.context_hash || 'reproducible'}.json`;
    a.click();
  };

  const totalEvidenceCount = resultData?.evidence?.length || 0;

  return (
    <div className="w-full flex flex-col gap-6 p-6 bg-slate-50 min-h-screen">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-100 text-purple-800 uppercase tracking-wide">
              Literature Synthesis Engine
            </span>
            <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-full">
              Snapshot: {resultData?.context_snapshot_id || 'v1'}
            </span>
          </div>
          <h1 className="text-xl font-black text-slate-900">Literature Reasoning & Research Gap Workspace</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Scope: <span className="font-bold text-slate-700">{resultData?.analysis_scope || `${papers.length} selected papers`}</span> ({totalEvidenceCount} Evidence Blocks)
          </p>
          <p className="text-[11px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200 mt-1 inline-block font-medium">
            {resultData?.coverage_statement || "Findings reflect the selected literature only."}
          </p>
        </div>

        <div className="flex items-center gap-2">
          {resultData && (
            <button
              onClick={handleExport}
              className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition"
            >
              <Download className="w-3.5 h-3.5" /> Export Synthesis JSON/Markdown
            </button>
          )}
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center shadow-sm flex flex-col items-center justify-center gap-3">
          <div className="w-8 h-8 border-3 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-bold text-slate-700">Synthesizing Literature & Identifying Research Gaps...</p>
          <p className="text-xs text-slate-400">Analyzing themes, candidate conflicts, and evidence strength across selected literature</p>
        </div>
      )}

      {!isLoading && resultData && (
        <div className="space-y-4">

          {/* 1. KEY THEMES SECTION */}
          <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <button
              onClick={() => toggleSection('themes')}
              className="w-full flex items-center justify-between p-4 bg-slate-50/80 hover:bg-slate-100/80 transition text-left border-b border-slate-200"
            >
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-purple-600" />
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Key Research Themes ({resultData.themes?.length || 0})</h3>
              </div>
              {openSections.themes ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
            </button>

            {openSections.themes && (
              <div className="p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
                {resultData.themes?.map((t) => (
                  <div key={t.theme_id} className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-black text-slate-800">{t.name}</h4>
                      <span className="text-[10px] font-bold px-2 py-0.5 bg-purple-50 text-purple-700 rounded-full border border-purple-200">
                        {t.evidence_ids.length} Evidence Blocks
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 font-medium">{t.description}</p>
                    <div className="flex items-center gap-1 text-[10px] font-bold text-slate-400">
                      <span>Represented in {t.paper_ids.length} Papers</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 2. AREAS OF AGREEMENT SECTION */}
          <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <button
              onClick={() => toggleSection('agreements')}
              className="w-full flex items-center justify-between p-4 bg-slate-50/80 hover:bg-slate-100/80 transition text-left border-b border-slate-200"
            >
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Areas of Agreement ({resultData.agreements?.length || 0})</h3>
              </div>
              {openSections.agreements ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
            </button>

            {openSections.agreements && (
              <div className="p-5 space-y-3">
                {resultData.agreements?.map((ag, idx) => (
                  <div key={idx} className="bg-emerald-50/40 border border-emerald-200 rounded-xl p-3.5 text-xs text-slate-800 font-medium leading-relaxed flex items-start gap-2 justify-between">
                    <span>{ag}</span>
                    {onOpenProof && (
                      <button
                        onClick={() => onOpenProof(ag)}
                        className="text-[10px] font-bold px-2 py-1 bg-white border border-emerald-200 text-emerald-700 rounded hover:bg-emerald-50 shrink-0"
                      >
                        Show Proof
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 3. MAJOR DIFFERENCES SECTION */}
          <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <button
              onClick={() => toggleSection('differences')}
              className="w-full flex items-center justify-between p-4 bg-slate-50/80 hover:bg-slate-100/80 transition text-left border-b border-slate-200"
            >
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-600" />
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Major Differences ({resultData.differences?.length || 0})</h3>
              </div>
              {openSections.differences ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
            </button>

            {openSections.differences && (
              <div className="p-5 space-y-3">
                {resultData.differences?.map((diff, idx) => (
                  <div key={idx} className="bg-blue-50/40 border border-blue-200 rounded-xl p-3.5 text-xs text-slate-800 font-medium leading-relaxed">
                    {diff}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 4. POTENTIAL CONFLICT CANDIDATES SECTION */}
          <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <button
              onClick={() => toggleSection('conflicts')}
              className="w-full flex items-center justify-between p-4 bg-slate-50/80 hover:bg-slate-100/80 transition text-left border-b border-slate-200"
            >
              <div className="flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-600" />
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Potential Conflict Candidates ({resultData.potential_conflicts?.length || 0})</h3>
              </div>
              {openSections.conflicts ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
            </button>

            {openSections.conflicts && (
              <div className="p-5 space-y-4">
                {resultData.potential_conflicts?.map((c) => (
                  <div key={c.conflict_id} className="bg-amber-50/40 border border-amber-200 rounded-xl p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-extrabold uppercase px-2.5 py-0.5 bg-amber-100 text-amber-800 rounded-full">
                        {c.conflict_type.replace('_', ' ')}
                      </span>
                      <span className="text-[10px] font-bold text-amber-700">Potential Conflict Candidate</span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                      <div className="bg-white p-3 rounded-lg border border-amber-100">
                        <span className="font-bold text-slate-500 block mb-1">Paper [{c.paper_a_id}]:</span>
                        <p className="text-slate-800 font-medium">{c.claim_a}</p>
                      </div>
                      <div className="bg-white p-3 rounded-lg border border-amber-100">
                        <span className="font-bold text-slate-500 block mb-1">Paper [{c.paper_b_id}]:</span>
                        <p className="text-slate-800 font-medium">{c.claim_b}</p>
                      </div>
                    </div>

                    <p className="text-xs text-amber-900 font-medium italic bg-white/60 p-2.5 rounded-lg border border-amber-200">
                      <strong>Conflict Basis:</strong> {c.conflict_basis}
                    </p>
                  </div>
                ))}
                {(!resultData.potential_conflicts || resultData.potential_conflicts.length === 0) && (
                  <p className="text-xs text-slate-400 italic">No explicit candidate conflicts detected across evidence.</p>
                )}
              </div>
            )}
          </div>

          {/* 5. POTENTIAL RESEARCH GAPS SECTION */}
          <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <button
              onClick={() => toggleSection('gaps')}
              className="w-full flex items-center justify-between p-4 bg-slate-50/80 hover:bg-slate-100/80 transition text-left border-b border-slate-200"
            >
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-indigo-600" />
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Potential Research Gaps ({resultData.gap_candidates?.length || 0})</h3>
              </div>
              {openSections.gaps ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
            </button>

            {openSections.gaps && (
              <div className="p-5 space-y-4">
                {resultData.gap_candidates?.map((gap) => (
                  <div key={gap.gap_id} className="bg-indigo-50/40 border border-indigo-200 rounded-xl p-4 space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-extrabold uppercase px-2.5 py-0.5 bg-indigo-100 text-indigo-800 rounded-full">
                          {gap.category.replace('_', ' ')}
                        </span>
                        <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded ${
                          gap.evidence_strength === 'STRONG_EVIDENCE' ? 'bg-emerald-100 text-emerald-800' :
                          gap.evidence_strength === 'MODERATE_EVIDENCE' ? 'bg-blue-100 text-blue-800' : 'bg-slate-200 text-slate-700'
                        }`}>
                          {gap.evidence_strength.replace('_', ' ')}
                        </span>
                      </div>

                      <span className="text-[10px] font-bold text-slate-400">Auditable Gap Candidate</span>
                    </div>

                    <h4 className="text-sm font-black text-indigo-950">{gap.title}</h4>

                    <div className="bg-white p-3 rounded-lg border border-indigo-100 space-y-1.5 text-xs">
                      <p className="text-slate-700"><strong>Observed Coverage:</strong> {gap.observed_coverage}</p>
                      <p className="text-slate-700"><strong>Missing Dimension:</strong> {gap.missing_dimension}</p>
                      <p className="text-slate-600 italic"><strong>Reasoning:</strong> {gap.reason}</p>
                    </div>

                    <div className="flex items-center justify-between pt-1">
                      <span className="text-[10px] font-bold text-slate-400">Observed across {gap.paper_ids.length} Papers</span>
                      <div className="flex items-center gap-2">
                        {onOpenProof && (
                          <button
                            onClick={() => onOpenProof(gap.title)}
                            className="text-[11px] font-bold px-2.5 py-1 bg-white border border-indigo-200 text-indigo-700 rounded hover:bg-indigo-50"
                          >
                            Show Proof
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
};
