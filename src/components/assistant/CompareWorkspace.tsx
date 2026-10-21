import React, { useState } from 'react';
import { FileText, Filter, CheckCircle, AlertTriangle, Download, Lock } from 'lucide-react';

interface EvidenceRef {
  paper_id: string;
  chunk_id: string;
  text: string;
  section?: string;
  page?: string;
  source_type: string;
}

interface MetricCompatibility {
  metric_name?: string;
  dataset?: string;
  split?: string;
  evaluation_protocol?: string;
  unit?: string;
  is_comparable: boolean;
  comparison_note: string;
}

interface ComparisonCell {
  paper_id: string;
  dimension: string;
  value: string;
  value_type: string;
  evidence_ids: string[];
  evidence_refs: EvidenceRef[];
  support_status: string;
  provenance: string;
  is_available: boolean;
}

interface ComparisonRow {
  dimension: string;
  cells: ComparisonCell[];
  comparison_claims: string[];
  metric_compatibility?: MetricCompatibility;
}

interface ComparisonMatrix {
  dimensions: string[];
  paper_ids: string[];
  rows: ComparisonRow[];
}

interface ComparisonSummary {
  similarities: string[];
  differences: string[];
  evidence_backed_findings: string[];
  potential_conflicts: string[];
  open_questions: string[];
}

interface CompareWorkspaceProps {
  papers: { id: string; title: string; authors?: string }[];
  resultData?: {
    matrix?: ComparisonMatrix;
    summary?: ComparisonSummary;
    context_snapshot_id?: string;
    context_hash?: string;
    verification_metrics?: any;
    latencies?: any;
  };
  isLoading?: boolean;
}

const ALL_DIMENSIONS = [
  "All",
  "Objective",
  "Research Problem",
  "Methodology",
  "Architecture/Model",
  "Dataset",
  "Experimental Setup",
  "Evaluation Metrics",
  "Results",
  "Limitations",
  "Future Work"
];

