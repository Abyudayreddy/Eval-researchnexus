import React, { useEffect, useState } from 'react';
import { 
  ArrowLeft, Download, Layers, CheckCircle2, AlertCircle, X, ChevronDown, ChevronRight
} from 'lucide-react';
import { ComparisonArtifact, ComparisonCell } from '../../models/ResearchContext';

interface ComparisonModalOverlayProps {
  isOpen: boolean;
  onClose: () => void;
  comparisonData: ComparisonArtifact | null;
  isLoading?: boolean;
  loadingStage?: string;
  error?: string | null;
  onChangeSelection: () => void;
}

export const ComparisonModalOverlay: React.FC<ComparisonModalOverlayProps> = ({
  isOpen,
  onClose,
  comparisonData,
  isLoading = false,
  loadingStage = 'Extracting paper-specific evidence...',
  error = null,
  onChangeSelection
}) => {
  const [selectedEvidenceCell, setSelectedEvidenceCell] = useState<{
    cell: ComparisonCell;
    paperTitle: string;
  } | null>(null);

  const [showSynthesis, setShowSynthesis] = useState<boolean>(false);
  const [activeExportMenu, setActiveExportMenu] = useState<boolean>(false);

  // Close on Escape key press
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (selectedEvidenceCell) {
          setSelectedEvidenceCell(null);
        } else {
          onClose();
        }
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose, selectedEvidenceCell]);

  if (!isOpen) return null;

  const papers = comparisonData?.papers || [];
  const rows = comparisonData?.matrix?.rows || [];

  const handleExport = (format: 'json' | 'csv' | 'markdown') => {
    if (!comparisonData) return;
    let content = '';
    let filename = `comparison_${comparisonData.comparison_id}`;
    let mimeType = 'text/plain';

    if (format === 'json') {
      content = JSON.stringify(comparisonData, null, 2);
      filename += '.json';
      mimeType = 'application/json';
    } else if (format === 'csv') {
      const header = ['Research Dimension', ...papers.map(p => `"${p.title.replace(/"/g, '""')}"`)].join(',');
      const csvRows = rows.map(r => {
        const cellVals = papers.map(p => {
          const c = r.cells.find(cell => cell.paper_id === p.paper_id);
          const val = c ? (c.status === 'EVIDENCE_BACKED' ? c.value : c.status) : 'NOT_REPORTED';
          return `"${val.replace(/"/g, '""')}"`;
        });
        return [`"${r.dimension}"`, ...cellVals].join(',');
      });
      content = [header, ...csvRows].join('\n');
      filename += '.csv';
      mimeType = 'text/csv';
    } else if (format === 'markdown') {
      const header = `| Research Dimension | ${papers.map(p => p.title).join(' | ')} |`;
      const separator = `| --- | ${papers.map(() => '---').join(' | ')} |`;
      const mdRows = rows.map(r => {
        const cellVals = papers.map(p => {
          const c = r.cells.find(cell => cell.paper_id === p.paper_id);
          return c ? (c.status === 'EVIDENCE_BACKED' ? c.value.replace(/\n/g, ' ') : c.status) : 'NOT_REPORTED';
        });
        return `| **${r.dimension}** | ${cellVals.join(' | ')} |`;
      });
      content = [`# Multi-Paper Comparison (${comparisonData.comparison_id})`, '', header, separator, ...mdRows].join('\n');
      filename += '.md';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    setActiveExportMenu(false);
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 md:p-8 animate-in fade-in duration-200"
      role="dialog"
      aria-modal="true"
    >
      {/* BACKGROUND BACKDROP (BLURRED + SOFTLY DIMMED) */}
      <div 
        className="fixed inset-0 bg-[var(--modal-backdrop)] backdrop-blur-md transition-opacity"
        onClick={onClose}
      />

      {/* COMPARISON WORKSPACE MODAL CONTAINER */}
      <div className="relative w-full max-w-7xl h-[92vh] bg-[var(--bg-card)] rounded-2xl shadow-2xl border border-[var(--border-color)] flex flex-col overflow-hidden z-10 text-[var(--text-main)]">
        
        {/* HEADER */}
        <div className="px-6 py-4 bg-[var(--bg-card)] border-b border-[var(--border-color)] flex flex-col sm:flex-row sm:items-center justify-between gap-4 shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-colors flex items-center gap-1.5 text-xs font-bold"
              title="Return to Explore Papers"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
            <div className="h-4 w-px bg-slate-200" />
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-emerald-100 text-emerald-800">
                  MULTI-PAPER COMPARISON
                </span>
                {comparisonData && (
                  <span className="text-[11px] font-mono text-slate-400">
                    ID: {comparisonData.comparison_id}
                  </span>
                )}
              </div>
              <h2 className="text-base font-black text-slate-900 mt-0.5">
                Evidence-Grounded Comparison Across 10 Research Dimensions
              </h2>
            </div>
          </div>

          <div className="flex items-center gap-2 self-end sm:self-auto">
            <div className="text-xs font-bold text-slate-500 mr-2">
              Selected Papers: <span className="text-emerald-700 font-black">{papers.length}</span>
            </div>
            <button
              onClick={() => {
                onClose();
                onChangeSelection();
              }}
              className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors"
            >
              Change Selection
            </button>

            {/* EXPORT DROPDOWN */}
            <div className="relative">
              <button
                onClick={() => setActiveExportMenu(!activeExportMenu)}
                className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl flex items-center gap-1.5 transition-colors shadow-sm"
              >
                <Download className="w-3.5 h-3.5" /> Export
              </button>
              {activeExportMenu && (
                <div className="absolute right-0 mt-1 w-36 bg-white border border-slate-200 rounded-xl shadow-lg py-1.5 z-30 text-xs font-medium">
                  <button onClick={() => handleExport('markdown')} className="w-full text-left px-3 py-1.5 hover:bg-slate-50">Markdown</button>
                  <button onClick={() => handleExport('csv')} className="w-full text-left px-3 py-1.5 hover:bg-slate-50">CSV</button>
                  <button onClick={() => handleExport('json')} className="w-full text-left px-3 py-1.5 hover:bg-slate-50">JSON (Full)</button>
                </div>
              )}
            </div>

            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-slate-700 rounded-xl hover:bg-slate-100 transition-colors ml-1"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* BODY AREA */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-[#FBFDFB]">
          
          {/* LOADING STATE */}
          {isLoading && (
            <div className="p-12 text-center space-y-4 max-w-md mx-auto my-12 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto border border-emerald-100 animate-spin">
                <Layers className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-black text-slate-900">Preparing Multi-Paper Comparison</h3>
              <p className="text-xs text-slate-500">{loadingStage}</p>
              <div className="space-y-1.5 text-left text-xs text-slate-600 bg-slate-50 p-3.5 rounded-xl border border-slate-100 font-mono">
                <div className="flex items-center gap-2 text-emerald-700 font-bold">✓ Papers selected ({papers.length || 3})</div>
                <div className="flex items-center gap-2 text-emerald-700 font-bold">✓ Paper contexts resolved</div>
                <div className="flex items-center gap-2 text-amber-700 font-bold animate-pulse">● Extracting paper-specific evidence...</div>
                <div className="flex items-center gap-2 text-slate-400">○ Building strict attribution matrix</div>
              </div>
            </div>
          )}

          {/* ERROR STATE */}
          {error && !isLoading && (
            <div className="p-8 text-center space-y-3 max-w-md mx-auto my-12 bg-rose-50 border border-rose-200 rounded-2xl">
              <AlertCircle className="w-8 h-8 text-rose-600 mx-auto" />
              <h3 className="text-sm font-bold text-rose-900">Unable to prepare comparison</h3>
              <p className="text-xs text-rose-700">{error}</p>
              <button
                onClick={onClose}
                className="mt-2 px-4 py-1.5 bg-rose-700 hover:bg-rose-800 text-white rounded-xl text-xs font-bold"
              >
                Back to Papers
              </button>
            </div>
          )}

          {/* LOADED COMPARISON CONTENT */}
          {!isLoading && !error && comparisonData && (
            <>
              {/* COMPACT PAPER HEADER CARDS */}
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                {papers.map((p, idx) => (
                  <div key={p.paper_id} className="p-3 bg-white border border-slate-200 rounded-xl shadow-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-black uppercase text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                        Paper {idx + 1}
                      </span>
                      <span className="text-[10px] font-mono text-slate-400">
                        {p.year || '2024'}
                      </span>
                    </div>
                    <h4 className="text-xs font-bold text-slate-900 line-clamp-2" title={p.title}>
                      {p.title}
                    </h4>
                    <p className="text-[11px] text-slate-500 truncate" title={p.authors}>
                      {p.authors}
                    </p>
                  </div>
                ))}
              </div>

              {/* CANONICAL 10-DIMENSION COMPARISON MATRIX */}
              <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse min-w-[800px]">
                    <thead>
                      <tr className="bg-[var(--bg-surface)] border-b border-[var(--border-color)]">
                        <th className="sticky left-0 bg-[var(--bg-surface)] z-20 p-3.5 text-xs font-black text-[var(--text-main)] uppercase tracking-wider w-[220px] border-r border-[var(--border-color)]">
                          Research Dimension
                        </th>
                        {papers.map(p => (
                          <th key={p.paper_id} className="p-3.5 text-xs font-bold text-[var(--text-main)] min-w-[260px] border-r border-[var(--border-subtle)] last:border-r-0">
                            <div className="font-black text-[var(--text-main)] line-clamp-2">{p.title}</div>
                            <div className="text-[10px] text-[var(--text-muted)] font-mono mt-0.5 truncate">{p.authors}</div>
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--border-subtle)] text-xs">
                      {rows.map((row) => (
                        <tr key={row.dimension} className="hover:bg-[var(--bg-card-hover)] transition-colors">
                          <td className="sticky left-0 bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] z-10 p-3.5 font-bold text-[var(--text-main)] border-r border-[var(--border-color)] bg-clip-padding">
                            <div className="font-black text-[var(--text-main)]">{row.dimension}</div>
                          </td>
                          {papers.map(p => {
                            const cell = row.cells.find(c => c.paper_id === p.paper_id);
                            const status = cell?.status || 'NOT_REPORTED';
                            const isBacked = status === 'EVIDENCE_BACKED';
                            const isExtractionFailed = status === 'EXTRACTION_FAILED';

                            // Strict verification: Reject cell if paper_id does not match
                            if (cell && cell.paper_id !== p.paper_id) {
                              return (
                                <td key={p.paper_id} className="p-3.5 border-r border-slate-100 last:border-r-0 bg-rose-50/40">
                                  <span className="text-[11px] font-mono text-rose-600 font-bold">Evidence Attribution Mismatch</span>
                                </td>
                              );
                            }

                            return (
                              <td key={p.paper_id} className="p-3.5 border-r border-slate-100 last:border-r-0 align-top">
                                {isBacked && cell ? (
                                  <div className="space-y-2">
                                    <p className="text-xs text-slate-800 leading-relaxed font-normal">
                                      {cell.value}
                                    </p>
                                    <div className="flex items-center justify-between pt-1">
                                      <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 inline-flex items-center gap-1">
                                        <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Evidence-backed
                                      </span>
                                      <button
                                        onClick={() => setSelectedEvidenceCell({ cell, paperTitle: p.title })}
                                        className="text-[11px] font-bold text-slate-600 hover:text-emerald-700 underline"
                                      >
                                        [View Evidence]
                                      </button>
                                    </div>
                                  </div>
                                ) : isExtractionFailed ? (
                                  <div className="space-y-1">
                                    <span className="text-[11px] font-mono font-bold text-rose-700 bg-rose-50 px-2 py-1 rounded border border-rose-200 inline-block">
                                      EXTRACTION FAILED
                                    </span>
                                  </div>
                                ) : (
                                  <div>
                                    <span className="text-[11px] font-mono font-bold text-slate-400 bg-slate-100 px-2 py-1 rounded inline-block">
                                      NOT REPORTED
                                    </span>
                                  </div>
                                )}
                              </td>
                            );
                          })}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* COLLAPSIBLE CROSS-PAPER SYNTHESIS */}
              {comparisonData.summary && (
                <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
                  <button
                    onClick={() => setShowSynthesis(!showSynthesis)}
                    className="w-full flex items-center justify-between text-left font-black text-xs text-slate-700 uppercase tracking-wider"
                  >
                    <span>Cross-Paper Synthesis</span>
                    <span className="text-slate-400 flex items-center gap-1 text-[11px] font-bold">
                      {showSynthesis ? 'Hide Synthesis' : 'Show Synthesis'}
                      {showSynthesis ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                    </span>
                  </button>

                  {showSynthesis && (
                    <div className="space-y-4 pt-3 border-t border-slate-100 text-xs animate-in fade-in duration-150">
                      <div>
                        <h5 className="font-bold text-slate-900 mb-1">Key Similarities Across Papers</h5>
                        <ul className="list-disc list-inside space-y-1 text-slate-600 pl-1">
                          {comparisonData.summary.similarities.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h5 className="font-bold text-slate-900 mb-1">Architectural & Empirical Differences</h5>
                        <ul className="list-disc list-inside space-y-1 text-slate-600 pl-1">
                          {comparisonData.summary.differences.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </>
          )}

        </div>
      </div>

      {/* RIGHT-SIDE EVIDENCE DRAWER */}
      {selectedEvidenceCell && (
        <div 
          className="fixed inset-y-0 right-0 w-full sm:w-[480px] bg-[var(--bg-card)] border-l border-[var(--border-color)] shadow-2xl z-60 flex flex-col animate-in slide-in-from-right duration-200 text-[var(--text-main)]"
          role="dialog"
        >
          <div className="p-4 border-b border-[var(--border-color)] flex items-center justify-between bg-[var(--bg-surface)]">
            <div>
              <span className="text-[10px] font-black uppercase text-[var(--accent-primary)] bg-[var(--accent-soft)] px-2 py-0.5 rounded">
                EVIDENCE PROVENANCE
              </span>
              <h3 className="text-sm font-bold text-[var(--text-main)] mt-1">Supporting Paper Passage</h3>
            </div>
            <button
              onClick={() => setSelectedEvidenceCell(null)}
              className="p-1.5 text-[var(--text-muted)] hover:text-[var(--text-main)] rounded-lg hover:bg-[var(--bg-card-hover)]"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-5 space-y-4 text-xs">
            <div className="p-3 bg-[var(--bg-surface)] border border-[var(--border-color)] rounded-xl space-y-1.5">
              <div className="text-[11px] text-[var(--text-muted)] font-bold uppercase tracking-wider">Paper:</div>
              <div className="font-bold text-[var(--text-main)]">{selectedEvidenceCell.paperTitle}</div>
              <div className="text-[10px] font-mono text-[var(--text-muted)]">ID: {selectedEvidenceCell.cell.paper_id}</div>
            </div>

            <div className="p-3 bg-[var(--bg-surface)] border border-[var(--border-color)] rounded-xl space-y-1.5">
              <div className="text-[11px] text-[var(--text-muted)] font-bold uppercase tracking-wider">Dimension:</div>
              <div className="font-bold text-[var(--accent-primary)]">{selectedEvidenceCell.cell.dimension_name}</div>
            </div>

            <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
              <div className="p-2.5 bg-[var(--bg-surface)] border border-[var(--border-color)] rounded-lg">
                <span className="text-[var(--text-muted)] block text-[9px] uppercase font-sans font-bold">Page</span>
                <span className="font-bold text-[var(--text-main)]">{selectedEvidenceCell.cell.page_number || '1'}</span>
              </div>
              <div className="p-2.5 bg-[var(--bg-surface)] border border-[var(--border-color)] rounded-lg">
                <span className="text-[var(--text-muted)] block text-[9px] uppercase font-sans font-bold">Chunk ID</span>
                <span className="font-bold text-[var(--text-main)] truncate block">{selectedEvidenceCell.cell.chunk_id || 'chunk_001'}</span>
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="text-[11px] text-[var(--text-muted)] font-bold uppercase tracking-wider">Exact Supporting Passage:</div>
              <div className="p-3.5 bg-[var(--bg-surface)] border border-[var(--border-color)] rounded-xl font-mono text-[var(--text-sub)] leading-relaxed whitespace-pre-wrap text-[11px]">
                {selectedEvidenceCell.cell.evidence_text || selectedEvidenceCell.cell.value}
              </div>
            </div>
          </div>

          <div className="p-4 border-t border-[var(--border-color)] bg-[var(--bg-surface)] flex items-center justify-end gap-2">
            <button
              onClick={() => setSelectedEvidenceCell(null)}
              className="px-4 py-2 bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] text-[var(--text-main)] border border-[var(--border-color)] rounded-xl text-xs font-bold transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

    </div>
  );
};
