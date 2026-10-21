
import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { api } from '../utils/api';

export default function PaperReaderPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const paperId = queryParams.get('paper_id');
  const searchId = queryParams.get('search_id');

  const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || "http://localhost:8000/api";
  const pdfUrl = `${API_BASE_URL}/papers/${paperId}/pdf`;

  useEffect(() => {
    if (paperId) {
      api.analytics.trackPaperView(paperId);
    }
  }, [paperId]);

  if (!paperId) {
    return <div className="p-8 text-center text-rose-500">Missing paper ID.</div>;
  }

  return (
    <div className="absolute inset-0 flex flex-col font-sans overflow-hidden bg-slate-900">
      <header className="px-4 py-3 flex items-center justify-between bg-slate-800 text-white shrink-0 shadow-md">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => {
              if (searchId) {
                navigate(`/hybrid-search?search_id=${searchId}`);
              } else {
                navigate(-1);
              }
            }}
            className="p-2 text-slate-300 hover:text-white bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-sm font-bold tracking-wide">ResearchNexus Reader</h1>
        </div>
        <div className="text-xs font-medium text-slate-400">
          Local PDF: {paperId}
        </div>
      </header>

      <div className="flex-1 w-full bg-slate-950 relative">
        <iframe
          src={pdfUrl}
          className="w-full h-full border-0"
          title="PDF Reader"
        >
          <div className="absolute inset-0 flex items-center justify-center text-slate-400 p-8 text-center">
            <p>Your browser does not support inline PDFs. <a href={pdfUrl} target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">Download it here</a>.</p>
          </div>
        </iframe>
      </div>
    </div>
  );
}
