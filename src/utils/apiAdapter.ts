export type ExecutionState =
  | "INITIALIZING"
  | "LOCAL_RETRIEVING"
  | "ONLINE_RETRIEVING"
  | "MERGING"
  | "RERANKING"
  | "EVIDENCE_ASSEMBLY"
  | "COMPLETED_WITH_RESULTS"
  | "COMPLETED_NO_RESULTS"
  | "DEGRADED"
  | "FAILED";

export type PipelineStage =
  | "QUERY_PROCESSING"
  | "LOCAL_RETRIEVAL"
  | "RESULT_FUSION"
  | "BGE_RERANKING"
  | "ONLINE_RESEARCH"
  | "EVIDENCE_PREPARATION"
  | "RESULTS_READY";

export interface ProviderWarning {
  provider: string;
  code?: string;
  message: string;
  severity: "warning" | "error";
  blocking: boolean;
}

export interface ExperimentStage { 
  stage: string; 
  progress: number | null; 
} 

export interface ExperimentStatus { 
  search_id: string;
  execution_id?: string;
  execution_state?: ExecutionState;
  current_stage?: PipelineStage;
  stage_message?: string;
  terminal?: boolean;
  overall_status: string; 
  progress?: number;
  stage?: string;
  warnings?: ProviderWarning[];
  local: ExperimentStage & { status: string; trace?: any; result_count: number }; 
  online: ExperimentStage & { status: string; trace?: any; result_count: number }; 
  metrics: { local_metrics?: any; online_metrics?: any; combined_metrics?: any }; 
  trace: { local_trace?: any; online_trace?: any; combined_trace?: any };
  results?: any[]; 
  combined_result_count: number;
  providers?: Record<string, { status: string; count: number }>;
} 

export function createInitialExperimentStatus(searchId: string, executionId: string, query: string): ExperimentStatus {
  return {
    search_id: searchId,
    execution_id: executionId,
    execution_state: "INITIALIZING",
    current_stage: "QUERY_PROCESSING",
    stage_message: `Understanding "${query}"`,
    terminal: false,
    overall_status: "running",
    progress: 5,
    stage: "QUERY_PROCESSING",
    warnings: [],
    local: { status: "running", stage: "LOCAL_RETRIEVAL", progress: null, result_count: 0 },
    online: { status: "queued", stage: "ONLINE_RESEARCH", progress: null, result_count: 0 },
    metrics: {},
    trace: {},
    results: [],
    combined_result_count: 0
  };
} 

export function normalizeSearchResponse(raw: any) {
  return {
    search_id: raw.search_id,
    execution_id: raw.execution_id || `exec_${raw.search_id}`,
    execution_state: (raw.execution_state || 'INITIALIZING') as ExecutionState,
    terminal: Boolean(raw.terminal),
    overall_status: raw.overall_status || 'running'
  };
}

export function normalizeStatusResponse(raw: any): ExperimentStatus {
  const overall = raw.overall_status || 'running';
  const localStatus = raw.local_status || 'queued';
  const onlineStatus = raw.online_status || 'queued';
  const results = raw.results || raw.combined_results || [];

  let execState: ExecutionState = raw.execution_state;
  if (!execState) {
    if (['complete', 'completed'].includes(overall.toLowerCase())) {
      execState = results.length > 0 ? 'COMPLETED_WITH_RESULTS' : 'COMPLETED_NO_RESULTS';
    } else if (['failed', 'error'].includes(overall.toLowerCase())) {
      execState = 'FAILED';
    } else if (overall.toLowerCase() === 'partial') {
      execState = 'DEGRADED';
    } else {
      execState = 'INITIALIZING';
    }
  }

  const isTerminal = typeof raw.terminal === 'boolean'
    ? raw.terminal
    : ['COMPLETED_WITH_RESULTS', 'COMPLETED_NO_RESULTS', 'DEGRADED', 'FAILED'].includes(execState);

  let currentStage: PipelineStage = raw.current_stage;
  if (!currentStage) {
    if (isTerminal) {
      currentStage = "RESULTS_READY";
    } else if (execState === 'LOCAL_RETRIEVING') {
      currentStage = "LOCAL_RETRIEVAL";
    } else if (execState === 'MERGING') {
      currentStage = "RESULT_FUSION";
    } else if (execState === 'RERANKING') {
      currentStage = "BGE_RERANKING";
    } else if (execState === 'ONLINE_RETRIEVING') {
      currentStage = "ONLINE_RESEARCH";
    } else if (execState === 'EVIDENCE_ASSEMBLY') {
      currentStage = "EVIDENCE_PREPARATION";
    } else {
      currentStage = "QUERY_PROCESSING";
    }
  }

  return {
    search_id: raw.search_id,
    execution_id: raw.execution_id || `exec_${raw.search_id}`,
    execution_state: execState,
    current_stage: currentStage,
    stage_message: raw.stage_message || raw.stage || currentStage,
    terminal: isTerminal,
    overall_status: overall,
    progress: raw.progress || 0,
    stage: raw.stage || currentStage,
    warnings: raw.warnings || [],
    results,
    combined_result_count: raw.combined_result_count || (raw.results ? raw.results.length : 0),
    providers: raw.providers,
    local: {
      status: localStatus,
      stage: raw.trace?.local_trace?.stage || localStatus,
      progress: null,
      result_count: raw.local_result_count || 0,
      trace: raw.trace?.local_trace || raw.local_trace
    },
    online: {
      status: onlineStatus,
      stage: raw.trace?.online_trace?.stage || onlineStatus,
      progress: null,
      result_count: raw.online_result_count || 0,
      trace: raw.trace?.online_trace || raw.online_trace
    },
    metrics: raw.metrics || {
      combined_metrics: raw.combined_metrics
    }, 
    trace: raw.trace || {
      local_trace: raw.local_trace,
      online_trace: raw.online_trace,
      combined_trace: raw.combined_trace
    },
  };
}

