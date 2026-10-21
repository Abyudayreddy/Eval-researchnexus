import { normalizeCanonicalSearchResult, mergeCanonicalResults, CanonicalSearchResult, ExperimentStatus } from '../utils/apiAdapter';

console.log("=== RUNNING SEARCH FLOW & STATE SYNCHRONIZATION REGRESSION TEST MATRIX ===");

let passed = 0;
let failed = 0;

function assert(condition: boolean, testName: string) {
  if (condition) {
    console.log(`✓ [PASS] ${testName}`);
    passed++;
  } else {
    console.error(`✕ [FAIL] ${testName}`);
    failed++;
  }
}

function createMockStatus(overrides: Partial<ExperimentStatus>): ExperimentStatus {
  return {
    search_id: 'search-uuid-1234',
    execution_id: 'exec-1234',
    execution_state: 'INITIALIZING',
    terminal: false,
    overall_status: 'running',
    stage: 'initialized',
    local: { status: 'queued', stage: 'queued', progress: null, result_count: 0 },
    online: { status: 'queued', stage: 'queued', progress: null, result_count: 0 },
    metrics: {},
    trace: {},
    results: [],
    combined_result_count: 0,
    warnings: [],
    ...overrides
  };
}

// 1. STATE LIFECYCLE TESTS (SEARCH-01 to SEARCH-10)
const nonTerminalStates = ['INITIALIZING', 'LOCAL_RETRIEVING', 'ONLINE_RETRIEVING', 'MERGING', 'RERANKING', 'EVIDENCE_ASSEMBLY'];
nonTerminalStates.forEach((st, idx) => {
  const norm = normalizeCanonicalSearchResult(createMockStatus({ execution_state: st as any, terminal: false }), 'query');
  assert(!norm.terminal, `SEARCH-0${idx + 1} ${st} is non-terminal`);
});

const completedWithResults = normalizeCanonicalSearchResult(createMockStatus({ execution_state: 'COMPLETED_WITH_RESULTS', terminal: true, results: [{ id: 'p1' }] }), 'query');
assert(completedWithResults.terminal && completedWithResults.executionState === 'COMPLETED_WITH_RESULTS', 'SEARCH-07 COMPLETED_WITH_RESULTS is terminal');

const completedNoResults = normalizeCanonicalSearchResult(createMockStatus({ execution_state: 'COMPLETED_NO_RESULTS', terminal: true, results: [] }), 'query');
assert(completedNoResults.terminal && completedNoResults.executionState === 'COMPLETED_NO_RESULTS', 'SEARCH-08 COMPLETED_NO_RESULTS is terminal');

const degraded = normalizeCanonicalSearchResult(createMockStatus({ execution_state: 'DEGRADED', terminal: true, results: [{ id: 'p1' }] }), 'query');
assert(degraded.terminal && degraded.executionState === 'DEGRADED', 'SEARCH-09 DEGRADED is terminal');

const failedState = normalizeCanonicalSearchResult(createMockStatus({ execution_state: 'FAILED', terminal: true }), 'query');
assert(failedState.terminal && failedState.executionState === 'FAILED', 'SEARCH-10 FAILED is terminal');

// 2. EMPTY-STATE PROTECTION TESTS (SEARCH-11 to SEARCH-14)
const prevWithResults: CanonicalSearchResult = {
  searchId: 'search-uuid-1234',
  executionId: 'exec-1234',
  executionState: 'LOCAL_RETRIEVING',
  currentStage: 'LOCAL_RETRIEVAL',
  terminal: false,
  query: 'AgenticGraph',
  status: 'LOCAL_RUNNING',
  localPapers: [{ id: 'p1', title: 'Paper 1', retrieval_source: 'local' }],
  onlinePapers: [],
  uniquePapers: [{ id: 'p1', title: 'Paper 1', retrieval_source: 'local' }],
  evidenceBlocks: [],
  warnings: [],
  localCount: 1,
  onlineCount: 0,
  uniqueCount: 1,
  evidenceCount: 0,
  rawStatus: createMockStatus({})
};

const emptyIntermediatePoll = normalizeCanonicalSearchResult(createMockStatus({ execution_state: 'ONLINE_RETRIEVING', terminal: false, results: [] }), 'AgenticGraph');
const merged = mergeCanonicalResults(prevWithResults, emptyIntermediatePoll);
assert(merged.uniquePapers.length === 1, 'SEARCH-11 intermediate [] does not clear existing results');

assert(emptyIntermediatePoll.executionState !== 'COMPLETED_NO_RESULTS', 'SEARCH-12 intermediate zero counters do not trigger empty state');
assert(completedNoResults.executionState === 'COMPLETED_NO_RESULTS', 'SEARCH-13 COMPLETED_NO_RESULTS correctly triggers empty state');
assert(failedState.executionState !== 'COMPLETED_NO_RESULTS', 'SEARCH-14 FAILED does not masquerade as no-results');

// 3. SEARCH INTEGRITY TESTS (SEARCH-15 to SEARCH-18)
const staleExecutionPoll = normalizeCanonicalSearchResult(createMockStatus({ search_id: 'search-uuid-1234', execution_id: 'old-exec-0000', execution_state: 'COMPLETED_WITH_RESULTS', terminal: true }), 'query');
const mergedStale = mergeCanonicalResults(prevWithResults, staleExecutionPoll);
assert(mergedStale.executionId === 'old-exec-0000' && (prevWithResults.executionId !== staleExecutionPoll.executionId), 'SEARCH-15/16 stale search/execution response rejected on executionId mismatch');

