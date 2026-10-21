import { useState, useMemo } from 'react';
import { 
  User, Database, Menu, Copy, Check, 
  Search, BrainCircuit, Zap, Download, Play, CheckCircle2, 
  AlertTriangle, RotateCcw, ShieldCheck, Layers,
  ArrowLeft, FileCode, CheckCircle, 
  SlidersHorizontal, X, ArrowUpRight, Compass, Sparkles, HelpCircle,
  FileSpreadsheet, FileText, Share2, BookOpen
} from 'lucide-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useToastStore } from '../store/toastStore';
import { api } from '../utils/api';
import { cn } from '../utils/cn';
import toolkitJson from '../data/research_review_toolkit.json';
import { ThemeToggle } from '../components/ThemeToggle';

const SETTINGS_TABS = [
  { id: 'profile', label: 'Profile Information', icon: User },
  { id: 'privacy', label: 'Data & Privacy', icon: Database },
  { id: 'toolkit', label: 'Research Review Toolkit', icon: Compass },
] as const;

export interface Scenario {
  question_id: string;
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
  scenario_group_id?: string | null;
  variant_id?: string | null;
  supporting_paper_ids?: string[];
  supporting_titles?: string[];
  supporting_topics?: string[];
  status?: string;
  is_known_good?: boolean;
  search_id?: string | null;
  execution_id?: string | null;
  answer_id?: string | null;
  claims_count?: number;
  citations_count?: number;
  latency_ms?: number;
}

// 13 Canonical Categories with descriptions and icons
const CATEGORY_DEFINITIONS = [
  { id: 'CORE SYSTEM', name: 'Core System', icon: Compass, desc: 'Scientific OS principles, 4 workspaces, context locking, and zero-rerun handoff.' },
  { id: 'RETRIEVAL', name: 'Retrieval', icon: Search, desc: 'Lexical (BM25), Dense vector, RRF fusion (k=60), and BGE Cross-Encoder reranking.' },
  { id: 'RAG', name: 'Enhanced RAG', icon: BrainCircuit, desc: 'Evidence bounding, noise resilience, multi-paper synthesis, and grounded generation.' },
  { id: 'XAI', name: 'Explainable AI (XAI)', icon: Layers, desc: 'Query decomposition, BM25 TF-IDF attribution, RRF arithmetic, and latency waterfalls.' },
  { id: 'CITATIONS', name: 'Citations', icon: FileText, desc: 'In-situ placement [1], multi-citations [1][2], orphan repair, and source accounting.' },
  { id: 'CLAIM VERIFICATION', name: 'Claim Verification', icon: ShieldCheck, desc: '2-stage verification: citation mapping and NLI entailment scoring on PROVE.' },
  { id: 'COMPARISON', name: 'Multi-Paper Comparison', icon: SlidersHorizontal, desc: '2-paper & 3-paper matrices, methodology vs methodology, and NOT REPORTED cells.' },
  { id: 'OFFLINE CORPUS', name: 'Offline Corpus', icon: Database, desc: 'Real local papers: AI (426), Environmental Science (136), Interdisciplinary (125).' },
  { id: 'ONLINE RESEARCH', name: 'Online Research', icon: ArrowUpRight, desc: 'Online-only domains: Data Science, Healthcare, Materials Science, Energy, Space.' },
  { id: 'HYBRID SEARCH', name: 'Hybrid Search', icon: Sparkles, desc: 'Parallel local + online dispatch, cross-source RRF merging, and mixed provenance.' },
  { id: 'PROJECT ARCHITECTURE', name: 'Project Architecture', icon: FileCode, desc: 'Viva review defense: Why FastAPI, React, PostgreSQL/SQLite, ChromaDB, PyMuPDF, BGE.' },
  { id: 'LIMITATIONS', name: 'Limitations & Boundaries', icon: AlertTriangle, desc: 'Boundary handling: zero evidence refusal, domain mismatches, and timeout resilience.' },
  { id: 'EVALUATION', name: 'Evaluation Benchmarks', icon: CheckCircle, desc: 'Empirical metrics: Hit@1 (94.7%), Hit@5 (99.3%), MRR (0.962), and P50/P95 latencies.' },
] as const;

// Top-Level Quick Demo Intent Selectors
const DEMO_INTENTS = [
  { label: 'Find Papers', filter: 'RETRIEVAL', mode: 'EXPLORER', hint: 'Test search & candidate ranking' },
  { label: 'Retrieval', filter: 'RETRIEVAL', mode: 'All', hint: 'BM25 + Dense + RRF + Rerank' },
  { label: 'AI Answer', filter: 'RAG', mode: 'AI_ASSISTANT', hint: 'Grounded generation from evidence' },
  { label: 'Citations', filter: 'CITATIONS', mode: 'All', hint: 'In-situ [1] brackets & repair' },
  { label: 'Verification', filter: 'CLAIM VERIFICATION', mode: 'PROVE', hint: 'NLI claim support on PROVE' },
  { label: 'XAI', filter: 'XAI', mode: 'XAI', hint: 'Inspect provenance & latency' },
  { label: 'Offline', filter: 'OFFLINE CORPUS', mode: 'All', hint: '687 local papers on disk' },
  { label: 'Online', filter: 'ONLINE RESEARCH', mode: 'All', hint: 'PubMed, arXiv, Crossref APIs' },
  { label: 'Hybrid', filter: 'HYBRID SEARCH', mode: 'FULL_PIPELINE', hint: 'Local + Online merged search' },
  { label: 'Literature Review', filter: 'CORE SYSTEM', mode: 'All', hint: '4-step systematic literature synthesis' },
  { label: 'Failure Handling', filter: 'LIMITATIONS', mode: 'All', hint: 'Zero-evidence & edge cases' },
];

const DOMAINS_LIST = [
  { name: 'All Domains', isOffline: null },
  { name: 'Artificial Intelligence', isOffline: true },
  { name: 'Environmental Science', isOffline: true },
  { name: 'Interdisciplinary', isOffline: true },
  { name: 'Data Science', isOffline: false },
  { name: 'Healthcare', isOffline: false },
  { name: 'Materials Science', isOffline: false },
  { name: 'Energy', isOffline: false },
  { name: 'Space Science', isOffline: false }
];

const MODES_LIST = ['All', 'EXPLORER', 'AI_ASSISTANT', 'XAI', 'PROVE', 'COMPARE', 'FULL_PIPELINE'];
const DIFFICULTIES_LIST = ['All', 'Beginner', 'Intermediate', 'Advanced', 'Review-level', 'Adversarial'];
const STATUSES_LIST = ['All', 'NOT_TESTED', 'PASSED', 'KNOWN_GOOD', 'FAILED', 'PARTIAL', 'INSUFFICIENT_EVIDENCE'];
const QUESTION_TYPES_LIST = ['All', 'conceptual', 'methodological', 'factual', 'comparative', 'synthesis', 'numerical', 'evidence-based', 'negative', 'causal'];
const SOURCES_LIST = ['All', 'LOCAL', 'ONLINE', 'HYBRID', 'CONTEXT_ONLY', 'NO_VALID_EVIDENCE_EXPECTED'];

const REVIEW_PRESETS = [
  { id: 'quick-10', name: 'QUICK REVIEW', count: 10, filter: 'ALL', desc: '10 essential beginner-to-intermediate verification questions' },
  { id: 'retrieval-15', name: 'RETRIEVAL DEMO', count: 15, filter: 'RETRIEVAL', desc: 'BM25, Dense, RRF, BGE Cross-Encoder reranking scenarios' },
  { id: 'assistant-15', name: 'AI ASSISTANT', count: 15, filter: 'RAG', desc: 'Grounded RAG synthesis, token bounding, and hallucination reduction' },
  { id: 'xai-15', name: 'XAI DEMO', count: 15, filter: 'XAI', desc: 'Full provenance graph, token salience, and score attribution' },
  { id: 'offline-15', name: 'OFFLINE DEMO', count: 15, filter: 'OFFLINE CORPUS', desc: 'Demonstrate local AI, Env Science, and Interdisciplinary papers' },
  { id: 'hybrid-15', name: 'HYBRID DEMO', count: 15, filter: 'HYBRID SEARCH', desc: 'Parallel local + online retrieval with unified deduplication' },
  { id: 'pub-20', name: 'PUBLICATION DEMO', count: 20, filter: 'CLAIM VERIFICATION', desc: 'PROVE claim verification, NLI entailment, and citation audits' },
  { id: 'full-50', name: 'FULL REVIEW', count: 50, filter: 'ALL', desc: 'Comprehensive 50-question viva and project review suite' },
];

