import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  Search, X, Filter, Bookmark, MessageSquare,
  BrainCircuit, History, Activity, Library
} from 'lucide-react';
import { cn } from '../utils/cn';
import { api } from '../utils/api';
import { toast } from 'sonner';
import { useOverlayStore } from '../store/overlayStore';
import { SideDrawer } from '../components/ui/Overlays';
import { 
  normalizeSearchResponse, 
  normalizeStatusResponse, 
  normalizeCanonicalSearchResult, 
  mergeCanonicalResults,
  createInitialExperimentStatus,
  CanonicalSearchResult, 
  ExperimentStatus
} from '../utils/apiAdapter';
import LocalRetrievalPanel from '../components/research/LocalRetrievalPanel';
import OnlineRetrievalPanel from '../components/research/OnlineRetrievalPanel';
import { ResearchExecutionPipeline } from '../components/research/ResearchExecutionPipeline';
import PaperCard from '../components/research/PaperCard';
import WhyThisPaperDrawer from '../components/research/WhyThisPaperDrawer';
import { ResearchAtmosphere } from '../components/ResearchAtmosphere';
import { getDynamicResearchTopics, DynamicResearchTopic } from '../services/researchTopicService';

type SearchLifecycleStatus = 
  | 'IDLE' 
  | 'SEARCHING' 
  | 'LOCAL_RUNNING' 
  | 'ONLINE_RUNNING' 
  | 'MERGING' 
  | 'RERANKING' 
  | 'EVIDENCE_ASSEMBLY' 
  | 'COMPLETED' 
  | 'FAILED';

