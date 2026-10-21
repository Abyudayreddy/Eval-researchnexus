import React, { useState, useEffect } from 'react';
import { UploadCloud, FileText, RefreshCw, Trash2, Search, BookOpen, MessageSquare, CheckSquare, Square, ShieldCheck } from 'lucide-react';

interface ResearchDoc {
  document_id: string;
  filename: string;
  original_filename?: string;
  file_size: number;
  page_count: number;
  processing_status: string;  // UPLOADED | VALIDATING | PROCESSING | EXTRACTED | CHUNKING | EMBEDDING | INDEXING | VERIFYING | READY | FAILED
  processing_error?: string;
  created_at?: string;
}

interface PersonalResearchCorpusProps {
  onSelectDocuments?: (docIds: string[]) => void;
  onAskAI?: (docId: string, filename: string) => void;
  onOpenReader?: (docId: string) => void;
}

export const PersonalResearchCorpus: React.FC<PersonalResearchCorpusProps> = ({
  onSelectDocuments,
  onAskAI,
  onOpenReader
}) => {
  const [documents, setDocuments] = useState<ResearchDoc[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedDocIds, setSelectedDocIds] = useState<string[]>([]);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // Fetch document list from backend
  const fetchDocuments = async () => {
    try {
      const res = await fetch('/api/documents');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch (e) {
      console.error('Failed to fetch documents', e);
    }
  };

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(fetchDocuments, 3000); // Polling for processing updates
    return () => clearInterval(interval);
  }, []);

  const handleFileUpload = async (file: File) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setUploadError('Only PDF research papers are supported.');
      return;
    }

    setIsUploading(true);
    setUploadError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Upload failed');
      }

      await fetchDocuments();
    } catch (err: any) {
      setUploadError(err.message || 'Failed to upload document.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleDelete = async (docId: string) => {
    try {
      const res = await fetch(`/api/documents/${docId}`, { method: 'DELETE' });
      if (res.ok) {
        setSelectedDocIds(prev => prev.filter(id => id !== docId));
        await fetchDocuments();
      }
    } catch (e) {
      console.error('Failed to delete document', e);
    }
  };

  const handleRetry = async (docId: string) => {
    try {
      await fetch(`/api/documents/${docId}/retry`, { method: 'POST' });
      await fetchDocuments();
    } catch (e) {
      console.error('Failed to retry document', e);
    }
  };

  const toggleSelect = (docId: string) => {
    setSelectedDocIds(prev => {
      const updated = prev.includes(docId) ? prev.filter(id => id !== docId) : [...prev, docId];
      if (onSelectDocuments) onSelectDocuments(updated);
      return updated;
    });
  };

  // Client-side metadata filtering
  const filteredDocuments = documents.filter(doc => {
    const matchesStatus = filterStatus === 'All' || doc.processing_status.toUpperCase() === filterStatus.toUpperCase();
    const matchesSearch = doc.filename.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const totalCount = documents.length;
  const readyCount = documents.filter(d => d.processing_status === 'READY').length;
  const processingCount = documents.filter(d => ['UPLOADED', 'VALIDATING', 'PROCESSING', 'EXTRACTED', 'CHUNKING', 'EMBEDDING', 'INDEXING', 'VERIFYING'].includes(d.processing_status)).length;
  const failedCount = documents.filter(d => d.processing_status === 'FAILED').length;

  return (
    <div className="w-full flex flex-col gap-6 p-6 bg-slate-50 min-h-screen">
      {/* Header Summary */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 uppercase tracking-wide">
              Personal Research Corpus
            </span>
            <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-full flex items-center gap-1">
              <ShieldCheck className="w-3 h-3 text-emerald-600" /> Dedicated Chroma Collection Isolation
            </span>
          </div>
          <h1 className="text-xl font-black text-slate-900">My Uploaded Research Library</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Isolated user corpus with deterministic BGE embeddings & cross-store index verification
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-600 bg-slate-100 px-3.5 py-2 rounded-xl">
            <span>Total: <strong>{totalCount}</strong></span>
            <span className="text-slate-300">|</span>
            <span className="text-emerald-700">Ready: <strong>{readyCount}</strong></span>
            <span className="text-slate-300">|</span>
            <span className="text-amber-700">Processing: <strong>{processingCount}</strong></span>
            <span className="text-slate-300">|</span>
            <span className="text-rose-700">Failed: <strong>{failedCount}</strong></span>
          </div>
        </div>
      </div>

      {/* Drag & Drop Upload Zone */}
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        className="bg-white border-2 border-dashed border-slate-300 hover:border-emerald-500 rounded-2xl p-8 text-center transition-all cursor-pointer shadow-sm flex flex-col items-center justify-center gap-3"
      >
        <div className="w-12 h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600">
          <UploadCloud className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-slate-800">Drop research papers (PDF) here to index</h3>
          <p className="text-xs text-slate-400 mt-0.5">Max size: 50MB. Text extraction, BGE embedding, & index verification executed automatically.</p>
        </div>

        <label className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl cursor-pointer transition shadow-sm">
          Browse PDF Files
          <input
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={(e) => e.target.files && e.target.files[0] && handleFileUpload(e.target.files[0])}
          />
        </label>

        {isUploading && <p className="text-xs text-emerald-600 font-bold animate-pulse">Uploading & validating file integrity...</p>}
        {uploadError && <p className="text-xs text-rose-600 font-bold">{uploadError}</p>}
      </div>

      {/* Filter & Metadata Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-1 bg-white border border-slate-200 p-1 rounded-xl shadow-sm">
          {['All', 'Ready', 'Processing', 'Failed'].map((status) => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={`px-3 py-1.5 text-xs font-bold rounded-lg transition ${
                filterStatus === status ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {status}
            </button>
          ))}
        </div>

        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search documents by filename or title..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 font-medium focus:outline-none focus:border-emerald-500 shadow-sm"
          />
        </div>
      </div>

      {/* Document Grid / Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredDocuments.map((doc) => {
          const isSelected = selectedDocIds.includes(doc.document_id);
          const isReady = doc.processing_status === 'READY';
          const isFailed = doc.processing_status === 'FAILED';

          return (
            <div
              key={doc.document_id}
              className={`bg-white border rounded-2xl p-5 shadow-sm space-y-3 transition flex flex-col justify-between ${
                isSelected ? 'border-emerald-500 ring-2 ring-emerald-500/20' : 'border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="space-y-2">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <button onClick={() => toggleSelect(doc.document_id)} className="text-slate-400 hover:text-emerald-600">
                      {isSelected ? <CheckSquare className="w-4 h-4 text-emerald-600" /> : <Square className="w-4 h-4" />}
                    </button>
                    <FileText className="w-4 h-4 text-slate-500 shrink-0" />
                    <h4 className="text-xs font-black text-slate-900 truncate max-w-[180px]" title={doc.filename}>
                      {doc.filename}
                    </h4>
                  </div>

                  <span className={`text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full ${
                    isReady ? 'bg-emerald-100 text-emerald-800' :
                    isFailed ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {doc.processing_status}
                  </span>
                </div>

                <div className="text-[11px] text-slate-500 space-y-1 font-medium bg-slate-50 p-2.5 rounded-xl border border-slate-150">
                  <p>Pages: <strong>{doc.page_count || 'Counting...'}</strong> | Size: <strong>{(doc.file_size / 1024).toFixed(1)} KB</strong></p>
                  {isFailed && <p className="text-rose-600 font-bold truncate">{doc.processing_error || 'Processing failed'}</p>}
                </div>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                <div className="flex items-center gap-1.5">
                  {isReady && onOpenReader && (
                    <button
                      onClick={() => onOpenReader(doc.document_id)}
                      className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-[11px] font-bold flex items-center gap-1"
                    >
                      <BookOpen className="w-3 h-3" /> Open
                    </button>
                  )}

                  {isReady && onAskAI && (
                    <button
                      onClick={() => onAskAI(doc.document_id, doc.filename)}
                      className="px-2.5 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg text-[11px] font-bold flex items-center gap-1 border border-emerald-200"
                    >
                      <MessageSquare className="w-3 h-3" /> Ask AI
                    </button>
                  )}

                  {isFailed && (
                    <button
                      onClick={() => handleRetry(doc.document_id)}
                      className="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-700 rounded-lg text-[11px] font-bold flex items-center gap-1 border border-amber-200"
                    >
                      <RefreshCw className="w-3 h-3" /> Retry
                    </button>
                  )}
                </div>

                <button
                  onClick={() => handleDelete(doc.document_id)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg transition"
                  title="Delete Document"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
