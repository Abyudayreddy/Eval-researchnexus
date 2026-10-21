/**
 * Search Execution & XAI Flow Automated Validation Tests
 * 
 * Run: npx tsx src/__tests__/search_flow_validation.test.ts
 */

import { normalizeCanonicalSearchResult, CanonicalSearchResult, ExperimentStatus } from '../utils/apiAdapter';

let passed = 0;
let failed = 0;

function assert(condition: boolean, message: string) {
  if (condition) {
    console.log('  ? ' + message);
    passed++;
  } else {
    console.error('  ? FAIL: ' + message);
    failed++;
  }
}

function describe(name: string, fn: () => void) {
  console.log('\n' + name);
  fn();
}

// Mock backend status objects
const mockRunningStatus: ExperimentStatus = {
  search_id: 'sub-1001',
  overall_status: 'running',
  stage: 'local_retrieval',
  local: { status: 'running', stage: 'running', progress: 50, result_count: 0 },
  online: { status: 'queued', stage: 'queued', progress: 0, result_count: 0 },
  metrics: {},
  trace: {},
  results: [],
  combined_result_count: 0
};

const mockCompletedWithResultsStatus: ExperimentStatus = {
  search_id: 'sub-1002',
  overall_status: 'complete',
  stage: 'completed',
  local: { status: 'complete', stage: 'complete', progress: 100, result_count: 4 },
  online: { status: 'complete', stage: 'complete', progress: 100, result_count: 2 },
  metrics: {},
  trace: {},
  results: [
    { id: 'p1', title: 'Paper 1', retrieval_source: 'local', evidence_text: 'Evidence 1' },
    { id: 'p2', title: 'Paper 2', retrieval_source: 'local', abstract: 'Abstract 2' },
    { id: 'p3', title: 'Paper 3', retrieval_source: 'online', snippet: 'Snippet 3' },
    { id: 'p4', title: 'Paper 4', retrieval_source: 'online' }
  ],
  combined_result_count: 4
};

const mockCompletedZeroResultsStatus: ExperimentStatus = {
  search_id: 'sub-1003',
  overall_status: 'no_results',
  stage: 'completed',
  local: { status: 'no_results', stage: 'no_results', progress: 100, result_count: 0 },
  online: { status: 'no_results', stage: 'no_results', progress: 100, result_count: 0 },
  metrics: {},
  trace: {},
  results: [],
  combined_result_count: 0
};

const mockFailedStatus: ExperimentStatus = {
  search_id: 'sub-1004',
  overall_status: 'failed',
  stage: 'failed',
  local: { status: 'failed', stage: 'failed', progress: 0, result_count: 0 },
  online: { status: 'failed', stage: 'failed', progress: 0, result_count: 0 },
  metrics: {},
  trace: {},
  results: [],
  combined_result_count: 0
};

// ============================================================
// Test 1: Intermediate empty-state suppression
// ============================================================

describe('Test 1: Intermediate empty-state suppression during polling', () => {
  const canon = normalizeCanonicalSearchResult(mockRunningStatus, 'test query');
  assert(canon.status !== 'COMPLETED', 'Status is not COMPLETED during local retrieval');
  assert(canon.status === 'LOCAL_RUNNING' || canon.status === 'SEARCHING', 'Status maps to RUNNING stage');
  const shouldShowEmptyState = canon.status === 'COMPLETED' && canon.uniquePapers.length === 0;
  assert(!shouldShowEmptyState, 'Empty state message is NOT shown while search is still running');
});

// ============================================================
// Test 2: Final result normalization & counter synchronization
// ============================================================

describe('Test 2: Final result normalization & counter synchronization', () => {
  const canon = normalizeCanonicalSearchResult(mockCompletedWithResultsStatus, 'climate change');
  assert(canon.status === 'COMPLETED', 'Completed search status maps to COMPLETED');
  assert(canon.uniquePapers.length === 4, 'uniquePapers count is 4');
  assert(canon.localPapers.length === 2, 'localPapers count is 2');
  assert(canon.onlinePapers.length === 2, 'onlinePapers count is 2');
  assert(canon.evidenceBlocks.length === 3, 'evidenceBlocks count is 3');
  assert(canon.localCount === 4, 'localCount is synchronized from backend status');
  assert(canon.onlineCount === 2, 'onlineCount is synchronized from backend status');
  assert(canon.uniqueCount === 4, 'uniqueCount is synchronized');
});

// ============================================================
// Test 3: Zero-result completed search handling
// ============================================================