export default function HybridSearchPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { openOverlay, closeOverlay } = useOverlayStore();

  const queryParams = new URLSearchParams(location.search);
  const urlSearchId = queryParams.get('search_id');

  const [query, setQuery] = useState('');
  const [searchLifecycle, setSearchLifecycle] = useState<SearchLifecycleStatus>('IDLE');
  const [canonicalResult, setCanonicalResult] = useState<CanonicalSearchResult | null>(null);
  const [activeSearchId, setActiveSearchId] = useState<string | null>(urlSearchId);
  const [experimentStatus, setExperimentStatus] = useState<ExperimentStatus | null>(null);
  const [results, setResults] = useState<any[]>([]);

  const [searchMode, setSearchMode] = useState<'hybrid' | 'semantic' | 'keyword'>('hybrid');
  const [publicationYear, setPublicationYear] = useState<string | null>(null);
  const [sourceFilter, setSourceFilter] = useState<string | null>(null);
  const [evidenceFilter, setEvidenceFilter] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<string>('relevance');

  const [selectedPaper, setSelectedPaper] = useState<any>(null);
  const [bookmarkedPapers, setBookmarkedPapers] = useState<string[]>([]);
  const [selectedPapersForAi, setSelectedPapersForAi] = useState<Set<string>>(new Set());
  const [dynamicStarters, setDynamicStarters] = useState<DynamicResearchTopic[]>([]);

  useEffect(() => {
    getDynamicResearchTopics().then(res => {
      setDynamicStarters(res.popularStarters);
    }).catch(err => {
      console.warn('Failed to load dynamic starters', err);
    });
  }, []);

  const activeExecutionIdRef = useRef<string | null>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  useEffect(() => {
    if (urlSearchId) {
      setActiveSearchId(urlSearchId);
      if (!canonicalResult || canonicalResult.searchId !== urlSearchId) {
        setSearchLifecycle('SEARCHING');
        startPolling(urlSearchId, null, query);
      }
    } else {
      const stateQuery = location.state?.query || queryParams.get('q');
      if (stateQuery && stateQuery.trim() && searchLifecycle === 'IDLE') {
        setQuery(stateQuery);
        handleSearchSubmit(undefined, stateQuery);
      }
    }
  }, [urlSearchId, location.state]);

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    try {
      const data = await api.bookmarks.getAll();
      if (Array.isArray(data)) {
        setBookmarkedPapers(data.map((b: any) => b.paper_id));
      }
    } catch (e) {
      console.error("Failed to load bookmarks", e);
    }
  };

  useEffect(() => {
    if (['IDLE', 'COMPLETED', 'FAILED'].includes(searchLifecycle)) {
      loadHistory();
    }
  }, [searchLifecycle]);

  const loadHistory = async () => {
    try {
      const data = await api.history.getAll();
      if (Array.isArray(data)) {
        setHistory(data);
      }
    } catch (e) {
      console.error("Failed to load history", e);
    }
  };

  const startPolling = (sid: string, execId: string | null, currentQuery: string) => {
    if (pollingRef.current) clearInterval(pollingRef.current);
    
    const poll = async () => {
      try {
        const rawStatus = await api.papers.getStatus(sid);
        const st = normalizeStatusResponse(rawStatus);

        // Stale execution guard: reject responses if searchId or executionId no longer match
        if (st.search_id !== sid) return;
        if (execId && st.execution_id && st.execution_id !== execId) return;

        const incomingCanon = normalizeCanonicalSearchResult(st, currentQuery || query);

        setExperimentStatus(st);
        
        // Merge incoming payload into canonical result to avoid wiping valid accumulated results
        setCanonicalResult(prev => {
          const merged = mergeCanonicalResults(prev, incomingCanon);
          setResults(merged.uniquePapers);
          setSearchLifecycle(merged.status);
          return merged;
        });

        // Strict terminal check: stop polling strictly when terminal === true
        if (incomingCanon.terminal) {
          if (pollingRef.current) clearInterval(pollingRef.current);
        }
      } catch (e) {
        console.error("Polling failed", e);
        if (activeSearchId === sid) {
          setSearchLifecycle('FAILED');
        }
      }
    };
    
    poll();
    pollingRef.current = setInterval(poll, 1000);
  };

  const handleSearchSubmit = async (e?: React.FormEvent, directQuery?: string) => {
    if (e) e.preventDefault();
    const q = directQuery || query;
    if (!q.trim()) return;
    if (searchLifecycle === 'SEARCHING') return;

    if (directQuery) setQuery(directQuery);

    const initialSearchId = `temp_${Date.now()}`;
    const initialExecId = `exec_init_${Date.now()}`;
    const initialStatus = createInitialExperimentStatus(initialSearchId, initialExecId, q);
    const initialCanon = normalizeCanonicalSearchResult(initialStatus, q);

    setSearchLifecycle('SEARCHING');
    setExperimentStatus(initialStatus);
    setCanonicalResult(initialCanon);
    setResults([]);
    setSelectedPapersForAi(new Set());
    
    if (pollingRef.current) clearInterval(pollingRef.current);

    // Track search in analytics
    api.analytics.trackSearch({
      query: q,
      search_mode: searchMode
    });

    try {
      const response = await api.papers.search({
        query: q,
        search_mode: searchMode,
        retrieval_mode: "local_online",
        publication_year: publicationYear,
        sort_by: sortBy
      });

      const normalized = normalizeSearchResponse(response);
      if (normalized.search_id) {
        activeExecutionIdRef.current = normalized.execution_id;
        setActiveSearchId(normalized.search_id);

        navigate(`?search_id=${normalized.search_id}`, { replace: true });
        startPolling(normalized.search_id, normalized.execution_id, q);
      }
    } catch (err) {
      console.error(err);
      toast.error('Failed to start search');
      setSearchLifecycle('FAILED');
    }
  };

  const handleExplain = (e: React.MouseEvent, paperId?: string) => {
    if (e) e.stopPropagation();
    if (paperId) {
      const paper = results.find(r => r.id === paperId || r.paper_id === paperId);
      if (paper) {
        setSelectedPaper(paper);
        openOverlay('side_drawer', { id: 'why_this_paper' });
      }
    } else if (activeSearchId) {
      navigate(`/xai?search_id=${activeSearchId}`);
    }
  };

  const handleAskAiSingle = (e: React.MouseEvent, paperId: string) => {
    e.stopPropagation();
    navigate(`/assistant?search_id=${activeSearchId}&paper_id=${paperId}`, { 
      state: { context_mode: 'SINGLE_PAPER' }
    });
  };

  const handleLiteratureBuilder = () => {
    const paperIds = Array.from(selectedPapersForAi);
    navigate(`/literature-review`, {
      state: { search_id: activeSearchId, paper_ids: paperIds }
    });
  };

  const handleBookmark = async (e: React.MouseEvent, paper: any) => {
    e.stopPropagation();
    const id = paper.id || paper.paper_id;
    if (bookmarkedPapers.includes(id)) {
      try {
        await api.bookmarks.remove(id);
        setBookmarkedPapers(prev => prev.filter(p => p !== id));
        toast.success("Removed from library");
      } catch (err) {
        toast.error("Failed to remove bookmark");
      }
    } else {
      try {
        await api.bookmarks.add({
          id: id,
          title: paper.title || "Untitled Paper",
          authors: Array.isArray(paper.authors) ? paper.authors.join(", ") : (paper.authors || "Unknown Authors"),
          abstract: paper.abstract || paper.evidence_text || "",
          url: paper.url || paper.paper_url || "",
          published: paper.published || paper.publication_date || paper.publication_year || null
        });
        setBookmarkedPapers(prev => [...prev, id]);
        toast.success("Added to library");
      } catch (err) {
        toast.error("Failed to save paper to library");
      }
    }
  };

  const isFinished = searchLifecycle === 'COMPLETED' || searchLifecycle === 'FAILED';
  const isRunning = ['SEARCHING', 'LOCAL_RUNNING', 'ONLINE_RUNNING', 'MERGING', 'RERANKING', 'EVIDENCE_ASSEMBLY'].includes(searchLifecycle);
  const showPanels = isRunning || isFinished;
  
  const localCount = canonicalResult ? canonicalResult.localCount : (experimentStatus?.local?.result_count || 0);
  const onlineCount = canonicalResult ? canonicalResult.onlineCount : (experimentStatus?.online?.result_count || 0);
  const uniqueResultCount = canonicalResult ? canonicalResult.uniqueCount : (experimentStatus?.combined_result_count || results.length);
  const evidenceBlocksCount = canonicalResult ? canonicalResult.evidenceCount : results.filter(r => r.evidence_text || r.abstract).length;

  const displayedResults = React.useMemo(() => {
    let filtered = [...results];
    
    // Apply filters
    if (publicationYear) {
      filtered = filtered.filter(r => String(r.publication_year) === publicationYear);
    }
    if (sourceFilter) {
      filtered = filtered.filter(r => {
        const source = (r.retrieval_source || '').toUpperCase();
        return source === sourceFilter;
      });
    }
    if (evidenceFilter) {
      filtered = filtered.filter(r => {
        const hasEvidence = !!r.evidence_text;
        return evidenceFilter === 'with' ? hasEvidence : !hasEvidence;
      });
    }
    
    // Apply sorting
    if (sortBy === 'newest') {
      filtered.sort((a, b) => {
        const dateA = a.publication_date ? new Date(a.publication_date).getTime() : 0;
        const dateB = b.publication_date ? new Date(b.publication_date).getTime() : 0;
        if (dateA !== dateB) return dateB - dateA;
        const yearA = a.publication_year ? parseInt(a.publication_year) : 0;
        const yearB = b.publication_year ? parseInt(b.publication_year) : 0;
        return yearB - yearA;
      });
    } else if (sortBy === 'oldest') {
      filtered.sort((a, b) => {
        const dateA = a.publication_date ? new Date(a.publication_date).getTime() : Infinity;
        const dateB = b.publication_date ? new Date(b.publication_date).getTime() : Infinity;
        if (dateA !== dateB) return dateA - dateB;
        const yearA = a.publication_year ? parseInt(a.publication_year) : Infinity;
        const yearB = b.publication_year ? parseInt(b.publication_year) : Infinity;
        return yearA - yearB;
      });
    }
    
    return filtered;
  }, [results, sortBy, publicationYear, sourceFilter, evidenceFilter]);

  return (
    <div className="absolute inset-0 flex flex-col font-sans overflow-hidden bg-[var(--bg-surface)] transition-colors duration-200">
      <ResearchAtmosphere activeSection={searchLifecycle === 'IDLE' ? 'hero' : 'discover'} />
      
      {/* RESEARCH HEADER */}
      <header className="relative px-6 py-4 flex items-center justify-between z-10 shrink-0">
        <div>
          <h1 className="text-xl font-black text-[var(--text-main)] flex items-center gap-2">
            Research Explorer
          </h1>
          <p className="text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-widest mt-0.5">
            Hybrid Research Intelligence
          </p>
        </div>
        <div className="flex gap-2">
          <button className="px-3 py-1.5 text-xs font-bold text-[var(--text-sub)] bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-color)] hover:border-[var(--accent-primary)] rounded-lg flex items-center gap-1.5 shadow-xs transition-all">
            <Bookmark className="w-3.5 h-3.5 text-[var(--accent-primary)]" /> Saved
          </button>
          <button onClick={() => openOverlay('side_drawer', { id: 'history_drawer' })} className="px-3 py-1.5 text-xs font-bold text-[var(--text-sub)] bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-color)] hover:border-[var(--info)] rounded-lg flex items-center gap-1.5 shadow-xs transition-all">
            <History className="w-3.5 h-3.5 text-[var(--info)]" /> History
          </button>
        </div>
      </header>

      {/* SCROLLABLE MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto relative z-10">
        <div className="max-w-5xl mx-auto px-4 md:px-8 pt-4 pb-16">
          
          {/* RESEARCH HERO (Only when IDLE) */}
          {searchLifecycle === 'IDLE' && (
            <div className="text-center mt-[10vh] mb-10 animate-in fade-in slide-in-from-bottom-4 duration-1000">
              <h2 className="text-4xl md:text-5xl font-black text-[var(--text-main)] mb-4 tracking-tight drop-shadow-xs">
                Explore the Research
              </h2>
              <p className="text-[var(--text-sub)] font-medium max-w-2xl mx-auto text-lg leading-relaxed">
                Ask a research question, discover relevant papers, inspect supporting evidence, and trace how ResearchNexus found each result.
              </p>
            </div>
          )}

          {/* SEARCH WORKSPACE */}
          <div className={cn("transition-all duration-700 ease-in-out", searchLifecycle !== 'IDLE' && "mb-8")}>
            <form onSubmit={(e) => handleSearchSubmit(e)} className="relative group">
              <div className="absolute left-6 top-1/2 -translate-y-1/2 text-[var(--text-muted)] group-focus-within:text-[var(--accent-primary)] transition-colors">
                <Search className="w-6 h-6" />
              </div>
              <input 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="What research question are you exploring?"
                className="w-full pl-16 pr-32 py-5 bg-[var(--bg-input)] border border-[var(--border-color)] rounded-2xl text-lg font-medium text-[var(--text-main)] placeholder-[var(--text-muted)] focus:outline-none focus:border-[var(--accent-primary)] focus:ring-4 focus:ring-[var(--accent-soft)] transition-all shadow-sm group-hover:border-[var(--border-color)]"
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
                {query && (
                  <button type="button" onClick={() => setQuery('')} className="p-2 text-[var(--text-muted)] hover:text-[var(--text-main)] transition-colors bg-[var(--bg-card)] rounded-full">
                    <X className="w-5 h-5" />
                  </button>
                )}
                <button 
                  type="submit" 
                  disabled={searchLifecycle === 'SEARCHING'}
                  className="px-6 py-2.5 bg-[var(--accent-primary)] hover:opacity-90 text-[var(--text-inverse)] rounded-xl text-sm font-black transition-all shadow-md active:scale-95 disabled:opacity-50 cursor-pointer"
                >
                  {searchLifecycle === 'SEARCHING' ? '...' : 'Search →'}
                </button>
              </div>
              <div className="absolute right-4 -bottom-6 text-[10px] font-bold text-[var(--text-muted)] opacity-0 md:opacity-100">
                Ctrl / Cmd + K
              </div>
            </form>

            {/* CONTROLS */}
            <div className="flex flex-wrap items-center justify-between gap-4 mt-6 px-2">
              <div className="flex items-center gap-1.5 p-1 bg-[var(--bg-card)] rounded-lg border border-[var(--border-color)]">
                {[
                  { id: 'hybrid', label: 'Hybrid' },
                  { id: 'semantic', label: 'Semantic' },
                  { id: 'keyword', label: 'Keyword' },
                ].map(mode => (
                  <button
                    key={mode.id}
                    type="button"
                    onClick={() => setSearchMode(mode.id as any)}
                    className={cn("px-4 py-1.5 rounded-md text-[11px] font-bold uppercase tracking-wider transition-all cursor-pointer",
                      searchMode === mode.id ? "bg-[var(--bg-card-hover)] text-[var(--text-main)] shadow-xs border border-[var(--border-subtle)]" : "text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card-hover)]"
                    )}
                  >
                    {mode.label}
                  </button>
                ))}
              </div>
              
              <div className="flex items-center gap-2">
                {publicationYear && (
                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-[var(--accent-soft)] text-[var(--accent-primary)] rounded-lg text-xs font-bold border border-[var(--border-color)]">
                    <span>{publicationYear}</span>
                    <button onClick={() => setPublicationYear(null)} className="hover:opacity-80"><X className="w-3 h-3" /></button>
                  </div>
                )}
                <button type="button" onClick={() => openOverlay('side_drawer', { id: 'search_filters' })} className="px-4 py-1.5 text-xs font-bold text-[var(--text-sub)] bg-[var(--bg-input)] border border-[var(--border-color)] hover:border-[var(--accent-primary)] rounded-lg flex items-center gap-1.5 shadow-xs transition-all hover:-translate-y-0.5 cursor-pointer">
                  <Filter className="w-3.5 h-3.5" /> Filters { [publicationYear, sourceFilter, evidenceFilter].filter(Boolean).length > 0 ? `(${[publicationYear, sourceFilter, evidenceFilter].filter(Boolean).length})` : ''}
                </button>
              </div>
            </div>
          </div>

          {/* PRE-SEARCH EMPTY STATE */}
          {searchLifecycle === 'IDLE' && (
            <div className="mt-16 animate-in fade-in duration-1000 delay-300">
              <div className="flex items-center justify-center gap-2 mb-6">
                <h3 className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-widest text-center">
                  Popular Research Starters
                </h3>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[var(--accent-soft)] text-[var(--accent-primary)] font-bold border border-[var(--border-subtle)]">
                  Daily Grounded
                </span>
              </div>
              <div className="flex flex-wrap justify-center gap-3 md:gap-4 max-w-4xl mx-auto">
                {(dynamicStarters.length > 0 ? dynamicStarters : [
                  { id: 'rag', title: "Retrieval-Augmented Generation", query: "retrieval augmented generation", domain: "Artificial Intelligence", sourceBadge: "Online + Offline" as const },
                  { id: 'xai', title: "Explainable AI in Medicine", query: "explainable AI in healthcare and medicine", domain: "Healthcare", sourceBadge: "Online" as const },
                  { id: 'trace', title: "Trace Evidence Retrieval", query: "trace evidence retrieval systems", domain: "Artificial Intelligence", sourceBadge: "Online + Offline" as const },
                  { id: 'climate', title: "Climate Change Modeling", query: "climate change machine learning models", domain: "Environmental Science", sourceBadge: "Online + Offline" as const },
                ]).map((starter, i) => (
                  <div 
                    key={starter.id || i}
                    onClick={() => handleSearchSubmit(undefined, starter.query)}
                    className="flex items-center gap-3 px-5 py-3 bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-[var(--accent-primary)] hover:bg-[var(--bg-card-hover)] rounded-full cursor-pointer hover:-translate-y-1 transition-all duration-300 group shadow-xs hover:shadow-md"
                  >
                    <div className="text-[var(--accent-primary)] group-hover:scale-110 transition-transform">
                      <BrainCircuit className="w-4 h-4" />
                    </div>
                    <div className="flex flex-col text-left">
                      <span className="font-bold text-[var(--text-sub)] text-sm group-hover:text-[var(--text-main)] transition-colors leading-tight">
                        {starter.title}
                      </span>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-[10px] font-medium text-[var(--text-muted)]">
                          {starter.domain}
                        </span>
                        <span className="text-[9px] font-mono text-[var(--accent-primary)] bg-[var(--accent-soft)] px-1.5 py-0.2 rounded">
                          {starter.sourceBadge}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* LIVE RESEARCH INTELLIGENCE AREA */}
          {showPanels && experimentStatus && (
            <div className="mb-8 space-y-6 animate-in slide-in-from-top-4 fade-in duration-500">
              {/* TRANSPARENT RESEARCH EXECUTION PIPELINE */}
              <ResearchExecutionPipeline status={experimentStatus} query={query} />

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 relative">
                {/* LOCAL RESEARCH */}
                <div className="relative">
                  <LocalRetrievalPanel status={experimentStatus.local} />
                </div>
                
                {/* ONLINE RESEARCH */}
                <div className="relative">
                  <OnlineRetrievalPanel status={experimentStatus.online} />
                </div>

                {/* CENTRAL MERGE INDICATOR (Desktop Only) */}
                {isRunning && (
                  <div className="hidden lg:flex absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 items-center justify-center z-10 w-24">
                     <div className="relative w-full h-full flex flex-col items-center">
                        <div className="w-[1px] h-8 bg-slate-300 absolute -top-10 left-1/2 transform -rotate-[60deg] origin-bottom animate-pulse"></div>
                        <div className="w-[1px] h-8 bg-slate-300 absolute -top-10 right-1/2 transform rotate-[60deg] origin-bottom animate-pulse"></div>
                        <div className="w-10 h-10 rounded-full bg-white border border-slate-200 shadow-sm flex items-center justify-center text-[10px] font-bold text-slate-500 uppercase z-20">
                           <Activity className="w-4 h-4 text-emerald-500 animate-pulse" />
                        </div>
                     </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* RESEARCH CONTEXT BAR */}
          {isFinished && (
            <div className="bg-slate-900 text-white rounded-2xl p-5 mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl shadow-slate-900/5 border border-slate-800 animate-in fade-in duration-700">
              <div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1.5 flex items-center gap-2">
                  Research Context <span className="w-1 h-1 rounded-full bg-emerald-500 animate-pulse"></span>
                </div>
                <div className="text-lg font-black text-white line-clamp-1 mb-2">"{query}"</div>
                
                {/* RETRIEVAL SUMMARY */}
                <div className="flex flex-wrap items-center gap-3 mt-2">
                  <div className="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700">
                    <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider">Local</span>
                    <span className="text-emerald-400 text-xs font-bold">{localCount}</span>
                  </div>
                  <div className="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700">
                    <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider">Online</span>
                    <span className="text-blue-400 text-xs font-bold">{onlineCount}</span>
                  </div>
                  <div className="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700">
                    <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider">Unique</span>
                    <span className="text-violet-400 text-xs font-bold">{uniqueResultCount}</span>
                  </div>
                  <div className="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700">
                    <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider">Evidence Blocks</span>
                    <span className="text-amber-400 text-xs font-bold">{evidenceBlocksCount}</span>
                  </div>
                </div>
              </div>
              
              <div className="flex flex-wrap items-center gap-2 shrink-0">
                {(canonicalResult?.executionState === 'COMPLETED_WITH_RESULTS' || (canonicalResult?.executionState === 'DEGRADED' && canonicalResult?.uniquePapers.length > 0)) && (
                  <button 
                    onClick={() => navigate(`/xai?search_id=${activeSearchId}`)} 
                    className="px-4 py-2 text-xs font-bold bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl flex items-center gap-2 transition-all shadow-md active:scale-95"
                  >
                    <BrainCircuit className="w-4 h-4" /> Analyze with XAI →
                  </button>
                )}
                <button onClick={(e) => handleExplain(e)} className="px-4 py-2 text-xs font-bold bg-white text-slate-900 hover:bg-slate-100 rounded-xl flex items-center gap-2 transition-colors">
                  <BrainCircuit className="w-4 h-4 text-emerald-600" /> Explain Search
                </button>
                <button onClick={() => navigate(`/assistant?search_id=${activeSearchId}`)} className="px-4 py-2 text-xs font-bold bg-purple-600 text-white hover:bg-purple-700 rounded-xl flex items-center gap-2 transition-colors">
                  <MessageSquare className="w-4 h-4" /> Ask AI
                </button>
                {selectedPapersForAi.size > 0 && (
                  <button onClick={handleLiteratureBuilder} className="px-4 py-2 text-xs font-bold bg-amber-500 text-white hover:bg-amber-600 rounded-xl flex items-center gap-2 transition-colors animate-in pop-in">
                    <Library className="w-4 h-4" /> Build Review ({selectedPapersForAi.size})
                  </button>
                )}
              </div>
            </div>
          )}

          {/* RESULTS AREA */}
          {isFinished && (
            <div className="space-y-6 animate-in slide-in-from-bottom-8 fade-in duration-700 delay-100">
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-2">
                <div>
                  <h2 className="text-xl font-black text-slate-900">Research Results</h2>
                  <p className="text-sm font-medium text-slate-500">Most relevant evidence from Local + Online research</p>
                </div>
                <div className="flex items-center gap-2">
                  <select 
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    className="text-xs font-bold text-slate-600 bg-white border border-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-emerald-400">
                    <option value="relevance">Most Relevant</option>
                    <option value="newest">Newest</option>
                    <option value="oldest">Oldest</option>
                  </select>
                </div>
              </div>

              {/* TECHNICAL FAILURE STATE */}
              {canonicalResult?.executionState === 'FAILED' && (
                <div className="bg-rose-50 border border-rose-200 text-rose-800 rounded-2xl p-6 text-center space-y-4 my-6">
                  <div className="w-10 h-10 rounded-full bg-rose-100 flex items-center justify-center mx-auto text-rose-600">
                    <Activity className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-black">Research search failed</h3>
                  <p className="text-sm font-medium text-rose-600">A technical error occurred while retrieving research evidence from backend services.</p>
                  <button onClick={() => handleSearchSubmit(undefined, query)} className="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-sm rounded-xl transition-colors shadow-sm">
                    Retry Search
                  </button>
                </div>
              )}

              {/* PROVIDER WARNINGS / DEGRADED SEARCH STATE */}
              {canonicalResult?.warnings && canonicalResult.warnings.length > 0 && (
                <div className="bg-amber-50/90 text-amber-900 text-xs font-medium p-4 rounded-xl border border-amber-200 space-y-2">
                  <div className="flex items-center gap-2 font-bold text-amber-800 text-xs">
                    <Activity className="w-4 h-4 text-amber-600" />
                    <span>Search completed with provider warnings</span>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 font-mono text-[11px] text-amber-800">
                    {canonicalResult.warnings.map((w, idx) => (
                      <li key={idx}>[{w.provider}] {w.message}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* DEGRADED + ZERO PAPERS RETRIEVED */}
              {canonicalResult?.executionState === 'DEGRADED' && canonicalResult?.uniquePapers.length === 0 && (
                <div className="text-center py-12 border border-dashed border-amber-300 rounded-2xl bg-amber-50/40">
                  <h3 className="text-base font-black text-amber-900 mb-2">Search completed with provider issues</h3>
                  <p className="text-xs text-amber-700 font-medium max-w-md mx-auto">No papers were returned because one or more external research sources failed or were rate-limited. Please retry or adjust your search query.</p>
                </div>
              )}

              {/* STRICT AUTHORITATIVE EMPTY RESULTS (ONLY WHEN COMPLETED_NO_RESULTS) */}
              {canonicalResult?.executionState === 'COMPLETED_NO_RESULTS' && (
                <div className="text-center py-16 border border-dashed border-slate-300 rounded-2xl bg-white/50 backdrop-blur-sm">
                  <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-4">
                    <Search className="w-6 h-6 text-slate-400" />
                  </div>
                  <h3 className="text-lg font-black text-slate-800 mb-2">No papers were returned for this search. Adjust your query or filters (like publication year) to see more results.</h3>
                  <p className="text-slate-500 font-medium mb-6">We couldn't locate strong evidence matching your query across local and online repositories.</p>
                  <div className="flex justify-center gap-4">
                    <button onClick={() => openOverlay('side_drawer', { id: 'search_filters' })} className="text-sm text-emerald-600 hover:text-emerald-700 font-bold bg-emerald-50 hover:bg-emerald-100 px-4 py-2 rounded-lg transition-colors">Adjust Query / Filters</button>
                    <button onClick={() => { setPublicationYear(null); setSourceFilter(null); setEvidenceFilter(null); }} className="text-sm text-slate-600 hover:text-slate-700 font-bold bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-lg transition-colors">Clear Filters</button>
                  </div>
                </div>
              )}

              {/* FILTER ZERO RESULTS (WHEN RESULTS EXIST BUT FILTERS EXCLUDE ALL) */}
              {canonicalResult?.terminal && (canonicalResult?.uniquePapers.length || 0) > 0 && displayedResults.length === 0 && (
                <div className="text-center py-12 border border-dashed border-slate-200 rounded-2xl bg-white/50">
                  <p className="text-sm font-bold text-slate-600 mb-4">No papers match the currently applied filters.</p>
                  <button onClick={() => { setPublicationYear(null); setSourceFilter(null); setEvidenceFilter(null); }} className="text-xs font-bold text-emerald-600 bg-emerald-50 hover:bg-emerald-100 px-4 py-2 rounded-lg transition-colors">
                    Clear Filters
                  </button>
                </div>
              )}

              {/* LIST */}
              {displayedResults.length > 0 && (
                <div className="space-y-5">
                  {displayedResults.map((result) => (
                    <PaperCard 
                      key={result.id || result.paper_id}
                      paper={result}
                      searchId={activeSearchId || ''}
                      isSelectedForAi={selectedPapersForAi.has(result.id || result.paper_id)}
                      isBookmarked={bookmarkedPapers.includes(result.id || result.paper_id)}
                      onToggleSelection={(e, id) => {
                        e.stopPropagation();
                        const next = new Set(selectedPapersForAi);
                        if (next.has(id)) next.delete(id); else next.add(id);
                        setSelectedPapersForAi(next);
                      }}
                      onBookmark={handleBookmark}
                      onNote={() => navigate(`/notebook?create=true&paperId=${result.id || result.paper_id}`)}
                      onProject={() => toast.info("Project integration available in Projects view.")}
                      onAskAi={handleAskAiSingle}
                      onExplain={handleExplain}
                    />
                  ))}
                </div>
              )}
            </div>
          )}

        </div>
      </div>

      {/* OVERLAYS */}
      <SideDrawer id="search_filters" title="Search Filters" position="left">
        <div className="space-y-6">
          <div className="space-y-3">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest block border-b border-slate-100 pb-2">Publication Year</span>
            <div className="flex flex-col gap-2.5">
              {[
                { id: '2026', label: '2026' },
                { id: '2025', label: '2025' },
                { id: '2024', label: '2024' }
              ].map(year => (
                <label key={year.id} className="flex items-center gap-3 text-sm font-medium text-slate-700 cursor-pointer p-2 rounded-lg hover:bg-slate-50 transition-colors">
                  <input 
                    type="radio" 
                    name="pubYear"
                    checked={publicationYear === year.id}
                    onChange={() => { setPublicationYear(year.id); closeOverlay(); }}
                    className="w-4 h-4 text-emerald-600 border-slate-300 focus:ring-emerald-500" 
                  /> 
                  {year.label}
                </label>
              ))}
            </div>
          </div>
          <div className="space-y-3">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest block border-b border-slate-100 pb-2">Source</span>
            <div className="flex flex-col gap-2.5">
              {['LOCAL', 'ONLINE', 'MIXED'].map(src => (
                <label key={src} className="flex items-center gap-3 text-sm font-medium text-slate-700 cursor-pointer p-2 rounded-lg hover:bg-slate-50 transition-colors">
                  <input 
                    type="radio" 
                    name="sourceFilter"
                    checked={sourceFilter === src}
                    onChange={() => { setSourceFilter(src); closeOverlay(); }}
                    className="w-4 h-4 text-emerald-600 border-slate-300 focus:ring-emerald-500" 
                  /> 
                  {src}
                </label>
              ))}
            </div>
          </div>
          <div className="space-y-3">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest block border-b border-slate-100 pb-2">Evidence</span>
            <div className="flex flex-col gap-2.5">
              {[
                { id: 'with', label: 'With Evidence' },
                { id: 'without', label: 'Without Evidence' }
              ].map(ev => (
                <label key={ev.id} className="flex items-center gap-3 text-sm font-medium text-slate-700 cursor-pointer p-2 rounded-lg hover:bg-slate-50 transition-colors">
                  <input 
                    type="radio" 
                    name="evidenceFilter"
                    checked={evidenceFilter === ev.id}
                    onChange={() => { setEvidenceFilter(ev.id); closeOverlay(); }}
                    className="w-4 h-4 text-emerald-600 border-slate-300 focus:ring-emerald-500" 
                  /> 
                  {ev.label}
                </label>
              ))}
            </div>
          </div>
          <button onClick={() => { setPublicationYear(null); setSourceFilter(null); setEvidenceFilter(null); closeOverlay(); }} className="w-full py-3 bg-slate-100 hover:bg-rose-50 text-slate-600 hover:text-rose-600 rounded-xl text-sm font-bold transition-colors">
            Clear Filters
          </button>
        </div>
      </SideDrawer>

              <SideDrawer id="history_drawer" title="Recent Research" position="right">
        <div className="space-y-4">
          {history.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-8 font-medium">No recent research found.</p>
          ) : (
            history.map((item) => (
              <div 
                key={item.history_id} 
                className="p-4 bg-white border border-slate-200 rounded-xl hover:border-blue-300 hover:shadow-md cursor-pointer transition-all group relative"
                onClick={() => {
                  setQuery(item.query);
                  setActiveSearchId(item.search_id);
                  navigate(`?search_id=${item.search_id}`, { replace: true });
                  setSearchLifecycle('SEARCHING');
                  startPolling(item.search_id, null, item.query);
                  closeOverlay();
                }}
              >
                <h4 className="font-bold text-slate-900 text-sm pr-6 leading-tight">{item.query}</h4>
                <div className="flex items-center gap-2 mt-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50 px-2 py-0.5 rounded">{new Date(item.created_at).toLocaleDateString()}</span>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">{item.local_result_count} Local</span>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded">{item.online_result_count} Online</span>
                </div>
                
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    if(confirm("Delete this history record?")) {
                      api.history.delete(item.history_id).then(() => loadHistory());
                    }
                  }}
                  className="absolute right-3 top-3 p-1.5 text-slate-400 hover:text-rose-500 rounded-lg hover:bg-rose-50 opacity-0 group-hover:opacity-100 transition-opacity"
                  title="Delete History"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))
          )}
        </div>
      </SideDrawer>

      <WhyThisPaperDrawer paper={selectedPaper} />
    </div>
  );
}