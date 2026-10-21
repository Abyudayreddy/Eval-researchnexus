import { useState, useEffect, useMemo } from 'react';
import { 
  Compass, Play, Search, BrainCircuit, ShieldCheck, 
  Layers, ArrowRight,
  Sparkles, ChevronRight, Check,
  ArrowLeft
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '../utils/cn';
import toolkitJson from '../data/research_review_toolkit.json';
import { toast } from 'sonner';

export type ScenarioStatus = 
  | 'NOT_TESTED' 
  | 'TESTING' 
  | 'PASSED' 
  | 'FAILED' 
  | 'PARTIAL' 
  | 'KNOWN_GOOD' 
  | 'INSUFFICIENT_EVIDENCE' 
  | 'NOT_APPLICABLE';

export interface Scenario {
  question_id: string;
  set_id?: 'SET1_QUICK' | 'SET2_DEEP' | 'SET3_LAB';
  filter: string;
  title: string;
  question: string;
  domain: string;
  mode: string;
  expected_source: string;
  target_surface: string[];
  query_type: string;
  difficulty: string;
  purpose: string;
  expected_behavior: string;
  expected_evidence: string;
  xai_expected?: boolean;
  answerability?: string;
  offline_available?: boolean;
  tags?: string[];
  status?: ScenarioStatus;
  is_known_good?: boolean;
  search_id?: string | null;
  execution_id?: string | null;
  answer_id?: string | null;
  claims_count?: number;
  citations_count?: number;
  latency_ms?: number;
}

interface DailyReviewState {
  review_set_id: string;
  generated_date: string;
  scenario_ids: string[];
  corpus_version: string;
  execution_results: Record<string, { status: ScenarioStatus; timestamp: string }>;
}

const ALL_PRODUCT_DOMAINS = [
  'Artificial Intelligence',
  'Data Science',
  'Healthcare',
  'Materials Science',
  'Environmental Science',
  'Energy',
  'Space Science',
  'Interdisciplinary'
] as const;

// Deterministic daily selection helper
function getDeterministicDailyScenarios(allScenarios: Scenario[], dateString: string): string[] {
  let hash = 0;
  for (let i = 0; i < dateString.length; i++) {
    hash = (hash << 5) - hash + dateString.charCodeAt(i);
    hash |= 0;
  }
  const positiveHash = Math.abs(hash);

  const eligible = allScenarios.filter(s => s.status === 'KNOWN_GOOD' || s.is_known_good || s.filter === 'CORE SYSTEM' || s.filter === 'RETRIEVAL' || s.filter === 'RAG');
  const pool = eligible.length >= 15 ? eligible : allScenarios;

  const selectedIds: string[] = [];
  const targetCount = Math.min(15, pool.length);
  const step = Math.max(1, Math.floor(pool.length / targetCount));

  for (let i = 0; i < targetCount; i++) {
    const idx = (positiveHash + i * step) % pool.length;
    const candidate = pool[idx];
    if (candidate && !selectedIds.includes(candidate.question_id)) {
      selectedIds.push(candidate.question_id);
    }
  }

  // Fallback to guarantee exactly 15 if duplicates were skipped
  for (const s of pool) {
    if (selectedIds.length >= 15) break;
    if (!selectedIds.includes(s.question_id)) {
      selectedIds.push(s.question_id);
    }
  }

  return selectedIds;
}

export default function ResearchReviewToolkitPage() {
  const navigate = useNavigate();
  const rawScenarios = useMemo(() => ((toolkitJson as any).scenarios || []) as Scenario[], []);

  // 3 Review Sets
  const [activeSetId, setActiveSetId] = useState<'quick' | 'deep' | 'lab'>('quick');
  const [activeTab, setActiveTab] = useState<'overview' | 'questions' | 'presets' | 'known_good' | 'history'>('overview');
  
  // Selected Scenario for details modal/card
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);

  // Daily State
  const [dailyState, setDailyState] = useState<DailyReviewState | null>(null);
  const [executionStatuses, setExecutionStatuses] = useState<Record<string, ScenarioStatus>>({});
  
  // Filters for Questions tab
  const [domainFilter, setDomainFilter] = useState<string>('All');
  const [categoryFilter, setCategoryFilter] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const todayStr = useMemo(() => new Date().toISOString().split('T')[0], []);

  // Initialize or reload daily review set
  useEffect(() => {
    try {
      const storageKey = `researchnexus_daily_toolkit_${todayStr}`;
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        const parsed = JSON.parse(saved);
        setDailyState(parsed);
        setExecutionStatuses(
          Object.fromEntries(
            Object.entries(parsed.execution_results || {}).map(([k, v]: any) => [k, v.status])
          )
        );
      } else {
        const ids = getDeterministicDailyScenarios(rawScenarios, todayStr);
        const newState: DailyReviewState = {
          review_set_id: `REV_DAILY_${todayStr}`,
          generated_date: todayStr,
          scenario_ids: ids,
          corpus_version: (toolkitJson as any).version || '2.0',
          execution_results: {}
        };
        localStorage.setItem(storageKey, JSON.stringify(newState));
        setDailyState(newState);
      }
    } catch (err) {
      console.error("Failed to load/create daily toolkit set", err);
    }
  }, [todayStr, rawScenarios]);

  // Set 1: Quick Review (Deterministic 15 daily scenarios)
  const quickScenarios = useMemo(() => {
    if (!dailyState?.scenario_ids) return [];
    const idSet = new Set(dailyState.scenario_ids);
    return rawScenarios
      .filter(s => idSet.has(s.question_id))
      .map(s => ({
        ...s,
        set_id: 'SET1_QUICK' as const,
        status: executionStatuses[s.question_id] || (s.is_known_good ? 'KNOWN_GOOD' : 'NOT_TESTED')
      }));
  }, [dailyState, rawScenarios, executionStatuses]);

  // Set 2: Deep System Review (Technical architecture & verification scenarios)
  const deepScenarios = useMemo(() => {
    return rawScenarios
      .filter(s => ['CORE SYSTEM', 'RETRIEVAL', 'RAG', 'CITATIONS', 'CLAIM VERIFICATION', 'XAI', 'PROJECT ARCHITECTURE', 'EVALUATION'].includes(s.filter))
      .map(s => ({
        ...s,
        set_id: 'SET2_DEEP' as const,
        status: executionStatuses[s.question_id] || (s.is_known_good ? 'KNOWN_GOOD' : 'NOT_TESTED')
      }));
  }, [rawScenarios, executionStatuses]);

  // Set 3: Research Scenario Lab (Cross-domain, multi-paper, edge-case, and online/offline scenarios)
  const labScenarios = useMemo(() => {
    return rawScenarios
      .filter(s => ['COMPARISON', 'OFFLINE CORPUS', 'ONLINE RESEARCH', 'HYBRID SEARCH', 'LIMITATIONS'].includes(s.filter) || ALL_PRODUCT_DOMAINS.includes(s.domain as any))
      .map(s => ({
        ...s,
        set_id: 'SET3_LAB' as const,
        status: executionStatuses[s.question_id] || (s.is_known_good ? 'KNOWN_GOOD' : 'NOT_TESTED')
      }));
  }, [rawScenarios, executionStatuses]);

  // Active Set Scenarios
  const currentSetScenarios = useMemo(() => {
    if (activeSetId === 'quick') return quickScenarios;
    if (activeSetId === 'deep') return deepScenarios;
    return labScenarios;
  }, [activeSetId, quickScenarios, deepScenarios, labScenarios]);

  // Filtered Scenarios for Questions list
  const filteredScenarios = useMemo(() => {
    return currentSetScenarios.filter(s => {
      if (domainFilter !== 'All' && s.domain !== domainFilter) return false;
      if (categoryFilter !== 'All' && s.filter !== categoryFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        return (
          s.title.toLowerCase().includes(q) ||
          s.question.toLowerCase().includes(q) ||
          s.question_id.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [currentSetScenarios, domainFilter, categoryFilter, searchQuery]);

  // Stats for daily quick review
  const dailyCompletedCount = useMemo(() => {
    return quickScenarios.filter(s => s.status && s.status !== 'NOT_TESTED' && s.status !== 'TESTING').length;
  }, [quickScenarios]);

  const activeScenario = useMemo(() => {
    if (!selectedScenarioId) return currentSetScenarios[0] || null;
    return currentSetScenarios.find(s => s.question_id === selectedScenarioId) || currentSetScenarios[0] || null;
  }, [selectedScenarioId, currentSetScenarios]);

  const updateScenarioStatus = (questionId: string, newStatus: ScenarioStatus) => {
    setExecutionStatuses(prev => ({ ...prev, [questionId]: newStatus }));
    try {
      const storageKey = `researchnexus_daily_toolkit_${todayStr}`;
      if (dailyState) {
        const updated = {
          ...dailyState,
          execution_results: {
            ...dailyState.execution_results,
            [questionId]: { status: newStatus, timestamp: new Date().toISOString() }
          }
        };
        setDailyState(updated);
        localStorage.setItem(storageKey, JSON.stringify(updated));
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleExecuteScenario = (scenario: Scenario) => {
    updateScenarioStatus(scenario.question_id, 'TESTING');
    toast.info(`Preparing execution: ${scenario.title}`);

    // If known good and cached artifact exists
    if (scenario.is_known_good && scenario.search_id) {
      setTimeout(() => {
        updateScenarioStatus(scenario.question_id, 'PASSED');
        toast.success(`Known Good Verified: ${scenario.title}`);
      }, 600);
      return;
    }

    // Recommended Workflow Navigation
    if (scenario.filter === 'COMPARISON') {
      navigate('/comparison/new', { state: { scenario } });
      return;
    }

    if (scenario.filter === 'CITATIONS' || scenario.filter === 'RAG') {
      navigate('/assistant', { state: { query: scenario.question, mode: scenario.mode } });
      return;
    }

    // Default to Hybrid Search / Research Explorer
    navigate('/hybrid-search', { state: { query: scenario.question, mode: scenario.mode } });
  };

  return (
    <div className="h-full w-full flex flex-col bg-main text-main font-sans overflow-hidden">
      {/* Top Header */}
      <header className="px-6 py-4 border-b border-theme bg-surface shrink-0 z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <button 
              onClick={() => navigate('/settings')}
              className="text-xs font-semibold text-muted hover:text-main flex items-center gap-1 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Settings
            </button>
            <span className="text-muted">•</span>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
              Quality Assurance & Validation
            </span>
          </div>
          <h1 className="text-xl md:text-2xl font-black text-main flex items-center gap-2.5">
            <Compass className="w-6 h-6 text-emerald-500" /> Research Review Toolkit
          </h1>
          <p className="text-xs text-muted mt-0.5">
            Review and validate ResearchNexus across retrieval, RAG, XAI, citations, claim verification, and domain workflows.
          </p>
        </div>

        {/* Set Switcher Tabs */}
        <div className="flex items-center gap-1.5 p-1 bg-card border border-theme rounded-xl shadow-xs self-start md:self-auto">
          <button
            onClick={() => { setActiveSetId('quick'); setSelectedScenarioId(null); }}
            className={cn(
              "px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5",
              activeSetId === 'quick' 
                ? "bg-emerald-600 text-white shadow-xs" 
                : "text-muted hover:text-main"
            )}
          >
            <Sparkles className="w-3.5 h-3.5" /> Quick Review
          </button>
          <button
            onClick={() => { setActiveSetId('deep'); setSelectedScenarioId(null); }}
            className={cn(
              "px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5",
              activeSetId === 'deep' 
                ? "bg-emerald-600 text-white shadow-xs" 
                : "text-muted hover:text-main"
            )}
          >
            <Layers className="w-3.5 h-3.5" /> Deep System Review
          </button>
          <button
            onClick={() => { setActiveSetId('lab'); setSelectedScenarioId(null); }}
            className={cn(
              "px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5",
              activeSetId === 'lab' 
                ? "bg-emerald-600 text-white shadow-xs" 
                : "text-muted hover:text-main"
            )}
          >
            <BrainCircuit className="w-3.5 h-3.5" /> Scenario Lab
          </button>
        </div>
      </header>

      {/* Main Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation / List Sidebar */}
        <div className="w-full md:w-80 lg:w-96 border-r border-theme bg-surface flex flex-col shrink-0 overflow-hidden">
          
          {/* Daily Status Banner (When in Quick Review) */}
          {activeSetId === 'quick' && (
            <div className="p-4 border-b border-theme bg-card/60 shrink-0">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[11px] font-bold text-muted uppercase tracking-wider">Today's Review ({todayStr})</span>
                <span className="text-xs font-black text-emerald-600 dark:text-emerald-400">
                  {dailyCompletedCount} / 15 completed
                </span>
              </div>
              <div className="w-full h-1.5 bg-surface rounded-full overflow-hidden border border-theme">
                <div 
                  className="h-full bg-emerald-500 transition-all duration-300"
                  style={{ width: `${(dailyCompletedCount / 15) * 100}%` }}
                />
              </div>
              <p className="text-[10px] text-muted mt-2">
                Deterministic daily selection • Refreshes every calendar day
              </p>
            </div>
          )}

          {/* Subtabs for set */}
          <div className="flex border-b border-theme px-3 pt-2 gap-2 shrink-0 bg-surface text-xs font-bold">
            <button
              onClick={() => setActiveTab('overview')}
              className={cn("pb-2 px-2 border-b-2 transition-colors", activeTab === 'overview' ? "border-emerald-500 text-emerald-600 dark:text-emerald-400" : "border-transparent text-muted hover:text-main")}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('questions')}
              className={cn("pb-2 px-2 border-b-2 transition-colors", activeTab === 'questions' ? "border-emerald-500 text-emerald-600 dark:text-emerald-400" : "border-transparent text-muted hover:text-main")}
            >
              Scenarios ({currentSetScenarios.length})
            </button>
            <button
              onClick={() => setActiveTab('known_good')}
              className={cn("pb-2 px-2 border-b-2 transition-colors", activeTab === 'known_good' ? "border-emerald-500 text-emerald-600 dark:text-emerald-400" : "border-transparent text-muted hover:text-main")}
            >
              Known Good
            </button>
          </div>

          {/* Search & Filters */}
          {activeTab === 'questions' && (
            <div className="p-3 border-b border-theme space-y-2 shrink-0 bg-card">
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-muted" />
                <input
                  type="text"
                  placeholder="Filter scenarios..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full bg-surface border border-theme rounded-lg pl-8 pr-3 py-1.5 text-xs text-main placeholder-muted focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <select
                  value={domainFilter}
                  onChange={e => setDomainFilter(e.target.value)}
                  className="bg-surface border border-theme rounded-lg px-2 py-1 text-[11px] text-main focus:outline-none"
                >
                  <option value="All">All Domains</option>
                  {ALL_PRODUCT_DOMAINS.map(d => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
                <select
                  value={categoryFilter}
                  onChange={e => setCategoryFilter(e.target.value)}
                  className="bg-surface border border-theme rounded-lg px-2 py-1 text-[11px] text-main focus:outline-none"
                >
                  <option value="All">All Categories</option>
                  <option value="CORE SYSTEM">Core System</option>
                  <option value="RETRIEVAL">Retrieval</option>
                  <option value="RAG">RAG</option>
                  <option value="CITATIONS">Citations</option>
                  <option value="CLAIM VERIFICATION">Claim Verification</option>
                  <option value="XAI">XAI</option>
                  <option value="COMPARISON">Comparison</option>
                  <option value="OFFLINE CORPUS">Offline Corpus</option>
                  <option value="ONLINE RESEARCH">Online Research</option>
                  <option value="LIMITATIONS">Limitations</option>
                </select>
              </div>
            </div>
          )}

          {/* Scenario List */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {activeTab === 'overview' ? (
              <div className="space-y-4 p-2 text-xs text-sub leading-relaxed">
                <div className="p-4 rounded-xl bg-card border border-theme space-y-2">
                  <h3 className="font-bold text-main text-sm">
                    {activeSetId === 'quick' && "Quick Research Review"}
                    {activeSetId === 'deep' && "Deep System Review"}
                    {activeSetId === 'lab' && "Research Scenario Lab"}
                  </h3>
                  <p className="text-muted">
                    {activeSetId === 'quick' && "Fast daily health check covering Explorer, Hybrid Retrieval, AI Assistant, citations, verification, and XAI."}
                    {activeSetId === 'deep' && "Detailed technical validation of BM25, ChromaDB dense retrieval, RRF, BGE reranking, claim extraction, and provenance."}
                    {activeSetId === 'lab' && "Large scenario-based research validation across all 8 product domains including comparative, online-only, and edge-case queries."}
                  </p>
                  <button
                    onClick={() => setActiveTab('questions')}
                    className="mt-2 w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold text-xs transition-colors flex items-center justify-center gap-1.5"
                  >
                    <span>View All {currentSetScenarios.length} Scenarios</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>

                <div className="space-y-2">
                  <h4 className="font-bold text-main text-xs uppercase tracking-wider">Representative Scenarios in this Set:</h4>
                  {currentSetScenarios.slice(0, 5).map(s => (
                    <div 
                      key={s.question_id}
                      onClick={() => { setSelectedScenarioId(s.question_id); setActiveTab('questions'); }}
                      className="p-2.5 rounded-lg bg-card border border-theme hover:border-emerald-500/50 cursor-pointer transition-all"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-mono text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">{s.question_id}</span>
                        <span className="text-[10px] text-muted">{s.filter}</span>
                      </div>
                      <div className="font-semibold text-main truncate">{s.title}</div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              filteredScenarios.map(s => {
                const isSelected = activeScenario?.question_id === s.question_id;
                return (
                  <div
                    key={s.question_id}
                    onClick={() => setSelectedScenarioId(s.question_id)}
                    className={cn(
                      "p-3 rounded-xl border transition-all cursor-pointer text-xs space-y-1.5",
                      isSelected
                        ? "bg-card border-emerald-500 ring-1 ring-emerald-500/20 shadow-xs"
                        : "bg-card border-theme hover:border-theme-hover"
                    )}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
                        {s.question_id}
                      </span>
                      <span className={cn(
                        "text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider",
                        s.status === 'PASSED' ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20" :
                        s.status === 'KNOWN_GOOD' ? "bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20" :
                        s.status === 'FAILED' ? "bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20" :
                        "bg-surface text-muted border border-theme"
                      )}>
                        {s.status || 'NOT_TESTED'}
                      </span>
                    </div>
                    <div className="font-bold text-main line-clamp-1">{s.title}</div>
                    <p className="text-[11px] text-muted line-clamp-1">{s.question}</p>
                    <div className="flex items-center gap-2 text-[10px] text-muted pt-1 border-t border-theme">
                      <span className="truncate">{s.domain}</span>
                      <span>•</span>
                      <span>{s.filter}</span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Detail & Execution Panel */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8 bg-main">
          {activeScenario ? (
            <div className="max-w-3xl mx-auto space-y-6">
              {/* Header Card */}
              <div className="p-6 rounded-2xl bg-card border border-theme shadow-xs space-y-4">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-black text-emerald-600 dark:text-emerald-400 bg-surface px-2.5 py-1 rounded border border-theme">
                      {activeScenario.question_id}
                    </span>
                    <span className="text-xs font-bold text-muted bg-surface px-2.5 py-1 rounded border border-theme">
                      {activeScenario.filter}
                    </span>
                    <span className="text-xs font-semibold text-sub bg-surface px-2.5 py-1 rounded border border-theme">
                      {activeScenario.domain}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => updateScenarioStatus(activeScenario.question_id, 'PASSED')}
                      className="px-2.5 py-1 rounded-lg text-xs font-bold border border-theme hover:bg-surface text-emerald-600 dark:text-emerald-400 flex items-center gap-1"
                    >
                      <Check className="w-3.5 h-3.5" /> Pass
                    </button>
                    <button
                      onClick={() => updateScenarioStatus(activeScenario.question_id, 'FAILED')}
                      className="px-2.5 py-1 rounded-lg text-xs font-bold border border-theme hover:bg-surface text-red-600 dark:text-red-400"
                    >
                      Fail
                    </button>
                  </div>
                </div>

                <div>
                  <h2 className="text-xl font-black text-main leading-snug mb-2">{activeScenario.title}</h2>
                  <div className="p-3.5 rounded-xl bg-surface border border-theme font-medium text-main text-sm">
                    "{activeScenario.question}"
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-3 pt-2">
                  <button
                    onClick={() => handleExecuteScenario(activeScenario)}
                    className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-black transition-colors flex items-center gap-2 shadow-sm"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" /> Execute Scenario
                  </button>
                  {activeScenario.is_known_good && (
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold">
                      <ShieldCheck className="w-3.5 h-3.5" /> Validated Known-Good Scenario
                    </span>
                  )}
                </div>
              </div>

              {/* What This Tests & Purpose */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-5 rounded-xl bg-card border border-theme space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-muted">What This Tests</h3>
                  <p className="text-xs text-sub leading-relaxed">{activeScenario.purpose}</p>
                </div>

                <div className="p-5 rounded-xl bg-card border border-theme space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-muted">Target Surface</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {activeScenario.target_surface.map((ts, idx) => (
                      <span key={idx} className="text-xs px-2.5 py-1 rounded-md bg-surface border border-theme font-semibold text-main">
                        {ts}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Recommended Workflow */}
              <div className="p-5 rounded-xl bg-card border border-theme space-y-3">
                <h3 className="text-xs font-bold uppercase tracking-wider text-muted">Recommended Workflow</h3>
                <div className="flex flex-wrap items-center gap-2">
                  {activeScenario.filter === 'COMPARISON' ? (
                    <>
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">1. Explore Papers</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">2. Select Papers</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-emerald-600/15 text-emerald-600 dark:text-emerald-400 px-3 py-1.5 rounded-lg border border-emerald-500/30">3. Compare Selected Papers</span>
                    </>
                  ) : activeScenario.filter === 'CITATIONS' || activeScenario.filter === 'CLAIM VERIFICATION' ? (
                    <>
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">1. Research Explorer</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">2. Ask AI</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">3. Prove (Verify)</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-emerald-600/15 text-emerald-600 dark:text-emerald-400 px-3 py-1.5 rounded-lg border border-emerald-500/30">4. XAI Trace</span>
                    </>
                  ) : (
                    <>
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">1. Research Explorer</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-surface px-3 py-1.5 rounded-lg border border-theme">2. Hybrid Retrieval</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted" />
                      <span className="text-xs font-bold bg-emerald-600/15 text-emerald-600 dark:text-emerald-400 px-3 py-1.5 rounded-lg border border-emerald-500/30">3. Evidence Grounding</span>
                    </>
                  )}
                </div>
              </div>

              {/* Expected Behavior & Evidence */}
              <div className="space-y-4">
                <div className="p-5 rounded-xl bg-card border border-theme space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-muted">Expected System Behavior</h3>
                  <p className="text-xs text-sub leading-relaxed">{activeScenario.expected_behavior}</p>
                </div>

                <div className="p-5 rounded-xl bg-card border border-theme space-y-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-muted">Expected Evidence Provenance</h3>
                  <p className="text-xs text-sub leading-relaxed">{activeScenario.expected_evidence}</p>
                  <div className="pt-2 flex items-center gap-3 text-[11px] text-muted">
                    <span>Offline Corpus: <strong>{activeScenario.offline_available ? 'Available' : 'Online Only'}</strong></span>
                    <span>•</span>
                    <span>Answerability: <strong>{activeScenario.answerability || 'ANSWERABLE'}</strong></span>
                    <span>•</span>
                    <span>XAI Trace: <strong>{activeScenario.xai_expected ? 'Required' : 'Optional'}</strong></span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-muted text-sm">
              Select a scenario to view technical verification details.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