export const normalizeSearchExperimentResponse = normalizeStatusResponse;

export interface CanonicalSearchResult {
  searchId: string;
  executionId: string;
  executionState: ExecutionState;
  currentStage: PipelineStage;
  stageMessage?: string;
  terminal: boolean;
  query: string;
  status: 'IDLE' | 'SEARCHING' | 'LOCAL_RUNNING' | 'ONLINE_RUNNING' | 'MERGING' | 'RERANKING' | 'EVIDENCE_ASSEMBLY' | 'COMPLETED' | 'FAILED';
  localPapers: any[];
  onlinePapers: any[];
  uniquePapers: any[];
  evidenceBlocks: any[];
  warnings: ProviderWarning[];
  localCount: number;
  onlineCount: number;
  uniqueCount: number;
  evidenceCount: number;
  rawStatus: ExperimentStatus;
}

export function normalizeCanonicalSearchResult(rawStatus: ExperimentStatus, query: string = ''): CanonicalSearchResult {
  const results = rawStatus.results || [];
  const localPapers = results.filter((r: any) => r.retrieval_source === 'local');
  const onlinePapers = results.filter((r: any) => r.retrieval_source === 'online' || r.retrieval_source === 'web' || r.source === 'crossref' || r.source === 'openalex');
  const uniquePapers = results;
  const evidenceBlocks = results.filter((r: any) => !!(r.evidence_text || r.abstract || r.snippet));
  
  const localCount = rawStatus.local?.result_count ?? localPapers.length;
  const onlineCount = rawStatus.online?.result_count ?? onlinePapers.length;
  const uniqueCount = rawStatus.combined_result_count ?? uniquePapers.length;
  const evidenceCount = evidenceBlocks.length;

  const execState = rawStatus.execution_state || 'INITIALIZING';
  const isTerminal = Boolean(rawStatus.terminal);
  const currentStage = rawStatus.current_stage || (isTerminal ? "RESULTS_READY" : "QUERY_PROCESSING");

  let legacyStatus: CanonicalSearchResult['status'] = 'SEARCHING';
  if (isTerminal) {
    legacyStatus = execState === 'FAILED' ? 'FAILED' : 'COMPLETED';
  } else if (execState === 'LOCAL_RETRIEVING') {
    legacyStatus = 'LOCAL_RUNNING';
  } else if (execState === 'ONLINE_RETRIEVING') {
    legacyStatus = 'ONLINE_RUNNING';
  } else if (execState === 'MERGING') {
    legacyStatus = 'MERGING';
  } else if (execState === 'RERANKING') {
    legacyStatus = 'RERANKING';
  } else if (execState === 'EVIDENCE_ASSEMBLY') {
    legacyStatus = 'EVIDENCE_ASSEMBLY';
  } else {
    legacyStatus = 'SEARCHING';
  }

  return {
    searchId: rawStatus.search_id,
    executionId: rawStatus.execution_id || `exec_${rawStatus.search_id}`,
    executionState: execState,
    currentStage: currentStage,
    stageMessage: rawStatus.stage_message,
    terminal: isTerminal,
    query,
    status: legacyStatus,
    localPapers,
    onlinePapers,
    uniquePapers,
    evidenceBlocks,
    warnings: rawStatus.warnings || [],
    localCount,
    onlineCount,
    uniqueCount,
    evidenceCount,
    rawStatus
  };
}

export function mergeCanonicalResults(
  prev: CanonicalSearchResult | null,
  incoming: CanonicalSearchResult
): CanonicalSearchResult {
  if (!prev || prev.searchId !== incoming.searchId || prev.executionId !== incoming.executionId) {
    return incoming;
  }

  // Preserve accumulated papers if incoming payload is intermediate empty array
  const uniquePapers = incoming.uniquePapers.length > 0 ? incoming.uniquePapers : prev.uniquePapers;
  const localPapers = incoming.localPapers.length > 0 ? incoming.localPapers : prev.localPapers;
  const onlinePapers = incoming.onlinePapers.length > 0 ? incoming.onlinePapers : prev.onlinePapers;
  const evidenceBlocks = incoming.evidenceBlocks.length > 0 ? incoming.evidenceBlocks : prev.evidenceBlocks;

  return {
    ...incoming,
    uniquePapers,
    localPapers,
    onlinePapers,
    evidenceBlocks,
    localCount: Math.max(prev.localCount, incoming.localCount),
    onlineCount: Math.max(prev.onlineCount, incoming.onlineCount),
    uniqueCount: Math.max(prev.uniqueCount, incoming.uniqueCount),
    evidenceCount: Math.max(prev.evidenceCount, incoming.evidenceCount),
  };
}

export function normalizeSearchId(value: any): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  if (!trimmed || trimmed === 'null' || trimmed === 'undefined' || trimmed === '[object Object]') return null;
  
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(trimmed)) return null;
  return trimmed;
}


