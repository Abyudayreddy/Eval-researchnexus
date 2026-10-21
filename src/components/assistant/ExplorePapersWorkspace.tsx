import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FileText, Upload, Sliders, CheckCircle2, RefreshCw, AlertCircle
} from 'lucide-react';
import { cn } from '../../utils/cn';
import { api } from '../../utils/api';

interface ExplorePapersWorkspaceProps {
  papers: any[];
  uploadedDocuments: any[];
  onUploadDocument: (doc: any) => void;
  onAskAboutPaper: (paper: any) => void;
  onComparePapers: (paperIds: string[]) => void;
  onPromoteToProve?: () => void;
  onPromoteToRefine?: () => void;
}

export function formatAuthorDisplay(raw: any): string {
  if (!raw) return 'Authors unavailable';
  if (Array.isArray(raw)) {
    const names = raw.map(a => typeof a === 'object' && a?.name ? a.name : String(a)).filter(Boolean);
    return names.length > 0 ? names.join(', ') : 'Authors unavailable';
  }
  if (typeof raw === 'string') {
    const s = raw.trim();
    if (!s || ['unknown', 'unknown authors', 'unavailable', 'none'].includes(s.toLowerCase())) {
      return 'Authors unavailable';
    }
    if (s.includes("'name':") || s.includes('"name":')) {
      const matches = Array.from(s.matchAll(/['"]name['"]\s*:\s*['"]([^'"]+)['"]/g), m => m[1]);
      if (matches.length > 0) {
        return matches.join(', ');
      }
    }
    return s;
  }
  return 'Authors unavailable';
}

export function formatTitleDisplay(rawTitle: any, fallbackId: string = ''): string {
  if (!rawTitle) return fallbackId || 'Untitled Paper';
  const s = String(rawTitle).trim();
  if (!s || ['unknown', 'unknown authors', 'authors unavailable', 'untitled'].includes(s.toLowerCase())) {
    return fallbackId || 'Untitled Paper';
  }
  if (s.includes("'name':") || s.includes('"name":')) {
    return fallbackId || 'Untitled Paper';
  }
  return s;
}

export const ExplorePapersWorkspace: React.FC<ExplorePapersWorkspaceProps> = ({
  papers,
  uploadedDocuments,
  onUploadDocument,
  onAskAboutPaper,
  onComparePapers,
}) => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'upload' | 'compare'>('compare');
  const [uploadingState, setUploadingState] = useState<{
    isUploading: boolean;
    stageIndex: number;
    fileName: string | null;
  }>({ isUploading: false, stageIndex: 0, fileName: null });

  const [selectedForCompare, setSelectedForCompare] = useState<string[]>([]);
  const [selectionError, setSelectionError] = useState<string | null>(null);

  const pipelineStages = [
    { name: 'Uploaded', detail: 'File payload validated' },
    { name: 'Validating PDF', detail: 'Verifying structure & non-corrupt header' },
    { name: 'Extracting Text', detail: 'PyMuPDF extraction & layout preservation' },
    { name: 'Cleaning Content', detail: 'Stripping headers, footers & noise' },
    { name: 'Detecting Sections', detail: 'Identifying Abstract, Intro, Methods, Results' },
    { name: 'Semantic Chunks', detail: 'Chunking 512 tokens with 10% overlap' },
    { name: 'Generating Embeddings', detail: 'BAAI/bge-base-en-v1.5 vectorization' },
    { name: 'Indexing Personal DB', detail: 'Creating ChromaDB vector collection' },
    { name: 'Verifying Coverage', detail: 'Checking retrieval recall & bounds' },
    { name: 'Ready for Retrieval', detail: 'Bound to active ResearchContext' },
  ];

  const [uploadError, setUploadError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadError(null);
    setUploadingState({ isUploading: true, stageIndex: 0, fileName: file.name });

    try {
      const uploadRes = await api.documents.upload(file);
      const docId = uploadRes.document_id;
      setUploadingState({ isUploading: true, stageIndex: 1, fileName: file.name });

      if (uploadRes.processing_status === 'READY') {
        setUploadingState({ isUploading: false, stageIndex: pipelineStages.length, fileName: file.name });
        onUploadDocument({
          id: docId,
          document_id: docId,
          name: file.name,
          filename: file.name,
          size: file.size,
          status: 'READY'
        });
        return;
      }

      const maxAttempts = 30;
      let attempt = 0;
      const statusMap: Record<string, number> = {
        'UPLOADED': 0,
        'VALIDATING': 1,
        'PROCESSING': 2,
        'EXTRACTED': 3,
        'CHUNKING': 5,
        'EMBEDDING': 6,
        'INDEXING': 7,
        'VERIFYING': 8,
        'READY': 9
      };

      const pollInterval = setInterval(async () => {
        attempt++;
        try {
          const statusRes = await api.documents.getStatus(docId);
          const currentStatus = statusRes.processing_status;
          const stageIdx = statusMap[currentStatus] ?? Math.min(attempt, 8);
          setUploadingState(prev => ({ ...prev, stageIndex: stageIdx }));

          if (currentStatus === 'READY') {
            clearInterval(pollInterval);
            setUploadingState({ isUploading: false, stageIndex: pipelineStages.length, fileName: file.name });
            onUploadDocument({
              id: docId,
              document_id: docId,
              name: file.name,
              filename: file.name,
              size: file.size,
              status: 'READY'
            });
          } else if (currentStatus === 'FAILED' || attempt >= maxAttempts) {
            clearInterval(pollInterval);
            setUploadingState({ isUploading: false, stageIndex: 0, fileName: null });
            setUploadError(statusRes.processing_error || 'Document processing timed out or failed.');
          }
        } catch (err: any) {
          clearInterval(pollInterval);
          setUploadingState({ isUploading: false, stageIndex: 0, fileName: null });
          setUploadError(err.message || 'Error tracking processing status');
        }
      }, 1000);

    } catch (err: any) {
      setUploadingState({ isUploading: false, stageIndex: 0, fileName: null });
      setUploadError(err.message || 'Failed to upload document');
    }
  };

  const toggleSelectPaper = (id: string) => {
    setSelectionError(null);
    setSelectedForCompare(prev => {
      if (prev.includes(id)) return prev.filter(x => x !== id);
      if (prev.length >= 5) {
        setSelectionError('You can compare a maximum of 5 papers simultaneously.');
        return prev;
      }
      return [...prev, id];
    });
  };

  const handleStartComparison = () => {
    if (selectedForCompare.length < 2) {
      setSelectionError('Select at least 2 papers to compare.');
      return;
    }
    if (selectedForCompare.length > 5) {
      setSelectionError('Select at most 5 papers to compare.');
      return;
    }
    setSelectionError(null);
    onComparePapers(selectedForCompare);
  };

  const handleStartLiteratureReview = () => {
    if (selectedForCompare.length < 2) {
      setSelectionError('Select at least 2 papers to create a literature review.');
      return;
    }
    setSelectionError(null);
    const chosen = allAvailablePapers.filter(p => selectedForCompare.includes(p.id));
    navigate('/literature-review', { state: { selected_papers: chosen } });
  };

  const allAvailablePapers = [
    ...uploadedDocuments.map(doc => ({
      id: doc.id || doc.name,
      paper_id: doc.id || doc.name,
      title: formatTitleDisplay(doc.name, 'Uploaded Document'),
      authors: 'User Uploaded Document',
      year: new Date().getFullYear().toString(),
      abstract: doc.summary || 'Uploaded research document indexed into personal collection.',
      isUploaded: true,
      venue: 'User Document'
    })),
    ...papers.map(p => ({
      ...p,
      id: p.id || p.paper_id,
      paper_id: p.id || p.paper_id,
      title: formatTitleDisplay(p.title, p.id || p.paper_id),
      authors: formatAuthorDisplay(p.authors),
      year: p.publicationYear || p.published || '2024'
    }))
  ];

  return (
    <div className="flex-1 overflow-y-auto bg-[var(--bg-main)] p-6 md:p-10 font-sans">
      <div className="max-w-5xl mx-auto space-y-6 animate-in fade-in duration-300">
        
        {/* HEADER */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-[var(--accent-soft)] text-[var(--accent-primary)] uppercase tracking-wider">
                EXPLORE PAPERS
              </span>
              <span className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-widest">
                Upload & Compare
              </span>
            </div>
            <h2 className="text-xl font-black text-[var(--text-main)]">Literature & PDF Analysis</h2>
            <p className="text-xs font-medium text-[var(--text-muted)] mt-1 max-w-xl">
              Process external PDF papers or select 2 to 5 papers to generate a strict, evidence-grounded multi-paper comparison matrix.
            </p>
          </div>

          <div className="flex items-center bg-[var(--bg-surface)] p-1 rounded-xl border border-[var(--border-color)] shrink-0">
            <button
              onClick={() => setActiveTab('compare')}
              className={cn(
                "px-4 py-1.5 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer",
                activeTab === 'compare' ? 'bg-[var(--bg-card)] text-[var(--text-main)] shadow-xs border border-[var(--border-subtle)]' : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
              )}
            >
              <Sliders className="w-3.5 h-3.5 text-[var(--accent-primary)]" /> Compare Papers ({allAvailablePapers.length})
            </button>
            <button
              onClick={() => setActiveTab('upload')}
              className={cn(
                "px-4 py-1.5 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer",
                activeTab === 'upload' ? 'bg-[var(--bg-card)] text-[var(--text-main)] shadow-xs border border-[var(--border-subtle)]' : 'text-[var(--text-muted)] hover:text-[var(--text-main)]'
              )}
            >
              <Upload className="w-3.5 h-3.5 text-[var(--info)]" /> Upload PDF
            </button>
          </div>
        </div>

        {/* TAB 1: COMPARE PAPERS WORKSPACE (FOCUSED SELECTION — NO PERMANENT MATRIX ON PAGE) */}
        {activeTab === 'compare' && (
          <div className="space-y-6">
            <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                <div>
                  <h3 className="text-sm font-black text-slate-900">Select 2 to 5 Papers to Compare</h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Selected: <span className="font-bold text-emerald-700">{selectedForCompare.length}</span> / 5
                  </p>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  <button
                    onClick={handleStartComparison}
                    disabled={selectedForCompare.length < 2}
                    className={cn(
                      "px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition-all",
                      selectedForCompare.length >= 2 
                        ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-600/20 shadow-md cursor-pointer' 
                        : 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
                    )}
                  >
                    <Sliders className="w-3.5 h-3.5" />
                    <span>Compare Selected Papers</span>
                  </button>
                  <button
                    onClick={handleStartLiteratureReview}
                    disabled={selectedForCompare.length < 2}
                    className={cn(
                      "px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition-all",
                      selectedForCompare.length >= 2 
                        ? 'bg-purple-600 hover:bg-purple-700 text-white shadow-purple-600/20 shadow-md cursor-pointer' 
                        : 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
                    )}
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>Create Literature Review</span>
                  </button>
                </div>
              </div>

              {/* INLINE VALIDATION WARNING */}
              {selectionError && (
                <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 font-bold flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
                  <span>{selectionError}</span>
                </div>
              )}

              {/* PAPER SELECTION CARDS LIST */}
              {allAvailablePapers.length === 0 ? (
                <div className="p-12 text-center border border-dashed border-slate-200 rounded-2xl bg-slate-50 text-slate-400 text-xs font-bold space-y-2">
                  <p>No research papers or uploaded PDFs available in active context.</p>
                  <button
                    onClick={() => setActiveTab('upload')}
                    className="px-3 py-1.5 bg-slate-900 text-white rounded-lg font-sans font-bold hover:bg-slate-800"
                  >
                    Upload a PDF
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {allAvailablePapers.map((p) => {
                    const isSelected = selectedForCompare.includes(p.id);
                    return (
                      <div
                        key={p.id}
                        onClick={() => toggleSelectPaper(p.id)}
                        className={cn(
                          "p-4 rounded-xl border cursor-pointer transition-all flex items-start gap-3 relative",
                          isSelected 
                            ? 'bg-emerald-50/70 border-emerald-400 ring-2 ring-emerald-400/20 shadow-xs' 
                            : 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-xs'
                        )}
                      >
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => {}}
                          className="mt-1 rounded text-emerald-600 focus:ring-emerald-500 cursor-pointer"
                        />
                        <div className="overflow-hidden flex-1 space-y-1">
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-[10px] font-mono text-slate-400">
                              {p.year || '2024'}
                            </span>
                            {p.isUploaded && (
                              <span className="text-[9px] font-bold uppercase bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded">
                                User Document
                              </span>
                            )}
                          </div>
                          <h4 className="text-xs font-bold text-slate-900 leading-snug line-clamp-2">
                            {p.title}
                          </h4>
                          <p className="text-[11px] text-slate-500 truncate">
                            {p.authors}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: UPLOAD PDF PIPELINE */}
        {activeTab === 'upload' && (
          <div className="space-y-6">
            <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm text-center border-dashed border-2 border-slate-300 hover:border-emerald-500 transition-colors relative">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              <div className="flex flex-col items-center justify-center space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-100">
                  <Upload className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Upload Research PDF</h3>
                  <p className="text-xs text-slate-500 mt-1">Drag and drop your paper here, or click to browse</p>
                </div>
                <div className="text-[10px] font-mono bg-slate-100 text-slate-500 px-3 py-1 rounded-md">
                  PyMuPDF • Page-aware Chunking • BAAI/bge-base-en-v1.5 • Chroma DB
                </div>
              </div>
            </div>

            {/* ERROR BANNER */}
            {uploadError && (
              <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 font-medium flex items-center justify-between">
                <span>{uploadError}</span>
                <button onClick={() => setUploadError(null)} className="font-bold underline text-rose-900 ml-4">Dismiss</button>
              </div>
            )}

            {/* PIPELINE STAGES PROGRESS */}
            {uploadingState.isUploading && (
              <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <span className="text-xs font-bold text-emerald-700 flex items-center gap-2">
                    <RefreshCw className="w-4 h-4 animate-spin text-emerald-600" />
                    Processing {uploadingState.fileName}
                  </span>
                  <span className="text-xs font-mono font-bold text-slate-500">
                    Stage {uploadingState.stageIndex + 1} of 10
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                  {pipelineStages.map((stg, idx) => {
                    const isDone = idx < uploadingState.stageIndex;
                    const isCurrent = idx === uploadingState.stageIndex;
                    return (
                      <div
                        key={stg.name}
                        className={cn(
                          "p-3 rounded-xl border text-xs flex items-center justify-between transition-all",
                          isDone ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' :
                          isCurrent ? 'bg-amber-50 border-amber-300 text-amber-900 shadow-sm animate-pulse' :
                          'bg-slate-50 border-slate-200 text-slate-400 opacity-60'
                        )}
                      >
                        <div className="flex items-center gap-2">
                          <span className="w-5 h-5 rounded-full font-mono text-[10px] font-bold flex items-center justify-center bg-white border border-current">
                            {idx + 1}
                          </span>
                          <div>
                            <div className="font-bold">{stg.name}</div>
                            <div className="text-[10px] opacity-75">{stg.detail}</div>
                          </div>
                        </div>
                        {isDone && <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* UPLOADED DOCUMENTS LIST */}
            {uploadedDocuments.length > 0 && (
              <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                  Indexed Personal Papers ({uploadedDocuments.length})
                </h3>
                <div className="space-y-3">
                  {uploadedDocuments.map((doc, idx) => (
                    <div key={idx} className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3">
                      <div className="flex items-start gap-3">
                        <FileText className="w-5 h-5 text-emerald-600 mt-0.5 shrink-0" />
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{doc.name || 'Uploaded Document'}</h4>
                          <span className="text-[11px] text-slate-500 font-mono">
                            Indexed • Chroma collection: researchnexus_uploaded_v1_bgebase • Document-only boundary active
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 self-end md:self-auto">
                        <button
                          onClick={() => onAskAboutPaper(doc)}
                          className="px-3 py-1.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-xs font-bold transition-colors"
                        >
                          Ask About This Paper
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
};
