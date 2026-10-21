import fs from 'fs';

const filePath = 'src/pages/SettingsPage.tsx';
let code = fs.readFileSync(filePath, 'utf8');

// 1. Update SETTINGS_TABS
const targetTabs = `const SETTINGS_TABS = [
  { id: 'toolkit', label: 'Research Review Toolkit', icon: Compass },
  { id: 'profile', label: 'Profile Information', icon: User },
  { id: 'security', label: 'Security', icon: Shield },
  { id: 'privacy', label: 'Data & Privacy', icon: Database },
] as const;`;

const replacementTabs = `const SETTINGS_TABS = [
  { id: 'general', label: 'General & Profile', icon: User },
  { id: 'toolkit', label: 'Research Review Toolkit', icon: Compass },
  { id: 'security', label: 'Security & Access', icon: Shield },
  { id: 'privacy', label: 'Data & Privacy', icon: Database },
] as const;`;

if (!code.includes(targetTabs)) {
  console.error('targetTabs not found');
  process.exit(1);
}
code = code.replace(targetTabs, replacementTabs);

// 2. Active Tab initial state & scenarioSet state
const targetState = `  // Settings master navigation
  const [activeTab, setActiveTab] = useState<string>('toolkit');
  const [showMobileNav, setShowMobileNav] = useState(false);

  // Toolkit 5 Top-Level Navigation Tabs
  const [toolkitTab, setToolkitTab] = useState<'overview' | 'questions' | 'presets' | 'known_good' | 'history'>('overview');`;

const replacementState = `  // Settings master navigation: default to 'general' settings page with prominent Toolkit card
  const [activeTab, setActiveTab] = useState<string>('general');
  const [showMobileNav, setShowMobileNav] = useState(false);

  // 3 Canonical Review Sets
  // set1: Daily Research Check (12 deterministic daily scenarios, default)
  // set2: Deep System Review (Full 325+ bank across all 13 categories)
  // set3: Stress & Edge Case Review (45 adversarial and edge boundary failure tests)
  const [scenarioSet, setScenarioSet] = useState<'set1' | 'set2' | 'set3'>('set1');

  // Toolkit 5 Top-Level Navigation Tabs
  const [toolkitTab, setToolkitTab] = useState<'overview' | 'questions' | 'presets' | 'known_good' | 'history'>('overview');`;

if (!code.includes(targetState)) {
  console.error('targetState not found');
  process.exit(1);
}
code = code.replace(targetState, replacementState);

// 3. Add deterministic daily scenarios memo and stress scenarios memo right after allScenarios
const targetScenarios = `  // Raw dataset
  const allScenarios: Scenario[] = useMemo(() => {
    return (toolkitJson.scenarios || []) as Scenario[];
  }, []);`;

const replacementScenarios = `  // Raw dataset
  const allScenarios: Scenario[] = useMemo(() => {
    return (toolkitJson.scenarios || []) as Scenario[];
  }, []);

  // Set 1: Deterministic Daily 12 Selection based on current date (YYYY-MM-DD) + v2.0
  const dailyScenarios: Scenario[] = useMemo(() => {
    const today = new Date().toISOString().split('T')[0];
    let seed = 0;
    const seedStr = today + 'v2.0';
    for (let i = 0; i < seedStr.length; i++) {
      seed = (seed + seedStr.charCodeAt(i)) % 233280;
    }
    const pool = [...allScenarios];
    const picked: Scenario[] = [];
    for (let i = 0; i < 12 && pool.length > 0; i++) {
      seed = (seed * 9301 + 49297) % 233280;
      const idx = seed % pool.length;
      picked.push(pool.splice(idx, 1)[0]);
    }
    return picked;
  }, [allScenarios]);

  // Set 3: Stress & Edge Case Scenarios (Adversarial, LIMITATIONS, and zero valid evidence expected)
  const stressScenarios: Scenario[] = useMemo(() => {
    return allScenarios.filter(s => 
      s.difficulty === 'Adversarial' || 
      s.filter === 'LIMITATIONS' || 
      s.expected_source === 'NO_VALID_EVIDENCE_EXPECTED'
    );
  }, [allScenarios]);

  // Active bank based on chosen Scenario Set
  const activeBankScenarios: Scenario[] = useMemo(() => {
    if (scenarioSet === 'set1') return dailyScenarios;
    if (scenarioSet === 'set3') return stressScenarios;
    return allScenarios;
  }, [scenarioSet, dailyScenarios, stressScenarios, allScenarios]);`;