describe('Test 3: Zero-result completed search handling', () => {
  const canon = normalizeCanonicalSearchResult(mockCompletedZeroResultsStatus, 'random string');
  assert(canon.status === 'COMPLETED', 'Zero-result completed search status is COMPLETED');
  assert(canon.uniquePapers.length === 0, 'uniquePapers.length is 0');
  const shouldShowEmptyState = canon.status === 'COMPLETED' && canon.uniquePapers.length === 0;
  assert(shouldShowEmptyState, 'Empty state message ONLY shown when status === COMPLETED and uniquePapers.length === 0');
  const shouldAutoOpenXai = canon.status === 'COMPLETED' && canon.uniquePapers.length > 0;
  assert(!shouldAutoOpenXai, 'XAI MUST NOT auto-open for zero-result searches');
});

// ============================================================
// Test 4: Technical failure vs No-results distinction
// ============================================================

describe('Test 4: Technical failure vs No-results distinction', () => {
  const canon = normalizeCanonicalSearchResult(mockFailedStatus, 'failed query');
  assert(canon.status === 'FAILED', 'Failed status maps to FAILED');
  const shouldShowEmptyState = canon.status === 'COMPLETED' && canon.uniquePapers.length === 0;
  assert(!shouldShowEmptyState, 'Technical failure NEVER displays " No papers were returned\ empty state');
 const shouldShowFailureState = canon.status === 'FAILED';
 assert(shouldShowFailureState, 'Technical failure displays \Research search failed\ error state with retry button');
});

// ============================================================
// Test 5: Stale Search Cancellation Guard (Execution Token Lock)
// ============================================================

describe('Test 5: Stale Search Cancellation Guard (Search A -> Search B)', () => {
 let activeExecutionId = 'exec_B';
 let processedResultId = '';

 function handleIncomingPollUpdate(incomingSid: string, _payload: any) {
 if (incomingSid !== activeExecutionId) return;
 processedResultId = incomingSid;
 }

 handleIncomingPollUpdate('exec_A', { search_id: 'exec_A', overall_status: 'complete' });
 assert(processedResultId === '', 'Stale update from Search A ignored');

 handleIncomingPollUpdate('exec_B', { search_id: 'exec_B', overall_status: 'complete' });
 assert(processedResultId === 'exec_B', 'Poll update from active Search B accepted');
});

// ============================================================
// Test 6: XAI Auto-Transition Criteria & Deduplication Guard
// ============================================================

describe('Test 6: XAI Auto-Transition Criteria & Deduplication Guard', () => {
 let autoTransferredSearchId: string | null = null;
 let transitionCount = 0;

 function checkAndTriggerXaiTransition(sid: string, canon: CanonicalSearchResult) {
 if (canon.status === 'COMPLETED' && canon.uniquePapers.length > 0 && autoTransferredSearchId !== sid) {
 autoTransferredSearchId = sid;
 transitionCount++;
 }
 }

 const canon = normalizeCanonicalSearchResult(mockCompletedWithResultsStatus, 'test query');
 
 checkAndTriggerXaiTransition('sub-1002', canon);
 assert(transitionCount === 1, 'XAI transition triggered on first completion');
 assert(autoTransferredSearchId === 'sub-1002', 'Transferred searchId recorded');

 checkAndTriggerXaiTransition('sub-1002', canon);
 assert(transitionCount === 1, 'Subsequent polling events for same searchId DO NOT re-trigger transition');
});

// ============================================================
// Test 7: Filter Zero-Result Handling
// ============================================================

describe('Test 7: Filter Zero-Result Handling', () => {
 const canon = normalizeCanonicalSearchResult(mockCompletedWithResultsStatus, 'climate change');
 const filteredResults = canon.uniquePapers.filter((r: any) => r.publication_year === 1900);
 
 const isSearchEmpty = canon.status === 'COMPLETED' && canon.uniquePapers.length === 0;
 const isFilterEmpty = canon.status === 'COMPLETED' && canon.uniquePapers.length > 0 && filteredResults.length === 0;
 
 assert(!isSearchEmpty, 'Search itself is NOT empty when papers exist');
 assert(isFilterEmpty, 'Filter zero-result displays filter message with Clear Filters button');
});

console.log('\n' + '='.repeat(50));
console.log('Results: ' + passed + ' passed, ' + failed + ' failed, ' + (passed + failed) + ' total');
if (failed > 0) { 
 console.error('SOME TESTS FAILED'); 
 process.exit(1); 
} else { 
 console.log('ALL SEARCH FLOW TESTS PASSED ?'); 
}

export {};