export const CompareWorkspace: React.FC<CompareWorkspaceProps> = ({
  papers,
  resultData,
  isLoading
}) => {
  const [selectedDimension, setSelectedDimension] = useState<string>("All");
  const [activeCellEvidence, setActiveCellEvidence] = useState<ComparisonCell | null>(null);

  const rows = resultData?.matrix?.rows || [];
  const filteredRows = selectedDimension === "All"
    ? rows
    : rows.filter(r => r.dimension.toLowerCase() === selectedDimension.toLowerCase());

  const handleExport = () => {
    if (!resultData) return;
    const jsonStr = JSON.stringify(resultData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `comparison_export_${resultData.context_hash || 'reproducible'}.json`;
    a.click();
  };

  return (
    <div className="w-full flex flex-col gap-6 p-6 bg-slate-50 min-h-screen">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-100 text-indigo-800 uppercase tracking-wide">
              Compare Mode
            </span>
            <span className="flex items-center gap-1 text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              <Lock className="w-3 h-3" /> Context Locked
            </span>
          </div>
          <h1 className="text-xl font-black text-slate-900">Multi-Paper Scientific Comparison Workspace</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Comparing <span className="font-bold text-slate-700">{papers.length} selected papers</span> (Bound strictly to [2–5] papers).
          </p>
        </div>

        <div className="flex items-center gap-2">
          {resultData && (
            <button
              onClick={handleExport}
              className="flex items-center gap-1.5 px-3 py-2 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition"
            >
              <Download className="w-3.5 h-3.5" /> Export Markdown/JSON
            </button>
          )}
        </div>
      </div>

      {/* Selected Papers Tags */}
      <div className="flex flex-wrap gap-2 items-center bg-white border border-slate-200 rounded-xl p-3 shadow-sm">
        <span className="text-xs font-black text-slate-400 uppercase tracking-wider mr-2">Selected ({papers.length}):</span>
        {papers.map((p, idx) => (
          <div key={p.id} className="flex items-center gap-1.5 bg-slate-100 border border-slate-200 rounded-lg px-3 py-1 text-xs font-medium text-slate-700">
            <span className="font-bold text-indigo-600">[{String.fromCharCode(65 + idx)}]</span>
            <span className="truncate max-w-[200px]">{p.title}</span>
          </div>
        ))}
      </div>

      {/* Dimension Filter Bar */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
        <Filter className="w-4 h-4 text-slate-400 mr-1 flex-shrink-0" />
        {ALL_DIMENSIONS.map((dim) => (
          <button
            key={dim}
            onClick={() => setSelectedDimension(dim)}
            className={`px-3 py-1.5 text-xs font-bold rounded-xl transition flex-shrink-0 ${
              selectedDimension === dim
                ? 'bg-slate-900 text-white shadow-sm'
                : 'bg-white text-slate-600 hover:bg-slate-200/60 border border-slate-200'
            }`}
          >
            {dim}
          </button>
        ))}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center shadow-sm flex flex-col items-center justify-center gap-3">
          <div className="w-8 h-8 border-3 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-bold text-slate-700">Synthesizing Evidence-Grounded Comparison Matrix...</p>
          <p className="text-xs text-slate-400">Verifying claims & metric compatibility across selected papers</p>
        </div>
      )}

      {/* Comparison Matrix Grid */}
      {!isLoading && filteredRows.length > 0 && (
        <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-xs font-black text-slate-700 uppercase tracking-wider">
                  <th className="p-4 w-48 bg-slate-100/80 sticky left-0 z-10">Dimension</th>
                  {papers.map((p, idx) => (
                    <th key={p.id} className="p-4 min-w-[280px]">
                      <span className="text-indigo-600 font-bold mr-1.5">[{String.fromCharCode(65 + idx)}]</span>
                      {p.title}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {filteredRows.map((row) => (
                  <React.Fragment key={row.dimension}>
                    <tr className="hover:bg-slate-50/50 transition">
                      <td className="p-4 font-black text-slate-800 bg-slate-50/50 sticky left-0 z-10 border-r border-slate-200">
                        {row.dimension}
                      </td>
                      {papers.map((p) => {
                        const cell = row.cells.find(c => c.paper_id === p.id);
                        if (!cell || !cell.is_available) {
                          return (
                            <td key={p.id} className="p-4 text-amber-600 bg-amber-50/30 italic font-medium">
                              Not available in selected evidence.
                            </td>
                          );
                        }

                        return (
                          <td key={p.id} className="p-4 text-slate-700 align-top space-y-2">
                            <p className="leading-relaxed font-medium">{cell.value}</p>

                            <div className="flex items-center justify-between pt-1">
                              <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase ${
                                cell.support_status === 'SUPPORTED' ? 'bg-emerald-100 text-emerald-800' :
                                cell.support_status === 'PARTIALLY_SUPPORTED' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'
                              }`}>
                                {cell.support_status}
                              </span>

                              {cell.evidence_ids.length > 0 && (
                                <button
                                  onClick={() => setActiveCellEvidence(cell)}
                                  className="text-[11px] font-bold text-indigo-600 hover:text-indigo-800 underline flex items-center gap-1"
                                >
                                  <FileText className="w-3 h-3" /> Evidence ({cell.evidence_ids.length})
                                </button>
                              )}
                            </div>
                          </td>
                        );
                      })}
                    </tr>

                    {/* Metric Compatibility Warning Row */}
                    {row.metric_compatibility && !row.metric_compatibility.is_comparable && (
                      <tr className="bg-amber-50/60 border-t border-b border-amber-200">
                        <td colSpan={papers.length + 1} className="p-3 px-4 text-xs font-semibold text-amber-900 flex items-center gap-2">
                          <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0" />
                          <span>
                            <strong className="font-bold">Metric Compatibility Note:</strong> {row.metric_compatibility.comparison_note}
                          </span>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Comparison Synthesis & Findings Summary */}
      {!isLoading && resultData?.summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Similarities & Differences */}
          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600" /> Key Similarities & Differences
            </h3>
            <div className="space-y-3">
              <div>
                <h4 className="text-xs font-extrabold text-slate-500 mb-1">SIMILARITIES</h4>
                <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 font-medium">
                  {resultData.summary.similarities.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
              <div>
                <h4 className="text-xs font-extrabold text-slate-500 mb-1">KEY DIFFERENCES</h4>
                <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 font-medium">
                  {resultData.summary.differences.map((d, i) => <li key={i}>{d}</li>)}
                </ul>
              </div>
            </div>
          </div>

          {/* Potential Conflicts & Open Questions */}
          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-600" /> Potential Conflict Candidates & Open Gaps
            </h3>
            <div className="space-y-3">
              <div>
                <h4 className="text-xs font-extrabold text-amber-700 mb-1">POTENTIAL CONFLICT CANDIDATES</h4>
                {resultData.summary.potential_conflicts.length > 0 ? (
                  <ul className="list-disc list-inside text-xs text-amber-900 space-y-1 font-medium bg-amber-50/50 p-2.5 rounded-xl border border-amber-200">
                    {resultData.summary.potential_conflicts.map((c, i) => <li key={i}>{c}</li>)}
                  </ul>
                ) : (
                  <p className="text-xs text-slate-400 italic">No explicit candidate conflicts detected across evidence.</p>
                )}
              </div>
              <div>
                <h4 className="text-xs font-extrabold text-slate-500 mb-1">OPEN QUESTIONS</h4>
                <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 font-medium">
                  {resultData.summary.open_questions.map((q, i) => <li key={i}>{q}</li>)}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cell Evidence Drawer Modal */}
      {activeCellEvidence && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex justify-end">
          <div className="w-full max-w-lg bg-white h-full shadow-2xl p-6 overflow-y-auto flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-slate-200 pb-4 mb-4">
                <div>
                  <span className="text-xs font-bold text-indigo-600 uppercase">Evidence Inspector</span>
                  <h3 className="text-base font-black text-slate-900">{activeCellEvidence.dimension}</h3>
                </div>
                <button
                  onClick={() => setActiveCellEvidence(null)}
                  className="text-xs font-bold px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg"
                >
                  Close
                </button>
              </div>

              <div className="space-y-4">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <p className="text-xs font-bold text-slate-700">Cell Claim Value:</p>
                  <p className="text-xs text-slate-600 mt-1">{activeCellEvidence.value}</p>
                </div>

                <h4 className="text-xs font-black text-slate-500 uppercase tracking-wider">CITED EVIDENCE CHUNKS ({activeCellEvidence.evidence_refs.length})</h4>
                {activeCellEvidence.evidence_refs.map((ref, idx) => (
                  <div key={idx} className="bg-indigo-50/50 border border-indigo-200 rounded-xl p-3 text-xs space-y-1.5">
                    <div className="flex justify-between items-center text-[10px] font-bold text-indigo-700">
                      <span>Chunk [{ref.chunk_id}]</span>
                      <span>Section: {ref.section || 'Main'} | Page: {ref.page || '1'}</span>
                    </div>
                    <p className="text-slate-800 font-medium italic">"{ref.text}"</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-200">
              <p className="text-[11px] text-slate-400 font-medium">Phase 3.6 Grounded Attribution Inspector</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