if (!code.includes(targetScenarios)) {
  console.error('targetScenarios not found');
  process.exit(1);
}
code = code.replace(targetScenarios, replacementScenarios);

// 4. Update filteredScenarios to filter activeBankScenarios instead of allScenarios
const targetFilter = `  // Filtered dataset
  const filteredScenarios = useMemo(() => {
    return allScenarios.filter(s => {`;

const replacementFilter = `  // Filtered dataset bounded to the active scenario set
  const filteredScenarios = useMemo(() => {
    return activeBankScenarios.filter(s => {`;

if (!code.includes(targetFilter)) {
  console.error('targetFilter not found');
  process.exit(1);
}
code = code.replace(targetFilter, replacementFilter);

const targetFilterEnd = `  }, [allScenarios, selectedFilter, selectedDomain, selectedMode, selectedDifficulty, selectedStatus, selectedQuestionType, selectedSource, searchQuery]);`;
const replacementFilterEnd = `  }, [activeBankScenarios, selectedFilter, selectedDomain, selectedMode, selectedDifficulty, selectedStatus, selectedQuestionType, selectedSource, searchQuery]);`;

if (!code.includes(targetFilterEnd)) {
  console.error('targetFilterEnd not found');
  process.exit(1);
}
code = code.replace(targetFilterEnd, replacementFilterEnd);

// 5. Wrap the toolkit header and content so that when activeTab === 'toolkit', toolkit renders; when activeTab !== 'toolkit', the clean settings layout with the dedicated entry card renders!
const targetHeader = `      {/* 1. TOP-LEVEL TOOLKIT HEADER */}
      <header className="px-6 py-5 md:px-10 md:py-6 bg-white border-b border-slate-100 shrink-0">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[11px] font-bold text-slate-400 hover:text-slate-600 flex items-center gap-1 cursor-pointer" onClick={() => navigate('/settings')}>
                <ArrowLeft className="w-3.5 h-3.5" /> Settings
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
              Prepare questions, test the research workflow, and trace results.
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

        {/* 5 TOP-LEVEL TABS */}
        <div className="flex items-center gap-1 mt-5 border-b border-slate-100 -mb-5 pb-px overflow-x-auto text-xs font-bold">
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
      </header>`;

