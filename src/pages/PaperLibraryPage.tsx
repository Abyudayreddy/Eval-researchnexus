import { useState, useEffect } from 'react';
import { 
  Library, Search, Bookmark, Maximize, 
  Download, Upload, Sparkles, BookOpen, CheckSquare, Square
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useOverlayStore } from '../store/overlayStore';
import { useToastStore } from '../store/toastStore';
import { CenteredSheet } from '../components/ui/Overlays';
import { api } from '../utils/api';
import { cn } from '../utils/cn';

export default function PaperLibraryPage() {
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPaper, setSelectedPaper] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedForReview, setSelectedForReview] = useState<Set<string>>(new Set());

  const { openOverlay } = useOverlayStore();
  const { addToast } = useToastStore();
  const navigate = useNavigate();

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    setIsLoading(true);
    try {
      const data = await api.bookmarks.getAll();
      setBookmarks(data || []);
    } catch (err) {
      console.error("Failed to load library", err);
      addToast('Failed to load paper library', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const removeBookmark = async (e: React.MouseEvent, paperId: string) => {
    e.stopPropagation();
    try {
      await api.bookmarks.remove(paperId);
      setBookmarks(prev => prev.filter(b => (b.paper_id !== paperId && b.paper?.id !== paperId)));
      setSelectedForReview(prev => {
        const next = new Set(prev);
        next.delete(paperId);
        return next;
      });
      addToast('Paper removed from library', 'info');
    } catch (err) {
      console.error("Failed to remove bookmark", err);
      addToast('Failed to remove bookmark', 'error');
    }
  };

  const openPaperPreview = (paper: any) => {
    setSelectedPaper(paper);
    openOverlay('centered_sheet', { id: 'library_paper_preview' });
  };

  const toggleSelectForReview = (e: React.MouseEvent, paperId: string) => {
    e.stopPropagation();
    setSelectedForReview(prev => {
      const next = new Set(prev);
      if (next.has(paperId)) {
        next.delete(paperId);
      } else {
        next.add(paperId);
      }
      return next;
    });
  };

  const handleStartReview = (preselectedPapers?: any[]) => {
    const papersToSend = preselectedPapers || bookmarks
      .filter(b => selectedForReview.has(b.paper?.id || b.paper_id))
      .map(b => b.paper);

    if (papersToSend.length === 0) {
      navigate('/literature-review');
      return;
    }

    navigate('/literature-review', {
      state: {
        selected_papers: papersToSend
      }
    });
  };

  const filteredBookmarks = bookmarks.filter(b => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    const title = b.paper?.title?.toLowerCase() || '';
    const authors = b.paper?.authors?.toLowerCase() || '';
    const abstract = b.paper?.abstract?.toLowerCase() || '';
    return title.includes(q) || authors.includes(q) || abstract.includes(q);
  });

  return (
    <div className="h-full flex flex-col bg-main font-sans overflow-hidden relative rounded-xl border border-theme text-main">
      {/* TOP HEADER */}
      <header className="px-6 py-4 border-b border-theme flex flex-col md:flex-row md:items-center justify-between gap-4 shrink-0 bg-surface z-10">
        <div>
          <h1 className="text-xl font-black text-main flex items-center gap-2">
            <Library className="w-5 h-5 text-emerald-500" /> Paper Library
          </h1>
          <p className="text-xs font-medium text-muted mt-0.5">
            Manage your personal collection of saved research papers ({bookmarks.length} saved).
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {selectedForReview.size > 0 ? (
            <button
              onClick={() => handleStartReview()}
              className="px-4 py-2 text-xs font-black bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg flex items-center gap-2 shadow-sm transition-all"
            >
              <Sparkles className="w-3.5 h-3.5" />
              Start Literature Review ({selectedForReview.size}) →
            </button>
          ) : bookmarks.length >= 2 ? (
            <button
              onClick={() => navigate('/literature-review')}
              className="px-3.5 py-2 text-xs font-bold bg-surface hover:bg-card-hover border border-theme text-main rounded-lg flex items-center gap-1.5 transition-colors shadow-xs"
            >
              <Sparkles className="w-3.5 h-3.5 text-emerald-500" />
              Open Literature Review
            </button>
          ) : null}

          <div className="flex items-center gap-2">
            <button className="px-3 py-1.5 text-xs font-bold text-sub bg-surface hover:bg-card-hover border border-theme rounded-lg flex items-center gap-1.5 transition-colors">
              <Upload className="w-3.5 h-3.5" /> Import
            </button>
            <button className="px-3 py-1.5 text-xs font-bold text-sub bg-surface hover:bg-card-hover border border-theme rounded-lg flex items-center gap-1.5 transition-colors">
              <Download className="w-3.5 h-3.5" /> Export
            </button>
          </div>
        </div>
      </header>

      {/* SEARCH & ACTION BAR */}
      <div className="px-6 py-3 border-b border-theme bg-surface shrink-0 z-10">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center gap-4 justify-between">
          <div className="relative w-full max-w-sm">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
            <input 
              type="text" 
              placeholder="Search library papers, authors, abstracts..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-card border border-theme rounded-lg pl-9 pr-3 py-2 text-xs text-main placeholder-muted focus:outline-none focus:border-emerald-500 transition-colors shadow-xs" 
            />
          </div>

          <div className="flex items-center gap-2 text-xs font-bold text-muted">
            <span>{filteredBookmarks.length} paper{filteredBookmarks.length !== 1 ? 's' : ''} in library</span>
            {selectedForReview.size > 0 && (
              <span className="text-emerald-500 font-mono">• {selectedForReview.size} selected for review</span>
            )}
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto bg-main p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          {isLoading ? (
            <div className="flex justify-center p-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
            </div>
          ) : bookmarks.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in max-w-md mx-auto">
              <BookOpen className="w-16 h-16 text-muted mb-4 opacity-40" />
              <h2 className="text-lg font-bold text-main mb-2">No saved papers yet</h2>
              <p className="text-xs text-muted mb-6 leading-relaxed">
                Save papers from Research Explorer or AI Assistant to build your personal library and launch systematic literature reviews.
              </p>
              <button
                onClick={() => navigate('/hybrid-search')}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition-colors shadow-xs"
              >
                Go to Research Explorer →
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4 animate-in fade-in">
              {filteredBookmarks.map((bookmark) => {
                const paper = bookmark.paper || bookmark;
                const paperId = paper.id || bookmark.paper_id;
                const isSelected = selectedForReview.has(paperId);

                return (
                  <div 
                    key={bookmark.id || paperId}
                    onClick={() => openPaperPreview(paper)}
                    className={cn(
                      "rounded-xl p-5 border transition-all cursor-pointer flex flex-col sm:flex-row justify-between items-start gap-4",
                      isSelected 
                        ? "bg-card border-emerald-500 shadow-sm ring-1 ring-emerald-500/20" 
                        : "bg-card border-theme hover:border-theme-hover shadow-xs"
                    )}
                  >
                    <div className="flex items-start gap-3 flex-1 min-w-0">
                      <button
                        onClick={(e) => toggleSelectForReview(e, paperId)}
                        className="mt-1 text-muted hover:text-emerald-500 transition-colors shrink-0"
                        title={isSelected ? "Deselect for literature review" : "Select for literature review"}
                      >
                        {isSelected ? (
                          <CheckSquare className="w-4 h-4 text-emerald-500" />
                        ) : (
                          <Square className="w-4 h-4 text-muted" />
                        )}
                      </button>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                          <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            Saved • Available for Review
                          </span>
                          {paper.domain && (
                            <span className="text-[10px] font-bold text-muted bg-surface px-2 py-0.5 rounded border border-theme">
                              {paper.domain}
                            </span>
                          )}
                        </div>

                        <h3 className="text-base font-bold text-main leading-snug mb-1.5 hover:text-emerald-500 transition-colors">
                          {paper.title}
                        </h3>

                        <div className="flex items-center gap-2 text-[11px] font-bold text-muted mb-2 flex-wrap">
                          <span className="text-emerald-500 truncate max-w-[260px]">
                            {paper.authors || "Authors available in record"}
                          </span>
                          <span>•</span>
                          <span>{paper.published ? paper.published.substring(0, 4) : 'Recent'}</span>
                        </div>

                        <p className="text-xs text-sub line-clamp-2 leading-relaxed">
                          {paper.abstract || "Detailed abstract recorded and available for literature review extraction."}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex sm:flex-col items-center gap-2 shrink-0 self-end sm:self-center">
                      <button 
                        onClick={(e) => {
                          e.stopPropagation();
                          handleStartReview([paper]);
                        }}
                        className="px-3 py-1.5 bg-surface hover:bg-emerald-500/10 border border-theme hover:border-emerald-500/30 text-xs font-bold text-main hover:text-emerald-400 rounded-lg transition-colors flex items-center gap-1.5"
                        title="Review this paper"
                      >
                        <Sparkles className="w-3.5 h-3.5 text-emerald-500" />
                        <span className="hidden sm:inline">Review</span>
                      </button>

                      <button 
                        onClick={(e) => removeBookmark(e, paperId)}
                        className="p-2 text-muted hover:text-rose-500 hover:bg-rose-500/10 rounded-lg transition-colors border border-transparent hover:border-rose-500/20"
                        title="Remove Bookmark"
                      >
                        <Bookmark className="w-4 h-4 fill-emerald-500 text-emerald-500" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* OVERLAY: PAPER PREVIEW */}
      <CenteredSheet id="library_paper_preview" title={selectedPaper?.title || "Paper Details"}>
        {selectedPaper && (
          <div className="space-y-5 text-main">
            <div className="flex flex-col gap-2 text-xs font-medium">
              <div className="flex items-start gap-4">
                <span className="w-20 text-muted uppercase tracking-widest text-[10px] shrink-0 font-bold mt-0.5">Authors</span>
                <span className="text-emerald-500 font-bold">{selectedPaper.authors || "Authors unavailable"}</span>
              </div>
              <div className="flex items-start gap-4">
                <span className="w-20 text-muted uppercase tracking-widest text-[10px] shrink-0 font-bold mt-0.5">Published</span>
                <span className="text-sub">{selectedPaper.published ? selectedPaper.published.substring(0, 10) : "Recent"}</span>
              </div>
              {selectedPaper.domain && (
                <div className="flex items-start gap-4">
                  <span className="w-20 text-muted uppercase tracking-widest text-[10px] shrink-0 font-bold mt-0.5">Domain</span>
                  <span className="text-sub">{selectedPaper.domain}</span>
                </div>
              )}
            </div>

            <div className="bg-surface p-4 rounded-xl border border-theme">
              <h4 className="text-[11px] font-bold text-muted uppercase tracking-widest mb-2">Abstract</h4>
              <p className="text-xs text-sub leading-relaxed whitespace-pre-wrap">
                {selectedPaper.abstract || "No abstract available."}
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-3 border-t border-theme">
              {selectedPaper.url && (
                <a 
                  href={selectedPaper.url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="w-full py-2.5 bg-surface hover:bg-card-hover border border-theme text-main rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-2"
                >
                  <Maximize className="w-3.5 h-3.5" /> Open Source URL
                </a>
              )}
              <button 
                onClick={() => {
                  useOverlayStore.getState().closeOverlay();
                  handleStartReview([selectedPaper]);
                }}
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-2 shadow-xs"
              >
                <Sparkles className="w-3.5 h-3.5" /> Start Literature Review
              </button>
            </div>
          </div>
        )}
      </CenteredSheet>
    </div>
  );
}