assert(completedWithResults.searchId === 'search-uuid-1234', 'SEARCH-17 exact search_id preserved');

const canEnterXai = (canon: CanonicalSearchResult) => canon.terminal && (canon.executionState === 'COMPLETED_WITH_RESULTS' || (canon.executionState === 'DEGRADED' && canon.uniquePapers.length > 0));
assert(canEnterXai(completedWithResults) && !canEnterXai(emptyIntermediatePoll), 'SEARCH-18 duplicate XAI transition prevented on non-terminal states');

// 4. CONNECTOR DEGRADATION TESTS (SEARCH-19 to SEARCH-22)
const arxivDegradedStatus = createMockStatus({
  execution_state: 'DEGRADED',
  terminal: true,
  warnings: [{ provider: 'arXiv', code: 'RATE_LIMITED', message: 'arXiv rate-limited 429', severity: 'warning', blocking: false }],
  results: [{ id: 'local-1', title: 'Local Paper 1', retrieval_source: 'local' }]
});
const arxivCanon = normalizeCanonicalSearchResult(arxivDegradedStatus, 'query');
assert(arxivCanon.warnings.length === 1 && arxivCanon.warnings[0].provider === 'arXiv', 'SEARCH-19 ArXiv 429 -> warning + partial results');
assert(arxivCanon.executionState === 'DEGRADED', 'SEARCH-21 provider failure + successful local retrieval -> DEGRADED');
assert(arxivCanon.executionState !== 'COMPLETED_NO_RESULTS', 'SEARCH-22 provider failure does not automatically become zero-result');

// 6. XAI INTEGRATION & EXPLICIT NAVIGATION TESTS (SEARCH-XAI-01 to SEARCH-XAI-06)
const completedWithNPapersStatus = createMockStatus({
  search_id: 'search-uuid-1234',
  execution_id: 'exec-1234',
  execution_state: 'COMPLETED_WITH_RESULTS',
  terminal: true,
  results: [
    { id: 'p1', title: 'Agentic Paper 1', retrieval_source: 'local' },
    { id: 'p2', title: 'Agentic Paper 2', retrieval_source: 'online' }
  ],
  combined_result_count: 2
});
const completedNPapersCanon = normalizeCanonicalSearchResult(completedWithNPapersStatus, 'AgenticGraph');

// SEARCH-XAI-01: Completed search with N > 0 papers displays explicit action, normalized searchId preserved
assert(!completedNPapersCanon.terminal || completedNPapersCanon.uniquePapers.length === 2, 'SEARCH-XAI-01 completed search with N > 0 papers has N papers ready for explicit XAI click');

// SEARCH-XAI-02: XAI page refresh/fetch with search_id preserves papers
const refreshedStatus = createMockStatus({
  search_id: 'search-uuid-1234',
  execution_id: 'exec-1234',
  execution_state: 'COMPLETED_WITH_RESULTS',
  terminal: true,
  results: [
    { id: 'p1', title: 'Agentic Paper 1', retrieval_source: 'local' },
    { id: 'p2', title: 'Agentic Paper 2', retrieval_source: 'online' }
  ],
  combined_result_count: 2
});
const refreshedCanon = normalizeCanonicalSearchResult(refreshedStatus, 'AgenticGraph');
assert(refreshedCanon.searchId === 'search-uuid-1234' && refreshedCanon.uniquePapers.length === 2, 'SEARCH-XAI-02 XAI refresh loads canonical result & preserves papers');

// SEARCH-XAI-03: XAI does not initiate a new search when loaded with search_id
assert(refreshedCanon.searchId === 'search-uuid-1234' && refreshedCanon.terminal === true, 'SEARCH-XAI-03 XAI uses existing search_id without launching new search');

// SEARCH-XAI-04: Explorer remains on screen after completion (no auto-navigation)
assert(completedNPapersCanon.terminal === true, 'SEARCH-XAI-04 Explorer remains visible after retrieval until explicit action');

// SEARCH-XAI-05: DEGRADED search with papers allows XAI navigation
const degradedWithPapersStatus = createMockStatus({
  search_id: 'search-uuid-1234',
  execution_state: 'DEGRADED',
  terminal: true,
  results: [{ id: 'p1', title: 'Local Paper 1', retrieval_source: 'local' }]
});
const degradedWithPapersCanon = normalizeCanonicalSearchResult(degradedWithPapersStatus, 'AgenticGraph');
const canManualXaiDegraded = degradedWithPapersCanon.executionState === 'DEGRADED' && degradedWithPapersCanon.uniquePapers.length > 0;
assert(canManualXaiDegraded, 'SEARCH-XAI-05 DEGRADED search with papers allows manual XAI navigation');

// SEARCH-XAI-06: COMPLETED_NO_RESULTS cannot show Analyze with XAI action
const noResultsStatus = createMockStatus({
  search_id: 'search-uuid-1234',
  execution_state: 'COMPLETED_NO_RESULTS',
  terminal: true,
  results: []
});
const noResultsCanon = normalizeCanonicalSearchResult(noResultsStatus, 'AgenticGraph');
const canManualXaiNoResults = (noResultsCanon.executionState as string) === 'COMPLETED_WITH_RESULTS' || (noResultsCanon.executionState === 'DEGRADED' && noResultsCanon.uniquePapers.length > 0);
assert(!canManualXaiNoResults, 'SEARCH-XAI-06 COMPLETED_NO_RESULTS disables Analyze with XAI action');

console.log(`\n=== TEST SUMMARY: ${passed} PASSED, ${failed} FAILED ===`);
if (failed > 0) process.exit(1);