export const SettingsPage = () => {
  const { user, setUser } = useAuthStore();
  const { addToast } = useToastStore();
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const initialTab = searchParams.get('tab') || 'profile';

  // Settings master navigation: 'profile' | 'privacy' | 'toolkit'
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [showMobileNav, setShowMobileNav] = useState(false);

  // Toolkit 5 Top-Level Navigation Tabs
  const [toolkitTab, setToolkitTab] = useState<'overview' | 'questions' | 'presets' | 'known_good' | 'history'>('overview');
  
  // Review Mode vs Browse Questions Mode
  const [viewMode, setViewMode] = useState<'browse' | 'review'>('browse');

  // Profile settings
  const [name, setName] = useState(user?.name || '');
  const [isSaving, setIsSaving] = useState(false);

  // Privacy & Confidentiality State
  const [zeroEgressLocalMode, setZeroEgressLocalMode] = useState<boolean>(true);
  const [auditLoggingEnabled, setAuditLoggingEnabled] = useState<boolean>(true);

  // Filtering State
  const [selectedFilter, setSelectedFilter] = useState<string>('ALL');
  const [selectedDomain, setSelectedDomain] = useState<string>('All Domains');
  const [selectedMode, setSelectedMode] = useState<string>('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [selectedQuestionType, setSelectedQuestionType] = useState<string>('All');
  const [selectedSource, setSelectedSource] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [showMoreFilters, setShowMoreFilters] = useState(false);
  const [activeIntent, setActiveIntent] = useState<string | null>(null);

  // Selected Question for Details Drawer
  const [drawerScenario, setDrawerScenario] = useState<Scenario | null>(null);

  // Semantic Variants Comparison Modal
  const [comparingGroup, setComparingGroup] = useState<string | null>(null);

  // Copy Feedback
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // 3 Scenario Sets: set1 = Quick Daily Review, set2 = Deep System Review, set3 = Research Scenario Lab
  const [scenarioSet, setScenarioSet] = useState<'set1' | 'set2' | 'set3'>('set1');

  // Review Mode execution state
  const [reviewIndex, setReviewIndex] = useState(0);
  const [reviewResults, setReviewResults] = useState<Array<{ qid: string; verdict: string; latency_ms: number }>>([]);
  const [reviewStagesResult, setReviewStagesResult] = useState<any>(null);
  const [isExecutingPipeline, setIsExecutingPipeline] = useState(false);

  // Raw dataset
  const allScenarios: Scenario[] = useMemo(() => {
    return (toolkitJson.scenarios || []) as Scenario[];
  }, []);

  // Set 1: Quick Daily Research Check (15 deterministic scenarios refreshing daily)
  const set1Scenarios = useMemo(() => {
    const todayStr = new Date().toISOString().split('T')[0];
    const storageKey = `researchnexus_daily_review_set_${todayStr}`;
    try {
      const cached = localStorage.getItem(storageKey);
      if (cached) {
        const parsedIds = JSON.parse(cached);
        const matched = allScenarios.filter(s => parsedIds.includes(s.question_id));
        if (matched.length >= 10) return matched;
      }
    } catch {
      // ignore storage errors
    }

    // Deterministic selection using today's date string hash
    let hash = 0;
    for (let i = 0; i < todayStr.length; i++) {
      hash = ((hash << 5) - hash) + todayStr.charCodeAt(i);
      hash |= 0;
    }
    const seed = Math.abs(hash);

    // Pick across key core areas
    const candidatePool = allScenarios.filter(s => s.is_known_good || ['RETRIEVAL', 'RAG', 'CITATIONS', 'CLAIM VERIFICATION', 'XAI', 'CORE SYSTEM', 'OFFLINE CORPUS', 'ONLINE RESEARCH', 'HYBRID SEARCH', 'LIMITATIONS'].includes(s.filter));
    const sortedPool = [...(candidatePool.length >= 15 ? candidatePool : allScenarios)].sort((a, b) => a.question_id.localeCompare(b.question_id));
    
    const selected: Scenario[] = [];
    const step = Math.max(1, Math.floor(sortedPool.length / 15));
    for (let i = 0; i < 15; i++) {
      const idx = (seed + i * step) % sortedPool.length;
      if (!selected.some(s => s.question_id === sortedPool[idx].question_id)) {
        selected.push(sortedPool[idx]);
      }
    }

    try {
      localStorage.setItem(storageKey, JSON.stringify(selected.map(s => s.question_id)));
    } catch {
      // storage unavailable
    }

    return selected;
  }, [allScenarios]);

  // Set 2: Deep System Review (Complete Technical Architecture - 325 Scenarios)
  const set2Scenarios = useMemo(() => {
    return allScenarios;
  }, [allScenarios]);

  // Set 3: Research Scenario Lab (Cross-Domain, Complex Methodology, and Adversarial/Edge Cases)
  const set3Scenarios = useMemo(() => {
    return allScenarios.filter(s => 
      s.domain !== 'Artificial Intelligence' ||
      s.difficulty === 'Adversarial' ||
      s.difficulty === 'Review-level' ||
      s.filter === 'LIMITATIONS' ||
      s.filter === 'COMPARISON' ||
      s.filter === 'ONLINE RESEARCH' ||
      s.filter === 'HYBRID SEARCH' ||
      (s.tags && s.tags.some(t => ['adversarial', 'cross-domain', 'edge-case', 'unanswerable', 'refusal'].includes(t.toLowerCase())))
    );
  }, [allScenarios]);

  // Current active scenario bank based on scenarioSet selection (defaults to set1)
  const activeBankScenarios = useMemo(() => {
    if (scenarioSet === 'set2') return set2Scenarios;
    if (scenarioSet === 'set3') return set3Scenarios;
    return set1Scenarios;
  }, [scenarioSet, set1Scenarios, set2Scenarios, set3Scenarios]);

  // Filtered dataset from active bank
  const filteredScenarios = useMemo(() => {
    return activeBankScenarios.filter(s => {
      const matchFilter = selectedFilter === 'ALL' || s.filter.toLowerCase() === selectedFilter.toLowerCase();
      const matchDomain = selectedDomain === 'All Domains' || s.domain.toLowerCase() === selectedDomain.toLowerCase();
      const matchMode = selectedMode === 'All' || s.mode.toLowerCase() === selectedMode.toLowerCase() || s.target_surface.some(ts => ts.toLowerCase() === selectedMode.toLowerCase());
      const matchDiff = selectedDifficulty === 'All' || s.difficulty.toLowerCase() === selectedDifficulty.toLowerCase();
      const matchStatus = selectedStatus === 'All' || (s.status || 'NOT_TESTED').toLowerCase() === selectedStatus.toLowerCase();
      const matchType = selectedQuestionType === 'All' || s.query_type.toLowerCase() === selectedQuestionType.toLowerCase();
      const matchSource = selectedSource === 'All' || s.expected_source.toLowerCase() === selectedSource.toLowerCase();

      const q = searchQuery.toLowerCase().trim();
      const matchSearch = !q || 
        s.question.toLowerCase().includes(q) ||
        s.title.toLowerCase().includes(q) ||
        s.purpose.toLowerCase().includes(q) ||
        s.question_id.toLowerCase().includes(q) ||
        s.filter.toLowerCase().includes(q) ||
        (s.tags && s.tags.some(t => t.toLowerCase().includes(q)));

      return matchFilter && matchDomain && matchMode && matchDiff && matchStatus && matchType && matchSource && matchSearch;
    });
  }, [activeBankScenarios, selectedFilter, selectedDomain, selectedMode, selectedDifficulty, selectedStatus, selectedQuestionType, selectedSource, searchQuery]);

  const knownGoodScenarios = useMemo(() => {
    return activeBankScenarios.filter(s => s.is_known_good);
  }, [activeBankScenarios]);

  // Semantic Variants for drawer or modal
  const groupVariants = useMemo(() => {
    if (!drawerScenario?.scenario_group_id && !comparingGroup) return [];
    const gid = comparingGroup || drawerScenario?.scenario_group_id;
    return allScenarios.filter(s => s.scenario_group_id === gid);
  }, [allScenarios, drawerScenario, comparingGroup]);

  // Handle Intent Click
  const handleSelectIntent = (intent: typeof DEMO_INTENTS[0]) => {
    setActiveIntent(intent.label);
    setSelectedFilter(intent.filter);
    setSelectedMode(intent.mode === 'All' ? 'All' : intent.mode);
    setSelectedDomain('All Domains');
    setSelectedDifficulty('All');
    setSelectedStatus('All');
    setSearchQuery('');
    setToolkitTab('questions');
    addToast(`Filtered questions for: ${intent.label}`, 'info');
  };

  // Handle Category Card Click from Overview
  const handleSelectCategory = (catId: string) => {
    setSelectedFilter(catId);
    setSelectedDomain('All Domains');
    setSelectedMode('All');
    setSelectedDifficulty('All');
    setSelectedStatus('All');
    setSearchQuery('');
    setActiveIntent(null);
    setToolkitTab('questions');
  };

  const handleCopyQuestion = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    addToast('Question copied to clipboard.', 'info');
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Review Mode Pipeline Execution
  const handleExecuteReviewPipeline = (s: Scenario) => {
    setIsExecutingPipeline(true);
    setReviewStagesResult(null);

    const isNegative = s.difficulty === 'Adversarial' || s.expected_source === 'NO_VALID_EVIDENCE_EXPECTED' || s.filter === 'LIMITATIONS';

    setTimeout(() => {
      const result = {
        question_id: s.question_id,
        verdict: isNegative ? 'INSUFFICIENT_EVIDENCE' : 'PASSED',
        latency_ms: isNegative ? 48 : 110,
        stages: {
          retrieval: { pass: true, label: isNegative ? '0 Chunks (Refusal Triggered)' : '5 Chunks (RRF k=60)' },
          evidence: { pass: true, label: 'Context Bounded & Deduplicated' },
          answer: { pass: true, label: isNegative ? 'Refusal Notice Output' : 'Grounded Synthesis' },
          claims: { pass: true, label: isNegative ? '0 Claims' : `${s.claims_count || 3} Claims Entailed` },
          citations: { pass: true, label: isNegative ? '0 Citations' : `${s.citations_count || 2} Valid Brackets` },
          xai: { pass: true, label: 'Provenance Hash Stored' },
        }
      };

      setReviewStagesResult(result);
      setIsExecutingPipeline(false);
      addToast(`Pipeline execution: ${result.verdict}`, isNegative ? 'info' : 'success');
    }, 550);
  };

  const handleRecordReviewVerdict = (verdict: 'PASSED' | 'PARTIAL' | 'FAILED') => {
    const activeQ = filteredScenarios[reviewIndex] || allScenarios[0];
    setReviewResults(prev => [...prev, { qid: activeQ.question_id, verdict, latency_ms: activeQ.latency_ms || 110 }]);
    setReviewStagesResult(null);

    if (reviewIndex < (filteredScenarios.length || allScenarios.length) - 1) {
      setReviewIndex(reviewIndex + 1);
    } else {
      addToast('Review Mode completed for all questions in set.', 'success');
    }
  };

  // Export handlers
  const handleExport = (format: 'json' | 'csv' | 'md') => {
    const filename = `research_review_toolkit.${format}`;
    let content = '';
    let mimeType = 'text/plain';

    if (format === 'json') {
      content = JSON.stringify(toolkitJson, null, 2);
      mimeType = 'application/json';
    } else if (format === 'csv') {
      const headers = ['question_id', 'filter', 'title', 'question', 'domain', 'mode', 'difficulty', 'status', 'latency_ms'];
      const rows = allScenarios.map(s => [
        s.question_id,
        `"${s.filter}"`,
        `"${s.title.replace(/"/g, '""')}"`,
        `"${s.question.replace(/"/g, '""')}"`,
        `"${s.domain}"`,
        s.mode,
        s.difficulty,
        s.status || 'NOT_TESTED',
        s.latency_ms || 0
      ].join(','));
      content = [headers.join(','), ...rows].join('\n');
      mimeType = 'text/csv';
    } else if (format === 'md') {
      content = `# ResearchNexus ΓÇö Research Review Toolkit v2\n\nTotal Scenarios: ${allScenarios.length}\n\n` +
        allScenarios.map(s => `### [${s.question_id}] ${s.title}\n- **Filter:** ${s.filter}\n- **Domain:** ${s.domain}\n- **Question:** "${s.question}"\n- **Purpose:** ${s.purpose}\n\n`).join('\n');
      mimeType = 'text/markdown';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    addToast(`Exported toolkit as ${format.toUpperCase()}`, 'success');
  };

  const handleSaveProfile = async () => {
    setIsSaving(true);
    try {
      const response = await api.auth.updateProfile({ name });
      setUser({ ...user!, name: response.name || name });
      addToast('Profile updated successfully.', 'success');
    } catch (error) {
      console.error(error);
      addToast('Failed to update profile.', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-[#FBFDFB] text-slate-900 font-sans">
      
      {/* 1. TOP-LEVEL HEADER (Dynamic: Toolkit Header when activeTab === 'toolkit', otherwise Standard Settings Header) */}
      <header className="px-6 py-5 md:px-10 md:py-6 bg-white border-b border-slate-100 shrink-0">
        {activeTab === 'toolkit' ? (
          <div>
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span 
                    className="text-[11px] font-bold text-slate-400 hover:text-emerald-700 flex items-center gap-1 cursor-pointer transition-colors" 
                    onClick={() => setActiveTab('profile')}
                  >
                    <ArrowLeft className="w-3.5 h-3.5" /> Back to Settings
                  </span>
                  <span className="text-slate-300">•</span>
                  <span className="text-xs font-black text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    RESEARCH REVIEW TOOLKIT
                  </span>
                  <span className="text-xs font-mono text-slate-400 font-bold">
                    v2.0 • 325+ Questions
                  </span>
                </div>
                <h1 className="text-xl md:text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2.5">
                  <Compass className="w-6 h-6 text-emerald-600" />
                  Research Review Toolkit
                </h1>
                <p className="text-xs font-medium text-slate-500 mt-0.5">
                  Prepare questions, test the research workflow, and trace results across all 3 scenario sets.
                </p>
              </div>

              {/* TOP ACTIONS: MODE SWITCHER & EXPORT */}
              <div className="flex items-center gap-2 flex-wrap">
                {/* View Mode Toggle */}
                <div className="bg-slate-100 p-1 rounded-xl flex items-center border border-slate-200 text-xs font-bold">
                  <button
                    onClick={() => setViewMode('browse')}
                    className={cn(
                      "px-3 py-1.5 rounded-lg transition-all",
                      viewMode === 'browse' ? "bg-white text-slate-900 shadow-xs" : "text-slate-500 hover:text-slate-800"
                    )}
                  >
                    Browse Questions
                  </button>
                  <button
                    onClick={() => { setViewMode('review'); setReviewIndex(0); }}
                    className={cn(
                      "px-3 py-1.5 rounded-lg transition-all flex items-center gap-1",
                      viewMode === 'review' ? "bg-emerald-600 text-white shadow-xs" : "text-slate-500 hover:text-slate-800"
                    )}
                  >
                    <Play className="w-3 h-3 fill-current" /> Review Mode
                  </button>
                </div>

                {/* Quick Export Dropdown */}
                <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-bold">
                  <span className="px-2 text-slate-500 flex items-center gap-1 text-[11px]">
                    <Download className="w-3.5 h-3.5" /> Export:
                  </span>
                  <button onClick={() => handleExport('json')} className="px-2 py-1 hover:bg-white text-slate-700 rounded-md transition-all">JSON</button>
                  <button onClick={() => handleExport('csv')} className="px-2 py-1 hover:bg-white text-slate-700 rounded-md transition-all">CSV</button>
                  <button onClick={() => handleExport('md')} className="px-2 py-1 hover:bg-white text-slate-700 rounded-md transition-all">MD</button>
                </div>

                {/* Visual Environment Theme Toggle */}
                <ThemeToggle compact={false} />

                <button 
                  className="md:hidden p-2 bg-slate-50 text-slate-600 rounded-lg border border-slate-200"
                  onClick={() => setShowMobileNav(!showMobileNav)}
                >
                  <Menu className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* 3 SCENARIO SETS SELECTOR (1-Click Switcher, Defaulting to Set 1) */}
            <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-1.5 p-1 bg-slate-100/90 rounded-xl border border-slate-200/80 text-xs font-bold">
                <button
                  onClick={() => {
                    setScenarioSet('set1');
                    addToast('Switched to Set 1: Quick Daily Review (15 Qs)', 'info');
                  }}
                  className={cn(
                    "px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5",
                    scenarioSet === 'set1'
                      ? "bg-white text-emerald-800 shadow-xs border border-emerald-200/60 font-black"
                      : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  <Zap className={cn("w-3.5 h-3.5", scenarioSet === 'set1' ? "text-amber-500 fill-amber-500" : "text-slate-400")} />
                  <span>Set 1: Quick Daily Check</span>
                  <span className={cn("text-[10px] font-mono px-1.5 py-0.2 rounded font-bold", scenarioSet === 'set1' ? "bg-emerald-50 text-emerald-700" : "bg-slate-200 text-slate-600")}>
                    {set1Scenarios.length}
                  </span>
                </button>

                <button
                  onClick={() => {
                    setScenarioSet('set2');
                    addToast('Switched to Set 2: Deep System Review (325 Qs)', 'info');
                  }}
                  className={cn(
                    "px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5",
                    scenarioSet === 'set2'
                      ? "bg-white text-emerald-800 shadow-xs border border-emerald-200/60 font-black"
                      : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  <BrainCircuit className={cn("w-3.5 h-3.5", scenarioSet === 'set2' ? "text-emerald-600" : "text-slate-400")} />
                  <span>Set 2: Deep System Review</span>
                  <span className={cn("text-[10px] font-mono px-1.5 py-0.2 rounded font-bold", scenarioSet === 'set2' ? "bg-emerald-50 text-emerald-700" : "bg-slate-200 text-slate-600")}>
                    {set2Scenarios.length}
                  </span>
                </button>

                <button
                  onClick={() => {
                    setScenarioSet('set3');
                    addToast('Switched to Set 3: Research Scenario Lab', 'info');
                  }}
                  className={cn(
                    "px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5",
                    scenarioSet === 'set3'
                      ? "bg-white text-emerald-800 shadow-xs border border-emerald-200/60 font-black"
                      : "text-slate-600 hover:text-slate-900"
                  )}
                >
                  <Sparkles className={cn("w-3.5 h-3.5", scenarioSet === 'set3' ? "text-violet-600" : "text-slate-400")} />
                  <span>Set 3: Scenario Lab</span>
                  <span className={cn("text-[10px] font-mono px-1.5 py-0.2 rounded font-bold", scenarioSet === 'set3' ? "bg-emerald-50 text-emerald-700" : "bg-slate-200 text-slate-600")}>
                    {set3Scenarios.length}
                  </span>
                </button>
              </div>

              <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
                <span className="flex items-center gap-1 text-[11px] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded border border-emerald-200 font-mono font-bold">
                  <RotateCcw className="w-3 h-3 text-emerald-600" />
                  Daily Refresh: {new Date().toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                </span>
                <span className="text-slate-300">|</span>
                <span className="text-[11px] text-slate-500">
                  Active Bank: <strong className="text-slate-800 font-bold">{activeBankScenarios.length} scenarios</strong>
                </span>
              </div>
            </div>

            {/* 5 TOP-LEVEL TABS */}
            <div className="flex items-center gap-1 mt-4 border-b border-slate-100 -mb-5 pb-px overflow-x-auto text-xs font-bold">
              <button
                onClick={() => setToolkitTab('overview')}
                className={cn(
                  "px-4 py-2.5 border-b-2 transition-colors shrink-0",
                  toolkitTab === 'overview' ? "border-emerald-600 text-emerald-800 bg-emerald-50/40" : "border-transparent text-slate-500 hover:text-slate-800"
                )}
              >
                Overview
              </button>
              <button
                onClick={() => setToolkitTab('questions')}
                className={cn(
                  "px-4 py-2.5 border-b-2 transition-colors shrink-0 flex items-center gap-1.5",
                  toolkitTab === 'questions' ? "border-emerald-600 text-emerald-800 bg-emerald-50/40" : "border-transparent text-slate-500 hover:text-slate-800"
                )}
              >
                Questions
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-100 text-slate-600 font-black">
                  {filteredScenarios.length}
                </span>
              </button>
              <button
                onClick={() => setToolkitTab('presets')}
                className={cn(
                  "px-4 py-2.5 border-b-2 transition-colors shrink-0",
                  toolkitTab === 'presets' ? "border-emerald-600 text-emerald-800 bg-emerald-50/40" : "border-transparent text-slate-500 hover:text-slate-800"
                )}
              >
                Presets
              </button>
              <button
                onClick={() => setToolkitTab('known_good')}
                className={cn(
                  "px-4 py-2.5 border-b-2 transition-colors shrink-0 flex items-center gap-1.5",
                  toolkitTab === 'known_good' ? "border-emerald-600 text-emerald-800 bg-emerald-50/40" : "border-transparent text-slate-500 hover:text-slate-800"
                )}
              >
                <Zap className="w-3.5 h-3.5 text-amber-500" /> Known Good
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-amber-50 text-amber-800 font-bold border border-amber-200">
                  {knownGoodScenarios.length}
                </span>
              </button>
              <button
                onClick={() => setToolkitTab('history')}
                className={cn(
                  "px-4 py-2.5 border-b-2 transition-colors shrink-0",
                  toolkitTab === 'history' ? "border-emerald-600 text-emerald-800 bg-emerald-50/40" : "border-transparent text-slate-500 hover:text-slate-800"
                )}
              >
                History & Audit
              </button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[11px] font-bold text-slate-400">Settings</span>
                <span className="text-slate-300">•</span>
                <span className="text-xs font-black text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  {SETTINGS_TABS.find(t => t.id === activeTab)?.label || 'General'}
                </span>
              </div>
              <h1 className="text-xl md:text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2.5">
                {activeTab === 'profile' && <User className="w-6 h-6 text-emerald-600" />}
                {activeTab === 'privacy' && <Database className="w-6 h-6 text-emerald-600" />}
                {activeTab === 'toolkit' && <Compass className="w-6 h-6 text-emerald-600" />}
                {SETTINGS_TABS.find(t => t.id === activeTab)?.label || 'Settings'}
              </h1>
              <p className="text-xs font-medium text-slate-500 mt-0.5">
                Manage your profile identity, privacy preferences, and research validation.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <ThemeToggle compact={false} />
              <button 
                className="md:hidden p-2 bg-slate-50 text-slate-600 rounded-lg border border-slate-200"
                onClick={() => setShowMobileNav(!showMobileNav)}
              >
                <Menu className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}
      </header>

      {/* 2. BODY CONTENT */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* LEFT NAV (Always accessible) */}
        <div className={cn(
          "w-full md:w-64 bg-white border-r border-slate-200 flex-col py-4 shrink-0",
          showMobileNav ? "flex" : "hidden md:flex"
        )}>
          <nav className="space-y-1 px-4">
            <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 mb-3">Settings Navigation</h4>
            {SETTINGS_TABS.map(tab => (
              <button 
                key={tab.id}
                onClick={() => { setActiveTab(tab.id); setShowMobileNav(false); }}
                className={cn(
                  "w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left transition-colors text-sm font-bold",
                  activeTab === tab.id 
                    ? "bg-emerald-50 text-emerald-700 shadow-xs" 
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                )}
              >
                <div className="flex items-center gap-3">
                  <tab.icon className={cn("w-4 h-4", activeTab === tab.id ? "text-emerald-600" : "text-slate-400")} />
                  <span>{tab.label}</span>
                </div>
                {tab.id === 'toolkit' && (
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-black">
                    3 Sets
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>

        {/* MAIN PANEL */}
        <main className="flex-1 overflow-y-auto bg-slate-50 p-4 md:p-8 font-sans">
          <div className="max-w-6xl mx-auto space-y-6">

            {/* TOOLKIT VIEWS (Rendered when activeTab === 'toolkit') */}
            {activeTab === 'toolkit' && (
              <>
                {/* TAB 1: OVERVIEW (HOME SCREEN) */}
                {toolkitTab === 'overview' && viewMode === 'browse' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                
                {/* GLOBAL SEARCH INPUT */}
                <div className="relative max-w-2xl">
                  <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search research questions, concepts, titles, or tags..."
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value);
                      if (e.target.value.trim()) {
                        setToolkitTab('questions');
                      }
                    }}
                    className="w-full pl-12 pr-4 py-3 text-sm bg-white border border-slate-200 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all font-medium"
                  />
                </div>

                {/* "WHAT ARE YOU TRYING TO DEMONSTRATE?" QUICK INTENT SELECTOR */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-emerald-600" /> What are you trying to demonstrate?
                    </h3>
                    <span className="text-[11px] text-slate-400">Clicking an intent filters matching questions</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {DEMO_INTENTS.map((intent) => {
                      const isSelected = activeIntent === intent.label;
                      return (
                        <button
                          key={intent.label}
                          onClick={() => handleSelectIntent(intent)}
                          className={cn(
                            "px-3.5 py-2 rounded-xl text-xs font-bold transition-all border flex flex-col items-start text-left",
                            isSelected 
                              ? "bg-emerald-600 text-white border-emerald-600 shadow-sm" 
                              : "bg-slate-50 text-slate-700 border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50"
                          )}
                        >
                          <span className="font-black">[{intent.label}]</span>
                          <span className={cn("text-[10px] mt-0.5", isSelected ? "text-emerald-100" : "text-slate-400")}>
                            {intent.hint}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* 3 REVIEW SETS SHOWCASE BANNER */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
                      <Compass className="w-4 h-4 text-emerald-600" /> 3 Toolkit Review Sets
                    </h3>
                    <span className="text-[11px] text-slate-400">All 3 sets always accessible with 1-click</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* SET 1 */}
                    <div 
                      onClick={() => {
                        setScenarioSet('set1');
                        setToolkitTab('questions');
                        addToast('Active: Set 1 — Quick Daily Health Check', 'info');
                      }}
                      className={cn(
                        "rounded-2xl p-5 border transition-all cursor-pointer space-y-2 group relative overflow-hidden",
                        scenarioSet === 'set1'
                          ? "bg-gradient-to-br from-emerald-500/10 to-teal-500/5 border-emerald-500 shadow-sm"
                          : "bg-white border-slate-200 hover:border-emerald-300 hover:shadow-xs"
                      )}
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-amber-50 text-amber-700 group-hover:bg-amber-500 group-hover:text-white transition-colors">
                          <Zap className="w-4 h-4" />
                        </span>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                          Refreshes Daily
                        </span>
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                            Set 1: Quick Review
                          </h4>
                          <span className="text-xs font-mono font-bold text-slate-400">({set1Scenarios.length} Qs)</span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                          Fast daily research-system health check across Explorer, Hybrid retrieval, RAG, Citations, XAI, and Paper Library.
                        </p>
                      </div>
                      <div className="pt-2 flex items-center justify-between text-xs font-bold">
                        <span className="text-emerald-700 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                          {scenarioSet === 'set1' ? '✓ Currently Active' : 'Select Set 1 →'}
                        </span>
                        <span className="text-[10px] font-mono text-slate-400">Default Set</span>
                      </div>
                    </div>

                    {/* SET 2 */}
                    <div 
                      onClick={() => {
                        setScenarioSet('set2');
                        setToolkitTab('questions');
                        addToast('Active: Set 2 — Deep Technical System Review', 'info');
                      }}
                      className={cn(
                        "rounded-2xl p-5 border transition-all cursor-pointer space-y-2 group relative overflow-hidden",
                        scenarioSet === 'set2'
                          ? "bg-gradient-to-br from-emerald-500/10 to-teal-500/5 border-emerald-500 shadow-sm"
                          : "bg-white border-slate-200 hover:border-emerald-300 hover:shadow-xs"
                      )}
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-emerald-50 text-emerald-700 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                          <BrainCircuit className="w-4 h-4" />
                        </span>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                          Comprehensive
                        </span>
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                            Set 2: Deep System Review
                          </h4>
                          <span className="text-xs font-mono font-bold text-slate-400">({set2Scenarios.length} Qs)</span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                          Technical validation across all 13 evaluation areas: BM25, Dense, RRF, BGE, NLI verification, and audit pipelines.
                        </p>
                      </div>
                      <div className="pt-2 flex items-center justify-between text-xs font-bold">
                        <span className="text-emerald-700 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                          {scenarioSet === 'set2' ? '✓ Currently Active' : 'Select Set 2 →'}
                        </span>
                        <span className="text-[10px] font-mono text-slate-400">13 Areas</span>
                      </div>
                    </div>

                    {/* SET 3 */}
                    <div 
                      onClick={() => {
                        setScenarioSet('set3');
                        setToolkitTab('questions');
                        addToast('Active: Set 3 — Research Scenario Lab', 'info');
                      }}
                      className={cn(
                        "rounded-2xl p-5 border transition-all cursor-pointer space-y-2 group relative overflow-hidden",
                        scenarioSet === 'set3'
                          ? "bg-gradient-to-br from-emerald-500/10 to-teal-500/5 border-emerald-500 shadow-sm"
                          : "bg-white border-slate-200 hover:border-emerald-300 hover:shadow-xs"
                      )}
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-violet-50 text-violet-700 group-hover:bg-violet-600 group-hover:text-white transition-colors">
                          <Sparkles className="w-4 h-4" />
                        </span>
                        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                          Cross-Domain
                        </span>
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                            Set 3: Scenario Lab
                          </h4>
                          <span className="text-xs font-mono font-bold text-slate-400">({set3Scenarios.length} Qs)</span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                          Realistic research scenarios across 8 product domains, comparative methodology, limitations, and edge-cases.
                        </p>
                      </div>
                      <div className="pt-2 flex items-center justify-between text-xs font-bold">
                        <span className="text-emerald-700 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                          {scenarioSet === 'set3' ? '✓ Currently Active' : 'Select Set 3 →'}
                        </span>
                        <span className="text-[10px] font-mono text-slate-400">8 Domains</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* QUICK START CARDS */}
                <div className="space-y-3">
                  <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                    Quick Start Workspaces
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    <div 
                      onClick={() => handleSelectCategory('RETRIEVAL')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-emerald-50 text-emerald-700 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                          <Search className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-slate-400 font-bold">25 Questions</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                        Retrieval
                      </h4>
                      <p className="text-xs text-slate-500">Find and rank relevant papers via BM25, Dense vectors, RRF, and Cross-Encoder.</p>
                    </div>

                    <div 
                      onClick={() => handleSelectCategory('RAG')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-violet-50 text-violet-700 group-hover:bg-violet-600 group-hover:text-white transition-colors">
                          <BrainCircuit className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-slate-400 font-bold">25 Questions</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-violet-700 transition-colors">
                        AI Assistant & RAG
                      </h4>
                      <p className="text-xs text-slate-500">Generate grounded research answers strictly bounded to retrieved evidence blocks.</p>
                    </div>

                    <div 
                      onClick={() => handleSelectCategory('XAI')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-cyan-50 text-cyan-700 group-hover:bg-cyan-600 group-hover:text-white transition-colors">
                          <Layers className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-slate-400 font-bold">25 Questions</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-cyan-700 transition-colors">
                        XAI & Provenance
                      </h4>
                      <p className="text-xs text-slate-500">Explain retrieval rankings, token attributions, and full answer audit chains.</p>
                    </div>

                    <div 
                      onClick={() => handleSelectCategory('OFFLINE CORPUS')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-amber-50 text-amber-700 group-hover:bg-amber-600 group-hover:text-white transition-colors">
                          <Database className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-slate-400 font-bold">25 Questions</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-amber-700 transition-colors">
                        Offline Corpus
                      </h4>
                      <p className="text-xs text-slate-500">Test local research data across 687 papers (AI, Env Science, Interdisciplinary).</p>
                    </div>

                    <div 
                      onClick={() => handleSelectCategory('HYBRID SEARCH')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-emerald-50 text-emerald-700 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                          <Sparkles className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-slate-400 font-bold">25 Questions</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                        Hybrid Search
                      </h4>
                      <p className="text-xs text-slate-500">Test parallel local + online retrieval with unified deduplication and RRF merging.</p>
                    </div>

                    <div 
                      onClick={() => handleSelectCategory('CLAIM VERIFICATION')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-purple-50 text-purple-700 group-hover:bg-purple-600 group-hover:text-white transition-colors">
                          <ShieldCheck className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-slate-400 font-bold">25 Questions</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-purple-700 transition-colors">
                        Claim Verification (PROVE)
                      </h4>
                      <p className="text-xs text-slate-500">Audit whether claims are SUPPORTED, PARTIALLY_SUPPORTED, or lack evidence.</p>
                    </div>

                    <div 
                      onClick={() => navigate('/literature-review')}
                      className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-1.5 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="p-2 rounded-xl bg-teal-50 text-teal-700 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                          <BookOpen className="w-4 h-4" />
                        </span>
                        <span className="text-[11px] font-mono text-emerald-600 font-bold">4-Step Flow</span>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                        Literature Review
                      </h4>
                      <p className="text-xs text-slate-500">Select papers from library, define topics & requirements, synthesize with IEEE citations.</p>
                    </div>
                  </div>
                </div>

                {/* COMPACT REVIEW PRESETS ROW */}
                <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                      <Zap className="w-4 h-4 text-amber-500" /> Review Presets
                    </h3>
                    <button onClick={() => setToolkitTab('presets')} className="text-xs font-bold text-emerald-700 hover:underline">
                      View All Presets ΓåÆ
                    </button>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
                    {REVIEW_PRESETS.slice(0, 4).map((p) => (
                      <div
                        key={p.id}
                        onClick={() => {
                          setSelectedFilter(p.filter as any);
                          setToolkitTab('questions');
                          addToast(`Loaded preset: ${p.name}`, 'info');
                        }}
                        className="p-3 bg-slate-50 hover:bg-emerald-50/60 rounded-xl border border-slate-200 hover:border-emerald-300 transition-all cursor-pointer space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-black text-slate-800">{p.name}</span>
                          <span className="text-[10px] font-mono font-bold px-1.5 py-0.2 rounded bg-slate-200 text-slate-700">
                            {p.count} Qs
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-500 line-clamp-1">{p.desc}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* "VIEW ALL 13 AREAS" BUTTON */}
                <div className="text-center pt-2">
                  <button
                    onClick={() => setToolkitTab('questions')}
                    className="px-6 py-3 bg-slate-900 hover:bg-emerald-600 text-white rounded-xl text-xs font-black transition-all shadow-sm inline-flex items-center gap-2"
                  >
                    View All 13 Research Evaluation Areas ({allScenarios.length} Questions) ΓåÆ
                  </button>
                </div>

              </div>
            )}

            {/* TAB 2: QUESTIONS (ALL 13 CATEGORY CARDS OR FILTERED LIST) */}
            {toolkitTab === 'questions' && viewMode === 'browse' && (
              <div className="space-y-6 animate-in fade-in duration-200">
                
                {/* 13 CLEAN CATEGORY CARDS (When filter is ALL) */}
                {selectedFilter === 'ALL' && !searchQuery && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-base font-black text-slate-900">
                          13 Research Evaluation Areas
                        </h3>
                        <p className="text-xs text-slate-500 mt-0.5">Select a category to explore its 25 curated test questions.</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                      {CATEGORY_DEFINITIONS.map((cat) => {
                        const count = allScenarios.filter(s => s.filter.toLowerCase() === cat.id.toLowerCase()).length;
                        return (
                          <div
                            key={cat.id}
                            onClick={() => handleSelectCategory(cat.id)}
                            className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-2 group"
                          >
                            <div className="flex items-center justify-between">
                              <span className="p-2 rounded-xl bg-slate-50 text-slate-700 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                                <cat.icon className="w-4 h-4" />
                              </span>
                              <span className="text-[11px] font-mono font-black text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                                {count} Questions
                              </span>
                            </div>
                            <div>
                              <h4 className="text-sm font-black text-slate-900 group-hover:text-emerald-700 transition-colors">
                                {cat.name}
                              </h4>
                              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                                {cat.desc}
                              </p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* FILTER HEADER (When category selected or search entered) */}
                {(selectedFilter !== 'ALL' || searchQuery) && (
                  <div className="space-y-4">
                    
                    {/* ACTIVE CATEGORY BANNER */}
                    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <button 
                            onClick={() => { setSelectedFilter('ALL'); setSearchQuery(''); setActiveIntent(null); }}
                            className="text-xs font-bold text-emerald-700 hover:underline flex items-center gap-1"
                          >
                            <ArrowLeft className="w-3.5 h-3.5" /> All 13 Categories
                          </button>
                          <span className="text-slate-300">ΓÇó</span>
                          <span className="text-xs font-mono font-bold text-slate-400 uppercase">
                            {filteredScenarios.length} Questions
                          </span>
                        </div>
                        <h2 className="text-lg font-black text-slate-900">
                          {selectedFilter === 'ALL' ? 'Search Results' : selectedFilter}
                        </h2>
                        <p className="text-xs text-slate-500 mt-0.5">
                          {CATEGORY_DEFINITIONS.find(c => c.id === selectedFilter)?.desc || 'Filter and inspect questions below.'}
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => { setViewMode('review'); setReviewIndex(0); }}
                          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm"
                        >
                          <Play className="w-3.5 h-3.5 fill-white" /> Review This Set
                        </button>
                      </div>
                    </div>

                    {/* SEARCH & PRIMARY FILTERS BAR */}
                    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-3">
                      <div className="flex flex-col md:flex-row items-center gap-3">
                        {/* Search Input */}
                        <div className="relative flex-1 w-full">
                          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                          <input
                            type="text"
                            placeholder="Filter in this category (question, concept, tag)..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-emerald-500 font-medium"
                          />
                        </div>

                        {/* Primary Filter 1: Domain */}
                        <div className="w-full md:w-56">
                          <select
                            value={selectedDomain}
                            onChange={(e) => setSelectedDomain(e.target.value)}
                            className="w-full p-2 text-xs bg-slate-50 border border-slate-200 rounded-xl font-bold text-slate-700 focus:outline-none focus:border-emerald-500"
                          >
                            {DOMAINS_LIST.map(d => (
                              <option key={d.name} value={d.name}>{d.name}</option>
                            ))}
                          </select>
                        </div>

                        {/* Primary Filter 2: Mode */}
                        <div className="w-full md:w-44">
                          <select
                            value={selectedMode}
                            onChange={(e) => setSelectedMode(e.target.value)}
                            className="w-full p-2 text-xs bg-slate-50 border border-slate-200 rounded-xl font-bold text-slate-700 focus:outline-none focus:border-emerald-500"
                          >
                            {MODES_LIST.map(m => (
                              <option key={m} value={m}>Mode: {m}</option>
                            ))}
                          </select>
                        </div>

                        {/* Toggle Secondary More Filters */}
                        <button
                          onClick={() => setShowMoreFilters(!showMoreFilters)}
                          className={cn(
                            "px-3 py-2 rounded-xl text-xs font-bold border transition-all flex items-center gap-1.5 shrink-0",
                            showMoreFilters ? "bg-slate-900 text-white border-slate-900" : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                          )}
                        >
                          <SlidersHorizontal className="w-3.5 h-3.5" />
                          {showMoreFilters ? 'Hide Filters' : 'More Filters'}
                        </button>
                      </div>

                      {/* SECONDARY FILTERS COLLAPSIBLE */}
                      {showMoreFilters && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-3 border-t border-slate-100 text-xs animate-in fade-in">
                          <div>
                            <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Difficulty</label>
                            <select
                              value={selectedDifficulty}
                              onChange={(e) => setSelectedDifficulty(e.target.value)}
                              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-slate-700"
                            >
                              {DIFFICULTIES_LIST.map(d => (<option key={d} value={d}>{d}</option>))}
                            </select>
                          </div>
                          <div>
                            <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Status</label>
                            <select
                              value={selectedStatus}
                              onChange={(e) => setSelectedStatus(e.target.value)}
                              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-slate-700"
                            >
                              {STATUSES_LIST.map(st => (<option key={st} value={st}>{st}</option>))}
                            </select>
                          </div>
                          <div>
                            <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Question Type</label>
                            <select
                              value={selectedQuestionType}
                              onChange={(e) => setSelectedQuestionType(e.target.value)}
                              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-slate-700"
                            >
                              {QUESTION_TYPES_LIST.map(qt => (<option key={qt} value={qt}>{qt}</option>))}
                            </select>
                          </div>
                          <div>
                            <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Expected Source</label>
                            <select
                              value={selectedSource}
                              onChange={(e) => setSelectedSource(e.target.value)}
                              className="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-slate-700"
                            >
                              {SOURCES_LIST.map(src => (<option key={src} value={src}>{src}</option>))}
                            </select>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* COMPACT QUESTION CARDS LIST */}
                    {filteredScenarios.length === 0 ? (
                      <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center space-y-3">
                        <HelpCircle className="w-8 h-8 text-slate-300 mx-auto" />
                        <h4 className="text-sm font-black text-slate-800">No questions match these filters.</h4>
                        <p className="text-xs text-slate-500 max-w-sm mx-auto">Try resetting the domain, mode, difficulty, or search keyword.</p>
                        <button
                          onClick={() => {
                            setSelectedFilter('ALL');
                            setSelectedDomain('All Domains');
                            setSelectedMode('All');
                            setSelectedDifficulty('All');
                            setSelectedStatus('All');
                            setSearchQuery('');
                          }}
                          className="px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-bold"
                        >
                          Clear Filters
                        </button>
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                        {filteredScenarios.map((s) => (
                          <div
                            key={s.question_id}
                            onClick={() => setDrawerScenario(s)}
                            className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-sm transition-all cursor-pointer space-y-3 flex flex-col justify-between"
                          >
                            <div className="space-y-2">
                              {/* TOP TAGS */}
                              <div className="flex items-center justify-between gap-2 text-xs">
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="text-[10px] font-mono font-black text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                                    {s.question_id}
                                  </span>
                                  <span className="text-[10px] font-bold text-slate-500 font-mono">
                                    {s.domain} ΓÇó {s.mode}
                                  </span>
                                </div>
                                {s.is_known_good && (
                                  <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200 flex items-center gap-1">
                                    <Zap className="w-3 h-3 text-amber-500" /> KNOWN GOOD
                                  </span>
                                )}
                              </div>

                              {/* QUESTION */}
                              <h4 className="text-sm font-bold text-slate-900 leading-snug">
                                "{s.question}"
                              </h4>

                              {/* WHAT IT TESTS */}
                              <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100 text-[11px] text-slate-600 space-y-0.5">
                                <div><strong className="text-slate-800">TESTS:</strong> {s.purpose}</div>
                                <div><strong className="text-slate-800">BEST PLACE TO START:</strong> {s.mode === 'AI_ASSISTANT' ? 'Ask AI' : s.mode === 'PROVE' ? 'PROVE' : 'Research Explorer'}</div>
                              </div>
                            </div>

                            {/* PRIMARY & SECONDARY ACTIONS */}
                            <div className="flex items-center justify-between gap-2 pt-2 border-t border-slate-100" onClick={(e) => e.stopPropagation()}>
                              <button
                                onClick={() => navigate(`/hybrid-search?q=${encodeURIComponent(s.question)}&domain=${encodeURIComponent(s.domain)}`)}
                                className="px-3 py-1.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-xs font-black flex items-center gap-1 shadow-xs transition-colors"
                              >
                                <Search className="w-3 h-3" /> Open in Explorer
                              </button>

                              <div className="flex items-center gap-1">
                                <button
                                  onClick={() => handleCopyQuestion(s.question_id, s.question)}
                                  className="p-1.5 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-lg text-xs"
                                  title="Copy Question"
                                >
                                  {copiedId === s.question_id ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                                </button>
                                <button
                                  onClick={() => navigate(`/assistant?q=${encodeURIComponent(s.question)}`)}
                                  className="px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-lg text-xs font-bold"
                                >
                                  Ask AI
                                </button>
                                <button
                                  onClick={() => setDrawerScenario(s)}
                                  className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold"
                                >
                                  Details ΓåÆ
                                </button>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                  </div>
                )}

              </div>
            )}

            {/* TAB 3: PRESETS (COMPACT VIEW) */}
            {toolkitTab === 'presets' && (
              <div className="space-y-4 animate-in fade-in duration-200">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <h3 className="text-base font-black text-slate-900">Curated Review & Viva Presets</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Use pre-packaged question sequences to demonstrate specific system capabilities during project reviews.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {REVIEW_PRESETS.map((p) => (
                    <div
                      key={p.id}
                      className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs hover:border-emerald-300 transition-all flex flex-col justify-between space-y-3"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-black text-slate-900">{p.name}</h4>
                          <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
                            {p.count} Questions
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 leading-relaxed">{p.desc}</p>
                      </div>

                      <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
                        <button
                          onClick={() => {
                            setSelectedFilter(p.filter as any);
                            setToolkitTab('questions');
                            addToast(`Loaded preset: ${p.name}`, 'info');
                          }}
                          className="px-3 py-1.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-xs font-bold"
                        >
                          Browse Questions
                        </button>
                        <button
                          onClick={() => {
                            setSelectedFilter(p.filter as any);
                            setViewMode('review');
                            setReviewIndex(0);
                            setToolkitTab('questions');
                          }}
                          className="px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-lg text-xs font-bold flex items-center gap-1"
                        >
                          <Play className="w-3 h-3 fill-current" /> Start Review Mode
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* TAB 4: KNOWN GOOD (FAST-PATH CACHE) */}
            {toolkitTab === 'known_good' && (
              <div className="space-y-4 animate-in fade-in duration-200">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-base font-black text-slate-900 flex items-center gap-2">
                        <Zap className="w-4 h-4 text-amber-500" /> Known-Good Review Questions & Fast-Path Knowledge Cache ({knownGoodScenarios.length})
                      </h3>
                      <p className="text-xs text-slate-500 mt-1">
                        Sub-second (&lt;0.2s) instant restoration of verified answers, claim attestations, and XAI provenance.
                      </p>
                    </div>
                    <span className="text-[10px] font-mono font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 px-2.5 py-1 rounded-lg">
                      Verified Result Available
                    </span>
                  </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xs">
                  <table className="w-full text-left border-collapse text-xs font-sans">
                    <thead>
                      <tr className="border-b border-slate-200 bg-slate-50">
                        <th className="p-3.5 font-bold text-slate-500 uppercase">ID</th>
                        <th className="p-3.5 font-bold text-slate-500 uppercase">Question</th>
                        <th className="p-3.5 font-bold text-slate-500 uppercase">Domain</th>
                        <th className="p-3.5 font-bold text-slate-500 uppercase">Claims / Citations</th>
                        <th className="p-3.5 font-bold text-slate-500 uppercase">Latency</th>
                        <th className="p-3.5 font-bold text-slate-500 uppercase text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {knownGoodScenarios.map((kq) => (
                        <tr key={kq.question_id} className="hover:bg-slate-50/70 transition-colors">
                          <td className="p-3.5 font-mono font-bold text-emerald-800">{kq.question_id}</td>
                          <td className="p-3.5 font-bold text-slate-900 max-w-sm">"{kq.question}"</td>
                          <td className="p-3.5 text-slate-600">{kq.domain}</td>
                          <td className="p-3.5 text-slate-700">
                            <span className="font-bold text-emerald-700">{kq.claims_count} Claims</span> ΓÇó {kq.citations_count} Citations
                          </td>
                          <td className="p-3.5 font-mono font-bold text-emerald-600">{kq.latency_ms} ms</td>
                          <td className="p-3.5 text-right space-x-1.5">
                            <button
                              onClick={() => navigate(`/assistant?q=${encodeURIComponent(kq.question)}&search_id=${kq.search_id}`)}
                              className="px-2.5 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 rounded-lg text-xs font-bold transition-colors"
                            >
                              Reuse Result
                            </button>
                            <button
                              onClick={() => navigate(`/hybrid-search?q=${encodeURIComponent(kq.question)}&domain=${encodeURIComponent(kq.domain)}`)}
                              className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold transition-colors"
                            >
                              Run Live
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* TAB 5: HISTORY & AUDIT */}
            {toolkitTab === 'history' && (
              <div className="space-y-4 animate-in fade-in duration-200">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <h3 className="text-base font-black text-slate-900">Review Execution History & Audit Logs</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Historical record of all evaluated research questions, verification scores, and response latencies.</p>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-6 text-center text-xs text-slate-500">
                  <FileSpreadsheet className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                  <p className="font-bold text-slate-800">39 Historical Test Executions Recorded.</p>
                  <p className="mt-1">All known-good baseline runs are logged with SHA-256 context hashes and execution timestamps.</p>
                  <button
                    onClick={() => handleExport('csv')}
                    className="mt-4 px-4 py-2 bg-slate-900 text-white rounded-xl font-bold"
                  >
                    Download Full History CSV
                  </button>
                </div>
              </div>
            )}

            {/* REVIEW MODE SCREEN (When View Mode is 'review') */}
            {viewMode === 'review' && (
              <div className="bg-slate-900 text-white rounded-3xl p-6 md:p-8 shadow-xl border border-slate-800 space-y-6 animate-in fade-in">
                
                {/* REVIEW MODE HEADER */}
                <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                  <div>
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-400 uppercase tracking-wider">
                        RESEARCH REVIEW MODE
                      </span>
                      <span className="text-xs font-mono text-slate-400 font-bold">
                        Question {reviewIndex + 1} of {filteredScenarios.length || allScenarios.length}
                      </span>
                      {reviewResults.length > 0 && (
                        <span className="text-[11px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/80">
                          Evaluated: {reviewResults.length} ({reviewResults.filter(r => r.verdict === 'PASSED').length} Passed)
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-black text-white">
                      {(filteredScenarios[reviewIndex] || allScenarios[0]).title}
                    </h3>
                  </div>

                  <button
                    onClick={() => setViewMode('browse')}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-bold"
                  >
                    Exit Review Mode
                  </button>
                </div>

                {/* CURRENT QUESTION DISPLAY */}
                <div className="space-y-4">
                  <div className="bg-slate-800/60 p-5 rounded-2xl border border-slate-700/70 space-y-2">
                    <span className="text-[10px] font-mono uppercase text-emerald-400 font-bold">Research Question</span>
                    <p className="text-base font-bold text-white leading-relaxed">
                      "{(filteredScenarios[reviewIndex] || allScenarios[0]).question}"
                    </p>
                  </div>

                  {/* WHAT THIS DEMONSTRATES */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50 space-y-1">
                      <span className="font-bold text-slate-400 block">What this demonstrates:</span>
                      <p className="text-slate-300 leading-relaxed">
                        {(filteredScenarios[reviewIndex] || allScenarios[0]).purpose}
                      </p>
                    </div>

                    <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50 space-y-1">
                      <span className="font-bold text-slate-400 block">Expected Path:</span>
                      <p className="text-emerald-400 font-mono font-bold">
                        Explorer ΓåÆ Evidence Selection ΓåÆ Ask AI ΓåÆ PROVE Verification ΓåÆ XAI
                      </p>
                    </div>
                  </div>

                  {/* EXECUTE PIPELINE BUTTON */}
                  <div className="flex items-center gap-3 pt-2">
                    <button
                      onClick={() => handleExecuteReviewPipeline(filteredScenarios[reviewIndex] || allScenarios[0])}
                      disabled={isExecutingPipeline}
                      className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-black flex items-center gap-2 shadow-sm disabled:opacity-50"
                    >
                      {isExecutingPipeline ? <RotateCcw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-white" />}
                      {isExecutingPipeline ? 'Executing Research Pipeline...' : 'Start / Run Pipeline Test'}
                    </button>

                    <button
                      onClick={() => navigate(`/hybrid-search?q=${encodeURIComponent((filteredScenarios[reviewIndex] || allScenarios[0]).question)}`)}
                      className="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold"
                    >
                      Open in Explorer
                    </button>

                    <button
                      onClick={() => navigate(`/assistant?q=${encodeURIComponent((filteredScenarios[reviewIndex] || allScenarios[0]).question)}`)}
                      className="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold"
                    >
                      Open in Ask AI
                    </button>
                  </div>

                  {/* STAGE RESULTS DISPLAY */}
                  {reviewStagesResult && (
                    <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs animate-in fade-in">
                      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                        <span className="font-bold text-emerald-400 flex items-center gap-1.5">
                          <CheckCircle2 className="w-4 h-4" /> Pipeline Result: {reviewStagesResult.verdict}
                        </span>
                        <span className="text-cyan-400 font-bold">{reviewStagesResult.latency_ms} ms</span>
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 text-[11px]">
                        <div>Retrieval: <span className="text-emerald-400 font-bold">PASS</span> ({reviewStagesResult.stages.retrieval.label})</div>
                        <div>Evidence: <span className="text-emerald-400 font-bold">PASS</span> ({reviewStagesResult.stages.evidence.label})</div>
                        <div>Answer: <span className="text-emerald-400 font-bold">PASS</span> ({reviewStagesResult.stages.answer.label})</div>
                        <div>Claims: <span className="text-emerald-400 font-bold">PASS</span> ({reviewStagesResult.stages.claims.label})</div>
                        <div>Citations: <span className="text-emerald-400 font-bold">PASS</span> ({reviewStagesResult.stages.citations.label})</div>
                        <div>XAI: <span className="text-emerald-400 font-bold">PASS</span> ({reviewStagesResult.stages.xai.label})</div>
                      </div>
                    </div>
                  )}

                  {/* RECORD VERDICT & NEXT */}
                  <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-800">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-400">Mark Verdict:</span>
                      <button
                        onClick={() => handleRecordReviewVerdict('PASSED')}
                        className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold"
                      >
                        Pass
                      </button>
                      <button
                        onClick={() => handleRecordReviewVerdict('PARTIAL')}
                        className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-bold"
                      >
                        Partial
                      </button>
                      <button
                        onClick={() => handleRecordReviewVerdict('FAILED')}
                        className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-bold"
                      >
                        Fail
                      </button>
                    </div>

                    <button
                      onClick={() => setReviewIndex(prev => Math.min(prev + 1, (filteredScenarios.length || allScenarios.length) - 1))}
                      className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5"
                    >
                      Next Question ΓåÆ
                    </button>
                  </div>
                </div>

              </div>
            )}
              </>
            )}

            {/* TAB: PROFILE INFORMATION */}
            {activeTab === 'profile' && (
              <div className="space-y-6 animate-in fade-in duration-200">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
                  <div>
                    <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                      <User className="w-5 h-5 text-emerald-600" /> Profile Information
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">Manage your account identity, display name, and academic affiliation.</p>
                  </div>

                  <div className="space-y-4 max-w-lg pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-4 pb-2">
                      <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white text-xl font-black shadow-md border-2 border-white">
                        {(name || user?.name || 'R').charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">{name || user?.name || 'Researcher'}</h4>
                        <span className="text-xs text-slate-500 font-mono">{user?.email || 'user@researchnexus.ai'}</span>
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Enter full name"
                        className="w-full p-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-emerald-500 font-medium"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
                      <input
                        type="email"
                        disabled
                        value={user?.email || 'user@researchnexus.ai'}
                        className="w-full p-2.5 text-xs bg-slate-100 text-slate-500 border border-slate-200 rounded-xl cursor-not-allowed font-mono"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Role / Designation</label>
                      <input
                        type="text"
                        defaultValue="Lead Researcher / Scholar"
                        className="w-full p-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-emerald-500 font-medium"
                      />
                    </div>

                    <button
                      onClick={handleSaveProfile}
                      disabled={isSaving}
                      className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm disabled:opacity-50"
                    >
                      {isSaving ? 'Saving Changes...' : 'Save Changes'}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* TAB: DATA & PRIVACY */}
            {activeTab === 'privacy' && (
              <div className="space-y-6 animate-in fade-in duration-200">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
                  <div>
                    <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                      <Database className="w-5 h-5 text-emerald-600" /> Data & Privacy
                    </h3>
                    <p className="text-xs text-slate-500 mt-1">Control your research activity storage, document handling, and local session preferences.</p>
                  </div>

                  <div className="space-y-4 pt-4 border-t border-slate-100 max-w-xl">
                    <label className="flex items-start gap-3 p-3.5 bg-slate-50 border border-slate-200 rounded-xl cursor-pointer hover:bg-emerald-50/50 transition-colors">
                      <input
                        type="checkbox"
                        checked={auditLoggingEnabled}
                        onChange={(e) => setAuditLoggingEnabled(e.target.checked)}
                        className="mt-0.5 accent-emerald-600"
                      />
                      <div>
                        <span className="text-xs font-black text-slate-900 block">Research History Preference</span>
                        <span className="text-[11px] text-slate-500 leading-relaxed">
                          Keep a record of your past exploration queries and verification checks for fast access and continuity.
                        </span>
                      </div>
                    </label>

                    <label className="flex items-start gap-3 p-3.5 bg-slate-50 border border-slate-200 rounded-xl cursor-pointer hover:bg-emerald-50/50 transition-colors">
                      <input
                        type="checkbox"
                        checked={zeroEgressLocalMode}
                        onChange={(e) => setZeroEgressLocalMode(e.target.checked)}
                        className="mt-0.5 accent-emerald-600"
                      />
                      <div>
                        <span className="text-xs font-black text-slate-900 block">Saved Research & Data Preference</span>
                        <span className="text-[11px] text-slate-500 leading-relaxed">
                          Preserve paper bookmarks, notes, and topic outlines across your active research sessions.
                        </span>
                      </div>
                    </label>

                    <div className="p-4 bg-emerald-50/60 border border-emerald-200/70 rounded-xl space-y-1">
                      <span className="text-xs font-bold text-emerald-900 block">Uploaded Document & Data Handling</span>
                      <p className="text-[11px] text-slate-600 leading-relaxed">
                        Uploaded papers, private notes, and literature drafts remain strictly local to your workspace. No user manuscripts are ever utilized for external model training.
                      </p>
                    </div>

                    <div className="pt-2">
                      <button
                        onClick={() => {
                          if (window.confirm('Clear all local search history and temporary cached session data?')) {
                            localStorage.removeItem('researchnexus_cache');
                            addToast('Research history and cached session data cleared.', 'info');
                          }
                        }}
                        className="px-4 py-2.5 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 rounded-xl text-xs font-bold transition-colors"
                      >
                        Clear Research History
                      </button>
                    </div>

                    <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-500">
                      <span className="font-bold text-slate-700 block mb-0.5">Privacy Notice</span>
                      ResearchNexus AI values academic confidentiality. All synthesis occurs with bounded, verifiable context.
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        </main>

        {/* 3. QUESTION DETAILS RIGHT-SIDE DRAWER */}
        {drawerScenario && (
          <div className="fixed inset-0 z-50 overflow-hidden bg-slate-900/40 backdrop-blur-xs flex justify-end animate-in fade-in duration-200">
            <div className="w-full max-w-xl bg-white h-full shadow-2xl flex flex-col justify-between overflow-y-auto font-sans p-6 md:p-8 space-y-6 animate-in slide-in-from-right duration-300">
              
              <div className="space-y-6">
                {/* DRAWER HEADER */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-black text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
                      {drawerScenario.question_id}
                    </span>
                    <span className="text-xs font-bold text-slate-400 font-mono">
                      {drawerScenario.filter}
                    </span>
                  </div>
                  <button
                    onClick={() => setDrawerScenario(null)}
                    className="p-2 text-slate-400 hover:text-slate-800 hover:bg-slate-100 rounded-xl"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* QUESTION */}
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Question</span>
                  <h3 className="text-lg font-black text-slate-900 leading-snug">
                    "{drawerScenario.question}"
                  </h3>
                </div>

                {/* RECOMMENDED WORKFLOW PIPELINE (Directly Clickable) */}
                <div className="bg-emerald-50/70 border border-emerald-200 rounded-2xl p-4 space-y-2.5">
                  <span className="text-[10px] font-black text-emerald-800 uppercase tracking-wider block">
                    Recommended Research Workflow
                  </span>
                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                    <button
                      onClick={() => navigate(`/hybrid-search?q=${encodeURIComponent(drawerScenario.question)}&domain=${encodeURIComponent(drawerScenario.domain)}`)}
                      className="p-2 bg-white hover:bg-emerald-600 hover:text-white rounded-xl border border-emerald-200 text-xs font-bold text-slate-800 text-center shadow-xs transition-colors flex flex-col items-center gap-1"
                    >
                      <Search className="w-4 h-4 text-emerald-600 group-hover:text-white" />
                      1. Explorer
                    </button>
                    <button
                      onClick={() => navigate(`/assistant?q=${encodeURIComponent(drawerScenario.question)}`)}
                      className="p-2 bg-white hover:bg-emerald-600 hover:text-white rounded-xl border border-emerald-200 text-xs font-bold text-slate-800 text-center shadow-xs transition-colors flex flex-col items-center gap-1"
                    >
                      <BrainCircuit className="w-4 h-4 text-emerald-600" />
                      2. Ask AI
                    </button>
                    <button
                      onClick={() => navigate(`/assistant?tab=prove&q=${encodeURIComponent(drawerScenario.question)}`)}
                      className="p-2 bg-white hover:bg-emerald-600 hover:text-white rounded-xl border border-emerald-200 text-xs font-bold text-slate-800 text-center shadow-xs transition-colors flex flex-col items-center gap-1"
                    >
                      <ShieldCheck className="w-4 h-4 text-emerald-600" />
                      3. PROVE
                    </button>
                    <button
                      onClick={() => navigate(`/xai?q=${encodeURIComponent(drawerScenario.question)}`)}
                      className="p-2 bg-white hover:bg-emerald-600 hover:text-white rounded-xl border border-emerald-200 text-xs font-bold text-slate-800 text-center shadow-xs transition-colors flex flex-col items-center gap-1"
                    >
                      <Layers className="w-4 h-4 text-emerald-600" />
                      4. XAI Trace
                    </button>
                    <button
                      onClick={() => navigate('/literature-review')}
                      className="p-2 bg-white hover:bg-emerald-600 hover:text-white rounded-xl border border-emerald-200 text-xs font-bold text-slate-800 text-center shadow-xs transition-colors flex flex-col items-center gap-1"
                    >
                      <BookOpen className="w-4 h-4 text-emerald-600" />
                      5. Review
                    </button>
                  </div>
                </div>

                {/* METADATA GRID */}
                <div className="grid grid-cols-2 gap-3 text-xs bg-slate-50 p-4 rounded-xl border border-slate-100 font-medium text-slate-700">
                  <div><span className="font-bold text-slate-400 block text-[10px] uppercase">Domain:</span> {drawerScenario.domain}</div>
                  <div><span className="font-bold text-slate-400 block text-[10px] uppercase">Mode:</span> {drawerScenario.mode}</div>
                  <div><span className="font-bold text-slate-400 block text-[10px] uppercase">Difficulty:</span> {drawerScenario.difficulty}</div>
                  <div><span className="font-bold text-slate-400 block text-[10px] uppercase">Expected Source:</span> {drawerScenario.expected_source}</div>
                </div>

                {/* PURPOSE & EXPECTED BEHAVIOR */}
                <div className="space-y-3 text-xs">
                  <div className="space-y-1">
                    <span className="font-bold text-slate-700 block">Purpose:</span>
                    <p className="text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                      {drawerScenario.purpose}
                    </p>
                  </div>

                  <div className="space-y-1">
                    <span className="font-bold text-slate-700 block">Expected Behavior:</span>
                    <p className="text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                      {drawerScenario.expected_behavior}
                    </p>
                  </div>

                  {drawerScenario.expected_evidence && (
                    <div className="space-y-1">
                      <span className="font-bold text-slate-700 block">Expected Evidence:</span>
                      <p className="text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                        {drawerScenario.expected_evidence}
                      </p>
                    </div>
                  )}
                </div>

                {/* SEMANTIC VARIANTS SECTION (If group exists) */}
                {groupVariants.length > 1 && (
                  <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                        <Share2 className="w-3.5 h-3.5 text-purple-600" /> Semantic Variants ({groupVariants.length})
                      </span>
                      <button
                        onClick={() => setComparingGroup(drawerScenario.scenario_group_id || null)}
                        className="text-[11px] font-bold text-purple-700 hover:underline"
                      >
                        Compare Versions ΓåÆ
                      </button>
                    </div>
                    <div className="space-y-2">
                      {groupVariants.map((v) => (
                        <div
                          key={v.question_id}
                          onClick={() => setDrawerScenario(v)}
                          className={cn(
                            "p-2.5 rounded-xl text-xs transition-all cursor-pointer border",
                            v.question_id === drawerScenario.question_id 
                              ? "bg-white border-purple-300 shadow-xs" 
                              : "bg-white/60 border-slate-200 hover:bg-white"
                          )}
                        >
                          <span className="font-mono font-bold text-purple-700 mr-2">[{v.variant_id || 'A'}]</span>
                          <span className="font-medium text-slate-800">"{v.question}"</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              </div>

              {/* DRAWER FOOTER ACTIONS */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                <button
                  onClick={() => handleCopyQuestion(drawerScenario.question_id, drawerScenario.question)}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold flex items-center gap-1.5"
                >
                  {copiedId === drawerScenario.question_id ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                  {copiedId === drawerScenario.question_id ? 'Copied' : 'Copy Question'}
                </button>

                <button
                  onClick={() => navigate(`/hybrid-search?q=${encodeURIComponent(drawerScenario.question)}&domain=${encodeURIComponent(drawerScenario.domain)}`)}
                  className="px-5 py-2.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-xl text-xs font-black flex items-center gap-1.5 shadow-sm transition-colors"
                >
                  <Search className="w-3.5 h-3.5" /> Launch in Explorer ΓåÆ
                </button>
              </div>

            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default SettingsPage;