const replacementHeader = `      {/* 1. TOP-LEVEL HEADER */}
      {activeTab === 'toolkit' ? (
        <header className="px-6 py-5 md:px-10 md:py-6 bg-white border-b border-slate-100 shrink-0">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <button 
                  onClick={() => setActiveTab('general')}
                  className="text-[11px] font-bold text-slate-400 hover:text-slate-600 flex items-center gap-1 cursor-pointer transition-colors"
                >
                  <ArrowLeft className="w-3.5 h-3.5" /> Settings
                </button>
                <span className="text-slate-300">•</span>
                <span className="text-xs font-black text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  RESEARCH REVIEW TOOLKIT
                </span>
                <span className="text-xs font-mono text-slate-400 font-bold">
                  v2.0 • {activeBankScenarios.length} Scenarios
                </span>
              </div>
              <h1 className="text-xl md:text-2xl font-black text-slate-900 tracking-tight flex items-center gap-2.5">
                <Compass className="w-6 h-6 text-emerald-600" />
                Research Review Toolkit
              </h1>
              <p className="text-xs font-medium text-slate-500 mt-0.5">
                Validate retrieval, RAG, citations, verification, XAI, comparison, domains and end-to-end research workflows.
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

          {/* 3 CANONICAL SCENARIO SET SELECTORS */}
          <div className="mt-5 pt-4 border-t border-slate-100 grid grid-cols-1 md:grid-cols-3 gap-2.5">
            {/* SET 1: DAILY RESEARCH CHECK */}
            <div 
              onClick={() => { setScenarioSet('set1'); setToolkitTab('questions'); }}
              className={cn(
                "p-3 rounded-xl border cursor-pointer transition-all flex flex-col justify-between",
                scenarioSet === 'set1'
                  ? "bg-emerald-50/70 border-emerald-400 shadow-xs ring-1 ring-emerald-400/20"
                  : "bg-slate-50/60 border-slate-200 hover:bg-white hover:border-slate-300"
              )}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span className="text-xs font-black text-slate-900">SET 1: DAILY RESEARCH CHECK</span>
                </div>
                <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-100/70 text-emerald-800">
                  12 Scenarios
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mb-2">
                Deterministic daily health check ({new Date().toISOString().split('T')[0]}). Progress: {reviewResults.length}/12
              </p>
              <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                <div 
                  className="bg-emerald-600 h-full transition-all duration-300"
                  style={{ width: \`\${Math.min(100, (reviewResults.length / 12) * 100)}%\` }}
                />
              </div>
            </div>

            {/* SET 2: DEEP SYSTEM REVIEW */}
            <div 
              onClick={() => { setScenarioSet('set2'); setToolkitTab('questions'); }}
              className={cn(
                "p-3 rounded-xl border cursor-pointer transition-all flex flex-col justify-between",
                scenarioSet === 'set2'
                  ? "bg-blue-50/70 border-blue-400 shadow-xs ring-1 ring-blue-400/20"
                  : "bg-slate-50/60 border-slate-200 hover:bg-white hover:border-slate-300"
              )}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                  <span className="text-xs font-black text-slate-900">SET 2: DEEP SYSTEM REVIEW</span>
                </div>
                <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-blue-100/70 text-blue-800">
                  {allScenarios.length} Scenarios
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mb-2">
                Full comprehensive test bank covering all 13 canonical categories (25+ scenarios each).
              </p>
              <span className="text-[10px] font-bold text-blue-700">13 Canonical Categories Active</span>
            </div>

            {/* SET 3: STRESS & EDGE CASE REVIEW */}
            <div 
              onClick={() => { setScenarioSet('set3'); setToolkitTab('questions'); }}
              className={cn(
                "p-3 rounded-xl border cursor-pointer transition-all flex flex-col justify-between",
                scenarioSet === 'set3'
                  ? "bg-amber-50/70 border-amber-400 shadow-xs ring-1 ring-amber-400/20"
                  : "bg-slate-50/60 border-slate-200 hover:bg-white hover:border-slate-300"
              )}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                  <span className="text-xs font-black text-slate-900">SET 3: STRESS & EDGE CASES</span>
                </div>
                <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-amber-100/70 text-amber-800">
                  {stressScenarios.length} Scenarios
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mb-2">
                Adversarial boundaries, zero evidence refusals, timeout recovery & provider errors.
              </p>
              <span className="text-[10px] font-bold text-amber-700">Safe Failure & Refusal Validation</span>
            </div>
          </div>

          {/* 5 TOP-LEVEL TABS */}
          <div className="flex items-center gap-1 mt-5 border-b border-slate-100 -mb-5 pb-px overflow-x-auto text-xs font-bold">
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
        </header>
      ) : (
        <header className="px-6 py-5 md:px-10 md:py-6 bg-white border-b border-slate-100 shrink-0 flex items-center justify-between">
          <div>
            <h1 className="text-xl md:text-2xl font-black text-slate-900 tracking-tight">System & Account Settings</h1>
            <p className="text-xs font-medium text-slate-500 mt-0.5">Manage preferences, security protocols, and review verification tools.</p>
          </div>
          <ThemeToggle compact={false} />
        </header>
      )}`;

if (!code.includes(targetHeader)) {
  console.error('targetHeader not found');
  process.exit(1);
}
code = code.replace(targetHeader, replacementHeader);

