export interface ResearchPaper {
  id: string;
  title: string;
  authors: string;
  publicationYear?: number;
  url?: string;
  sourceType: 'LOCAL' | 'ONLINE' | 'UPLOADED' | 'MIXED';
}

export interface ComparisonCell {
  paper_id: string;
  dimension_id: string;
  dimension_name: string;
  status: 'EVIDENCE_BACKED' | 'NOT_REPORTED' | 'EXTRACTION_FAILED';
  value: string;
  evidence_id?: string | null;
  evidence_text?: string | null;
  page_number?: number | string | null;
  chunk_id?: string | null;
  source_id?: string | null;
  confidence?: number | null;
  is_available?: boolean;
}

export interface ComparisonRow {
  dimension: string;
  cells: ComparisonCell[];
  comparison_claims?: string[];
  metric_compatibility?: any;
}

export interface ComparisonMatrix {
  dimensions: string[];
  paper_ids: string[];
  rows: ComparisonRow[];
}

export interface ComparisonArtifact {
  comparison_id: string;
  session_id: string;
  question: string;
  paper_ids: string[];
  papers: {
    paper_id: string;
    title: string;
    authors: string;
    year?: number | string;
    source_type?: string;
  }[];
  dimensions: string[];
  matrix: ComparisonMatrix;
  summary: {
    similarities: string[];
    differences: string[];
    evidence_backed_findings?: string[];
  };
  created_at?: string;
}

export interface EvidenceBlock {
  evidenceId: string;
  sourceType: 'LOCAL' | 'ONLINE' | 'UPLOADED';
  paperId?: string;
  documentId?: string;
  chunkId: string;
  text: string;
  sourceTitle: string;
  retrievalMethod: 'BM25' | 'DENSE' | 'RRF' | 'BGE';
  retrievalScore?: number;
  metadata?: Record<string, unknown>;
}

export interface Claim {
  claimId: string;
  claimText: string;
  claimType: string;
  status: 'SUPPORTED' | 'PARTIALLY_SUPPORTED' | 'UNSUPPORTED' | 'INSUFFICIENT_EVIDENCE' | 'VERIFICATION_UNAVAILABLE';
  citations: string[];
  supportingEvidenceIds: string[];
  reasoning?: string;
}

export interface Citation {
  citationId: string;
  claimId: string;
  evidenceId: string;
  paperId?: string;
  sourceTitle: string;
  status: 'VALID' | 'INVALID' | 'MISSING' | 'REPAIRED';
}

export interface ResearchAnswer {
  answerId: string;
  contextId: string;
  contextHash: string;
  summary: string;
  sections: { title: string; content: string }[];
  citations: Citation[];
  model: string;
  createdAt: string;
}

export interface VerificationResult {
  verificationId: string;
  contextId: string;
  contextHash: string;
  claims: Claim[];
  citationPrecision: number;
  citationCoverage: number;
  claimSupportRate: number;
  unsupportedClaimRate: number;
}

export interface RefinementVersion {
  versionNumber: number;
  versionLabel: 'v1' | 'v2' | 'v3';
  contextHash: string;
  answer: ResearchAnswer;
  verification: VerificationResult;
  feedbackType: 'MISSING_EVIDENCE' | 'WEAK_EVIDENCE' | 'UNSUPPORTED_CLAIM' | 'PARTIAL_SUPPORT' | 'NUMERICAL_SUPPORT_GAP' | 'NO_REFINEMENT_NEEDED';
  createdAt: string;
}

export interface ResearchContext {
  contextId: string;
  searchId: string | null;
  query: string;
  contextOrigin: 'EXPLORER' | 'DIRECT' | 'UPLOAD' | 'COMPARE';
  activeWorkspace: 'ASK' | 'UPLOAD' | 'COMPARE' | 'PROVE' | 'REFINE';
  papers: ResearchPaper[];
  selectedPaperIds: string[];
  uploadedDocumentIds: string[];
  evidenceBlocks: EvidenceBlock[];
  claims: Claim[];
  citations: Citation[];
  answer: ResearchAnswer | null;
  verification: VerificationResult | null;
  refinementVersions: RefinementVersion[];
  contextHash: string;
  version: number;
}

export function computeContextHash(ctx: {
  searchId: string | null;
  query: string;
  selectedPaperIds: string[];
  uploadedDocumentIds: string[];
  evidenceIds: string[];
  scope: string;
}): string {
  const canonicalObj = {
    searchId: ctx.searchId || '',
    query: (ctx.query || '').trim().toLowerCase(),
    selectedPaperIds: [...ctx.selectedPaperIds].sort(),
    uploadedDocumentIds: [...ctx.uploadedDocumentIds].sort(),
    evidenceIds: [...ctx.evidenceIds].sort(),
    scope: ctx.scope || 'all_research'
  };
  const str = JSON.stringify(canonicalObj);
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  const hexString = Math.abs(hash).toString(16).padStart(8, '0');
  let sha256Like = '';
  for (let i = 0; i < 8; i++) {
    sha256Like += hexString;
  }
  return sha256Like.substring(0, 64);
}

export function createInitialResearchContext(overrides?: Partial<ResearchContext>): ResearchContext {
  const query = overrides?.query || '';
  const searchId = overrides?.searchId || null;
  const selectedPaperIds = overrides?.selectedPaperIds || [];
  const uploadedDocumentIds = overrides?.uploadedDocumentIds || [];
  const evidenceBlocks = overrides?.evidenceBlocks || [];
  const scope = 'all_research';

  const hash = computeContextHash({
    searchId,
    query,
    selectedPaperIds,
    uploadedDocumentIds,
    evidenceIds: evidenceBlocks.map(e => e.evidenceId),
    scope
  });

  return {
    contextId: overrides?.contextId || `ctx_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
    searchId,
    query,
    contextOrigin: overrides?.contextOrigin || 'DIRECT',
    activeWorkspace: overrides?.activeWorkspace || 'ASK',
    papers: overrides?.papers || [],
    selectedPaperIds,
    uploadedDocumentIds,
    evidenceBlocks,
    claims: overrides?.claims || [],
    citations: overrides?.citations || [],
    answer: overrides?.answer || null,
    verification: overrides?.verification || null,
    refinementVersions: overrides?.refinementVersions || [],
    contextHash: hash,
    version: overrides?.version || 1
  };
}

export function mutateResearchContextVersion(
  prev: ResearchContext,
  updates: Partial<ResearchContext>
): ResearchContext {
  const nextVersion = prev.version + 1;
  const query = updates.query !== undefined ? updates.query : prev.query;
  const searchId = updates.searchId !== undefined ? updates.searchId : prev.searchId;
  const selectedPaperIds = updates.selectedPaperIds || prev.selectedPaperIds;
  const uploadedDocumentIds = updates.uploadedDocumentIds || prev.uploadedDocumentIds;
  const evidenceBlocks = updates.evidenceBlocks || prev.evidenceBlocks;

  const nextHash = computeContextHash({
    searchId,
    query,
    selectedPaperIds,
    uploadedDocumentIds,
    evidenceIds: evidenceBlocks.map(e => e.evidenceId),
    scope: 'all_research'
  });

  return {
    ...prev,
    ...updates,
    query,
    searchId,
    selectedPaperIds,
    uploadedDocumentIds,
    evidenceBlocks,
    contextHash: nextHash,
    version: nextVersion
  };
}