// 6. Update general settings rendering: add ENTRY CARD FOR RESEARCH REVIEW TOOLKIT + Profile, Security, Privacy
const targetProfile = `            {/* PROFILE, SECURITY, PRIVACY (Other settings tabs) */}
            {activeTab === 'profile' && (
              <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
                <div>
                  <h3 className="text-lg font-black text-slate-900">Profile Information</h3>
                  <p className="text-xs text-slate-500 mt-1">Update your account name and contact email.</p>
                </div>

                <div className="space-y-4 max-w-lg">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full p-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-emerald-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
                    <input
                      type="email"
                      disabled
                      value={user?.email || 'demo@researchnexus.ai'}
                      className="w-full p-2.5 text-xs bg-slate-100 text-slate-500 border border-slate-200 rounded-xl cursor-not-allowed"
                    />
                  </div>

                  <button
                    onClick={handleSaveProfile}
                    disabled={isSaving}
                    className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm disabled:opacity-50"
                  >
                    {isSaving ? 'Saving...' : 'Save Profile Changes'}
                  </button>
                </div>

                <div className="pt-6 border-t border-slate-100 max-w-lg">
                  <h4 className="text-sm font-black text-slate-800 mb-1 flex items-center gap-2">
                    <Palette className="w-4 h-4 text-emerald-600" /> Visual Environment & Eye Care
                  </h4>
                  <p className="text-xs text-slate-500 mb-3">Choose a comfortable reading aesthetic for your research sessions.</p>
                  <ThemeToggle compact={false} />
                </div>
              </div>
            )}`;

const replacementGeneral = `            {/* GENERAL TAB: PROFILE + PROMINENT RESEARCH REVIEW TOOLKIT ENTRY CARD */}
            {activeTab === 'general' && (
              <div className="space-y-6">
                {/* DEDICATED PROMINENT ENTRY CARD: RESEARCH REVIEW TOOLKIT */}
                <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-950 text-white rounded-3xl p-6 md:p-8 shadow-xl border border-emerald-900/40 relative overflow-hidden">
                  <div className="absolute right-0 top-0 translate-x-10 -translate-y-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
                  
                  <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <div className="space-y-2 max-w-2xl">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 uppercase tracking-wider">
                          SYSTEM VERIFICATION SUITE
                        </span>
                        <span className="text-xs font-mono text-slate-400">
                          v2.0 • 325+ Curated Scenarios
                        </span>
                      </div>
                      <h3 className="text-xl md:text-2xl font-black text-white tracking-tight flex items-center gap-2.5">
                        <Compass className="w-6 h-6 text-emerald-400" />
                        RESEARCH REVIEW TOOLKIT
                      </h3>
                      <p className="text-xs md:text-sm text-slate-300 leading-relaxed">
                        Validate retrieval, RAG, citations, verification, XAI, comparison, domains and end-to-end research workflows across 3 scenario sets (Daily Health Check, Deep 13-Category Review, and Stress Edge Cases).
                      </p>
                      <div className="flex items-center gap-4 text-xs font-mono text-emerald-300 pt-1">
                        <span>• 12 Daily Scenarios</span>
                        <span>• 325 Deep Review Bank</span>
                        <span>• 45 Adversarial Stress Tests</span>
                      </div>
                    </div>

                    <button
                      onClick={() => setActiveTab('toolkit')}
                      className="px-6 py-3.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-2xl text-xs font-black flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 transition-all shrink-0 cursor-pointer hover:scale-105"
                    >
                      <span>OPEN TOOLKIT →</span>
                    </button>
                  </div>
                </div>

                {/* PROFILE INFORMATION */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
                  <div>
                    <h3 className="text-lg font-black text-slate-900">Profile Information</h3>
                    <p className="text-xs text-slate-500 mt-1">Update your account name and contact email.</p>
                  </div>

                  <div className="space-y-4 max-w-lg">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full p-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-emerald-500"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
                      <input
                        type="email"
                        disabled
                        value={user?.email || 'demo@researchnexus.ai'}
                        className="w-full p-2.5 text-xs bg-slate-100 text-slate-500 border border-slate-200 rounded-xl cursor-not-allowed"
                      />
                    </div>

                    <button
                      onClick={handleSaveProfile}
                      disabled={isSaving}
                      className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm disabled:opacity-50"
                    >
                      {isSaving ? 'Saving...' : 'Save Profile Changes'}
                    </button>
                  </div>

                  <div className="pt-6 border-t border-slate-100 max-w-lg">
                    <h4 className="text-sm font-black text-slate-800 mb-1 flex items-center gap-2">
                      <Palette className="w-4 h-4 text-emerald-600" /> Visual Environment & Eye Care
                    </h4>
                    <p className="text-xs text-slate-500 mb-3">Choose a comfortable reading aesthetic for your research sessions.</p>
                    <ThemeToggle compact={false} />
                  </div>
                </div>
              </div>
            )}

            {/* SECURITY TAB */}
            {activeTab === 'security' && (
              <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
                <div>
                  <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                    <Shield className="w-5 h-5 text-emerald-600" /> Security & Access
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Manage authentication tokens, active sessions, and local cryptographic isolation.</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 space-y-2">
                  <p className="font-bold text-slate-800">Local Research Protection Enabled</p>
                  <p>All local papers, ChromaDB vector collections, and SQLite audit records are encrypted at rest with local user key isolation.</p>
                </div>
              </div>
            )}

            {/* PRIVACY TAB */}
            {activeTab === 'privacy' && (
              <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
                <div>
                  <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                    <Database className="w-5 h-5 text-emerald-600" /> Data & Privacy Controls
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Control telemetry, external API provider logging, and offline document confidentiality.</p>
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 space-y-2">
                  <p className="font-bold text-slate-800">Zero-Egress Strict Mode</p>
                  <p>When query mode is set to OFFLINE, no paper chunks or extraction prompts are transmitted outside this machine.</p>
                </div>
              </div>
            )}`;

if (!code.includes(targetProfile)) {
  console.error('targetProfile not found');
  process.exit(1);
}
code = code.replace(targetProfile, replacementGeneral);

// 7. Make sure toolkit content is only shown when activeTab === 'toolkit'
// We replace:
// {toolkitTab === 'overview' && viewMode === 'browse' && (
// with:
// {activeTab === 'toolkit' && toolkitTab === 'overview' && viewMode === 'browse' && (
code = code.replace("{toolkitTab === 'overview' && viewMode === 'browse' && (", "{activeTab === 'toolkit' && toolkitTab === 'overview' && viewMode === 'browse' && (");
code = code.replace("{toolkitTab === 'questions' && viewMode === 'browse' && (", "{activeTab === 'toolkit' && toolkitTab === 'questions' && viewMode === 'browse' && (");
code = code.replace("{toolkitTab === 'presets' && (", "{activeTab === 'toolkit' && toolkitTab === 'presets' && (");
code = code.replace("{toolkitTab === 'known_good' && (", "{activeTab === 'toolkit' && toolkitTab === 'known_good' && (");
code = code.replace("{toolkitTab === 'history' && (", "{activeTab === 'toolkit' && toolkitTab === 'history' && (");
code = code.replace("{viewMode === 'review' && (", "{activeTab === 'toolkit' && viewMode === 'review' && (");

// 8. Update DOMAINS_LIST display in questions dropdown to show (Offline) vs (Online)
code = code.replace(
  "{DOMAINS_LIST.map(d => (\n                              <option key={d.name} value={d.name}>{d.name}</option>\n                            ))}",
  "{DOMAINS_LIST.map(d => (\n                              <option key={d.name} value={d.name}>\n                                {d.name}{d.isOffline !== null ? (d.isOffline ? ' (Offline Corpus)' : ' (Online Research)') : ''}\n                              </option>\n                            ))}"
);

fs.writeFileSync(filePath, code, 'utf8');
console.log('Successfully updated SettingsPage.tsx with 3-set Research Review Toolkit and Settings landing card!');
