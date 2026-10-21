IMPLEMENTATION PROMPT
PROJECT: ResearchMind / ResearchNexus AI
FEATURE: Strict AI Research Assistant Workflow

============================================================
0. PRIMARY OBJECTIVE
============================================================

Implement the AI Assistant as a structured research workspace.

IMPORTANT:
This is NOT a generic chatbot.

The Assistant must behave as a research workflow system built around:

Research Context
→ Evidence
→ Answer
→ Verification
→ Refinement

The user must always understand:
1. What they are doing.
2. What evidence is being used.
3. What the system is currently doing.
4. What was generated.
5. What was verified.
6. What can be improved.

The four major user-facing workspaces are:

1. ASK
   Research Answer

2. EXPLORE PAPERS
   Upload Papers
   Compare Papers

3. PROVE
   Evidence & Claim Verification

4. REFINE
   Strengthen the Answer

These are NOT a forced wizard.

The user may move between them deliberately.

Valid examples:

Explorer → ASK
Explorer → COMPARE
UPLOAD → ASK
UPLOAD → COMPARE
COMPARE → ASK
COMPARE → PROVE
ASK → PROVE
PROVE → REFINE
REFINE → PROVE

Do NOT automatically navigate between workspaces.

The user must explicitly choose the next action.

============================================================
1. EXISTING TECHNOLOGIES — DO NOT REPLACE
============================================================

Use the existing project architecture.

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS

Backend:
- FastAPI
- Existing PostgreSQL architecture
- Existing ChromaDB

Document processing:
- PyMuPDF
- LlamaIndex

Embedding:
- BAAI/bge-base-en-v1.5

Retrieval:
- BM25
- ChromaDB dense retrieval
- Reciprocal Rank Fusion
- RRF k=60

Reranking:
- BAAI/bge-reranker-base

LLM:
- Gemini 2.5 Flash

Do NOT introduce another LLM.
Do NOT replace existing retrieval.
Do NOT introduce LangChain unless already present and required.
Do NOT invent architecture that does not exist.

Reuse existing Research Explorer, XAI, Enhanced RAG, Claim Verification,
Iterative Refinement, Comparison, Personal Corpus, and Research Session
implementations wherever possible.

============================================================
2. CORE ARCHITECTURAL RULE
============================================================

Create ONE shared ResearchContext.

All Assistant workspaces operate on this context.

Do NOT allow each workspace to create its own unrelated paper/evidence state.

The context must be authoritative for:

- query
- search
- papers
- selected papers
- uploaded documents
- evidence
- answer
- claims
- citations
- verification
- refinement versions

============================================================
3. RESEARCH CONTEXT MODEL
============================================================

Create or consolidate a ResearchContext model.

Example:

interface ResearchContext {
  contextId: string;

  searchId: string | null;
  query: string;

  contextOrigin:
    | "EXPLORER"
    | "DIRECT"
    | "UPLOAD"
    | "COMPARE";

  activeWorkspace:
    | "ASK"
    | "UPLOAD"
    | "COMPARE"
    | "PROVE"
    | "REFINE";

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

============================================================
4. IMMUTABILITY RULES
============================================================

The following are immutable for a generated artifact:

- searchId
- contextHash
- evidence provenance
- selected paper IDs
- uploaded document IDs
- source IDs
- evidence IDs

Do NOT silently mutate an active context.

When the user changes important context:

Example:

Old:
Paper A + Paper B

User adds:
Paper C

Do NOT silently change the old answer's context.

Create a new context version.

Example:

Context v1
→ Answer v1

Context changes
→ Context v2

New analysis
→ Answer v2

Historical artifacts remain immutable.

============================================================
5. CONTEXT HASH
============================================================

Create deterministic SHA256 context hashing.

Hash the canonicalized representation of:

- searchId
- query
- selectedPaperIds
- uploadedDocumentIds
- evidence IDs
- relevant scope information

The same context must always produce the same hash.

Example:

SHA256(canonicalizedContext)

Every generated artifact must store:

contextHash

This allows the system to answer:

"This exact answer was generated from this exact research context."

============================================================
6. CONTEXT ORIGINS
============================================================

There are four valid context origins.

------------------------------------------------------------
A. EXPLORER
------------------------------------------------------------

User performs research search in Research Explorer.

Example:

Query:
AgenticGraph

Research Explorer retrieves:

- local papers
- online papers
- unique papers
- evidence blocks

User remains on Research Explorer.

IMPORTANT:
Do NOT automatically navigate to XAI or Assistant.

The user must explicitly choose:

"Use in AI Assistant"

or equivalent existing action.

When selected:

Reuse the SAME searchId.

Do NOT start another search.

------------------------------------------------------------
B. DIRECT
------------------------------------------------------------

User enters the Assistant directly and asks:

"How do graph-based agent architectures improve tool selection?"

Create a new ResearchContext.

Only retrieve evidence when required by the selected scope.

------------------------------------------------------------
C. UPLOAD
------------------------------------------------------------

User uploads paper(s).

The upload pipeline processes documents.

Do not automatically create a research answer.

Only add uploaded documents to active context when user selects:

"Add to Research Context"

------------------------------------------------------------
D. COMPARE
------------------------------------------------------------

User selects 2–5 papers.

Create ComparisonContext derived from ResearchContext.

Selected papers become immutable for that comparison operation.

============================================================
7. GLOBAL SCOPE RULES
============================================================

Support existing scopes:

1. all_research
2. selected_papers
3. single_paper
4. current_evidence
5. uploaded_documents

Strictly enforce them.

------------------------------------------------------------
CURRENT_EVIDENCE
------------------------------------------------------------

ZERO retrieval.

Use only already supplied evidenceBlocks.

------------------------------------------------------------
SINGLE_PAPER
------------------------------------------------------------

Only selected paper may be used.

No unrelated local or online evidence.

------------------------------------------------------------
SELECTED_PAPERS
------------------------------------------------------------

Only selectedPaperIds.

No hidden retrieval outside selected papers.

------------------------------------------------------------
UPLOADED_DOCUMENTS
------------------------------------------------------------

Only uploadedDocumentIds.

Do not mix with general research corpus unless explicitly selected.

------------------------------------------------------------
ALL_RESEARCH
------------------------------------------------------------

May use eligible local/online research sources through
the existing retrieval architecture.

============================================================
8. ASK WORKSPACE
============================================================

NAME:
ASK

PURPOSE:
Generate an evidence-grounded research answer.

ASK is responsible for:

- understanding the research question
- determining context eligibility
- retrieving eligible evidence when needed
- assembling evidence
- generating answer
- mapping citations
- performing structural citation validation

ASK is NOT responsible for:

- deep claim verification
- iterative refinement
- arbitrary paper comparison
- research memory management
- unrestricted retrieval
- hidden retrieval during verification

============================================================
9. ASK WORKFLOW
============================================================

Implement the following exact workflow:

1. Query Understanding
2. Context Eligibility
3. Retrieval if required
4. Evidence Deduplication
5. Context Assembly
6. Answer Generation
7. Citation Mapping
8. Structural Citation Validation
9. Render Answer
10. Offer explicit actions

Workflow:

Question
↓
Understand
↓
Eligibility
↓
Retrieve if required
↓
Evidence
↓
Gemini 2.5 Flash
↓
Citation Mapping
↓
Validation
↓
Research Answer

============================================================
10. QUERY UNDERSTANDING
============================================================

Extract only information needed by the research pipeline.

Examples:

- research intent
- core terms
- entities
- comparison intent
- numerical intent
- methodological intent
- scope constraints
- time constraints

Do not expose excessive technical detail to normal users.

Normal UI:

"Understanding your research question"

Technical disclosure:

"Query normalization → retrieval intent → keyword extraction"

============================================================
11. ASK RETRIEVAL
============================================================

If retrieval is required, use existing architecture:

BM25
+
Chroma dense retrieval
↓
RRF k=60
↓
BGE reranker
↓
Evidence eligibility
↓
Deduplication
↓
Context assembly

Do NOT create a second retrieval implementation.

Reuse existing Retrieval/XAI infrastructure.

============================================================
12. EVIDENCE BLOCK MODEL
============================================================

Every evidence block must maintain provenance.

Example:

interface EvidenceBlock {
  evidenceId: string;

  sourceType:
    | "LOCAL"
    | "ONLINE"
    | "UPLOADED";

  paperId?: string;
  documentId?: string;

  chunkId: string;

  text: string;

  sourceTitle: string;

  retrievalMethod:
    | "BM25"
    | "DENSE"
    | "RRF"
    | "BGE";

  retrievalScore?: number;

  metadata?: Record<string, unknown>;
}

Do not strip provenance before generation.

============================================================
13. ANSWER GENERATION
============================================================

Use existing Gemini 2.5 Flash integration.

Prompt requirements:

- answer only from supplied eligible evidence
- no unsupported factual claims
- no invented citations
- no invented studies
- preserve uncertainty
- distinguish evidence from interpretation
- attach citations to evidence-grounded claims

Do not allow generation to retrieve new information.

============================================================
14. ANSWER STRUCTURE
============================================================

Do NOT render as a generic chat message.

Use research-oriented structure.

Recommended output:

Research Answer

Summary

Key Findings

Evidence-Based Analysis

Methodological Interpretation

Limitations / Uncertainty

References

Evidence details should be expandable.

============================================================
15. ASK OUTPUT MODEL
============================================================

Create:

interface ResearchAnswer {
  answerId: string;

  contextId: string;

  contextHash: string;

  summary: string;

  sections: AnswerSection[];

  citations: Citation[];

  evidenceManifest: EvidenceManifest;

  model: string;

  createdAt: string;
}

Do not overwrite previous answers.

============================================================
16. ASK ACTIONS
============================================================

After answer generation, display explicit actions.

Examples:

[Prove Claims]

[Strengthen Answer]

[Compare Papers]

[Inspect Evidence]

Do not automatically enter another workspace.

============================================================
17. EXPLORE PAPERS — UPLOAD
============================================================

UPLOAD purpose:

Bring user's research papers into the Personal Research Corpus.

Do not generate an answer automatically.

Reuse existing Personal Corpus pipeline.

Required lifecycle:

UPLOADED
↓
VALIDATING
↓
PROCESSING
↓
EXTRACTED
↓
CHUNKING
↓
EMBEDDING
↓
INDEXING
↓
VERIFYING
↓
READY

or

FAILED

============================================================
18. UPLOAD VALIDATION
============================================================

Validate:

- PDF magic bytes
- file size
- SHA256
- duplicate status
- user ownership

Maximum existing limit:

50 MB

Do not modify this limit unless already configured differently in the project.

============================================================
19. UPLOAD PROCESSING
============================================================

Use:

PDF
↓
PyMuPDF
↓
text extraction
↓
cleaning
↓
section-aware processing
↓
LlamaIndex semantic chunking
↓
BGE embeddings
↓
Chroma indexing
↓
cross-store verification
↓
READY

READY is allowed only after indexing verification succeeds.

============================================================
20. UPLOAD USER FLOW
============================================================

After READY:

Show:

Paper Ready

Actions:

[Add to Research Context]
[Open Paper]
[Compare]

Do not automatically start ASK.

============================================================
21. COMPARE WORKSPACE
============================================================

Purpose:

Compare 2–5 research papers using evidence specific to each paper.

Strict validation:

minimum = 2
maximum = 5

Anything outside this range must be rejected with a clear UI message.

============================================================
22. COMPARISON DIMENSIONS
============================================================

Use exactly:

1. Objective
2. Research Problem
3. Methodology
4. Architecture / Model
5. Dataset
6. Experimental Setup
7. Evaluation Metrics
8. Results
9. Limitations
10. Future Work

Do not add random comparison dimensions unless they already exist
elsewhere in the current implementation.

============================================================
23. COMPARISON WORKFLOW
============================================================

Selected papers
↓
Lock ComparisonContext
↓
Retrieve paper-specific evidence
↓
Extract dimensions
↓
Normalize comparable information
↓
Generate comparison
↓
Validate comparative claims
↓
Display comparison

============================================================
24. COMPARISON EVIDENCE RULE
============================================================

Every comparison cell must be traceable to one or more paper-specific
evidence blocks.

Do not create unsupported comparison values.

If information is missing:

Display:

"Not reported"

If metrics are incompatible:

Display:

"Not directly comparable"

Do NOT infer a winner.

============================================================
25. NO ARBITRARY WINNER
============================================================

Never produce:

"Best Paper: A"

unless the user explicitly defines a valid comparison criterion.

Otherwise show:

Paper A
Strengths
Limitations

Paper B
Strengths
Limitations

etc.

============================================================
26. COMPARE ACTIONS
============================================================

After comparison:

[Ask About These Papers]

[Prove Comparative Claims]

[Refine Comparison]

[Open Paper]

Again:
No automatic transition.

============================================================
27. PROVE WORKSPACE
============================================================

PURPOSE:

Determine whether answer claims are actually supported by evidence.

Input:

- answer
- claims
- citations
- evidence
- context

PROVE is NOT another generation pass.

============================================================
28. PROVE WORKFLOW
============================================================

Answer
↓
Claim Extraction
↓
Claim Normalization
↓
Stage A deterministic verification
↓
Stage B evidence-only LLM verification
↓
Citation validation
↓
Optional citation repair
↓
Verification Result

============================================================
29. CLAIM EXTRACTION
============================================================

Extract meaningful factual/analytical claims.

Do not treat every sentence fragment as an independent claim.

Store:

claimId
claimText
claimType
citations
supportingEvidence

============================================================
30. STAGE A — DETERMINISTIC VERIFICATION
============================================================

Check:

- exact numbers
- percentages
- ranges
- dates
- negations
- named entities
- citation presence
- obvious textual mismatch

Example:

Claim:
"Accuracy increased from 81% to 91%."

Evidence:
"Accuracy increased from 81% to 86%."

Return:

NUMERICAL_SUPPORT_GAP

Do not let the LLM override deterministic mismatch.

============================================================
31. STAGE B — EVIDENCE-ONLY VERIFICATION
============================================================

Use Gemini 2.5 Flash only against supplied evidence.

No new retrieval.

Allowed statuses:

SUPPORTED
PARTIALLY_SUPPORTED
INSUFFICIENT_EVIDENCE
UNSUPPORTED
VERIFICATION_UNAVAILABLE

Verifier must not search the internet.

Verifier must not access unrestricted corpus retrieval.

============================================================
32. CITATION VERIFICATION
============================================================

Allowed citation statuses:

VALID
INVALID
MISSING
REPAIRED

Repair only if supporting evidence is unambiguous.

If ambiguous:

MISSING / INVALID

Do NOT guess.

============================================================
33. PROVE METRICS
============================================================

Maintain:

CitationPrecision
CitationCoverage
ClaimSupportRate
UnsupportedClaimRate

Also preserve claim-level details.

============================================================
34. PROVE UI
============================================================

Each claim must have a visible evidence path.

Example:

Claim 01
"Graph reasoning improves tool selection."

SUPPORTED

Evidence
[exact passage]

Source
Paper X

Citation
✓ Valid

------------------------------------------------------------

For unsupported:

Claim 05

UNSUPPORTED

Reason:
Available evidence does not establish this claim.

Actions:

[Revise Claim]

[Remove Claim]

============================================================
35. REFINE WORKSPACE
============================================================

PURPOSE:

Strengthen a research answer based on evidence weaknesses.

Input:

- current answer
- verification result
- context
- evidence manifest

Refinement is NOT unlimited.

Maximum:

2 refinement cycles.

Versions:

v1
→ v2
→ v3

============================================================
36. REFINE WORKFLOW
============================================================

Current Answer
↓
Analyze verification
↓
Generate deterministic feedback
↓
Classify evidence problem
↓
Determine refinement necessity
↓
Generate revised answer
↓
Re-verify
↓
Store immutable version

============================================================
37. REFINEMENT FEEDBACK TYPES
============================================================

Use exactly:

MISSING_EVIDENCE
WEAK_EVIDENCE
UNSUPPORTED_CLAIM
PARTIAL_SUPPORT
NUMERICAL_SUPPORT_GAP
NO_REFINEMENT_NEEDED

Reuse the existing Iterative Refinement logic.

============================================================
38. REFINEMENT RULE
============================================================

Never modify v1 in-place.

Store:

v1
v2
v3

Each version must preserve:

- answer
- citations
- evidence manifest
- verification
- feedback
- contextHash
- generation metadata
- timestamp
- latency

============================================================
39. REFINEMENT EXAMPLE
============================================================

v1:

"Model A substantially improves performance."

Verification:

PARTIALLY_SUPPORTED

Reason:

Evidence demonstrates improvement only on Dataset X.

v2 should become:

"Model A improves performance on Dataset X under the reported experimental conditions."

Do not broaden the claim beyond available evidence.

============================================================
40. REFINE UI
============================================================

Create a clear version timeline:

v1
│
├── verification
│
├── evidence gap
│
▼
v2
│
├── verification
│
▼
v3

Show:

What changed
Why it changed
Which evidence caused the change

============================================================
41. NAVIGATION RULES
============================================================

Allowed:

ASK → PROVE
ASK → REFINE

COMPARE → ASK
COMPARE → PROVE
COMPARE → REFINE

UPLOAD → ASK
UPLOAD → COMPARE

PROVE → REFINE
REFINE → PROVE

No automatic transitions.

The user controls movement.

============================================================
42. NO HIDDEN WORKFLOW
============================================================

Never let one workspace secretly perform another workspace's job.

Examples:

ASK must not silently perform refinement.

PROVE must not silently perform retrieval.

REFINE must not silently change research context.

COMPARE must not silently search unrelated literature.

UPLOAD must not silently generate an answer.

============================================================
43. API ARCHITECTURE
============================================================

Do not create one generic:

POST /assistant/chat

endpoint.

Use task-specific APIs or reuse existing endpoints cleanly.

Suggested responsibilities:

POST /assistant/context
GET  /assistant/context/{context_id}

POST /assistant/answer

POST /assistant/upload
GET  /assistant/upload/{document_id}/status

POST /assistant/compare

POST /assistant/verify

POST /assistant/refine

Use existing backend routes where equivalent functionality already exists.

Do not duplicate an already implemented subsystem.

============================================================
44. CONTEXT VALIDATION
============================================================

Before every major operation validate:

- context exists
- user owns context
- contextHash matches
- paper IDs are valid
- uploaded document IDs belong to user
- scope is compatible
- required evidence exists
- required answer exists for PROVE/REFINE

Reject invalid operations explicitly.

============================================================
45. ERROR STATES
============================================================

Do not collapse all failures into:

"Something went wrong."

Use clear research-specific states.

Examples:

NO_ELIGIBLE_EVIDENCE
CONTEXT_INVALID
PAPER_NOT_FOUND
UPLOAD_NOT_READY
INSUFFICIENT_EVIDENCE
VERIFICATION_UNAVAILABLE
REFINEMENT_LIMIT_REACHED
INVALID_COMPARISON_SIZE
CONTEXT_CHANGED

============================================================
46. USER-FACING PROGRESS
============================================================

Use progressive disclosure.

Normal user:

Understanding your question
Finding relevant research
Selecting strongest evidence
Building research context
Generating answer
Checking citations

Advanced user can expand:

Technical Details

Then show actual pipeline:

Question
↓
BM25 + Dense
↓
RRF k=60
↓
BGE
↓
Eligibility
↓
Deduplication
↓
Context
↓
Gemini 2.5 Flash
↓
Citation Mapping
↓
Verification
↓
Refinement

Do not show fake percentages.

Do not create fake progress bars.

============================================================
47. RESEARCH SESSION INTEGRATION
============================================================

Every major action should be represented in the existing Research Session system.

Artifacts:

ResearchAnswer
ComparisonResult
VerificationResult
RefinementVersion

Each artifact must reference:

sessionId
contextId
contextHash
createdAt

Historical artifacts are immutable.

Regenerated output = new version/artifact.

============================================================
48. RESEARCH MEMORY INTEGRATION
============================================================

Reuse existing ResearchMemory architecture.

Memory origin may be:

USER_RECORDED
EVIDENCE_DERIVED
AI_SUGGESTED

AI-suggested memories require explicit user acceptance.

Do not automatically turn every Assistant answer into permanent memory.

Evidence has higher authority than memory.

============================================================
49. FRONTEND COMPONENT STRUCTURE
============================================================

Use/reuse existing components where possible.

Suggested structure:

AssistantLanding
AssistantNavigation
ResearchContextBar
ContextInspector

AskWorkspace
ResearchComposer
ResearchAnswer
KeyFindingCard
EvidenceCard
CitationDrawer

UploadWorkspace
UploadDropzone
UploadProgress
DocumentInspector

CompareWorkspace
CompareTable
PaperInspector
ComparisonEvidence

ProveWorkspace
ClaimList
ClaimProofDrawer
EvidenceViewer
CitationStatus

RefineWorkspace
RefinementTimeline
RefinementInspector
VersionComparison
EvidenceGapPanel

ResearchPipeline
TechnicalDetailsPanel

Do not create redundant components if equivalent ones already exist.

============================================================
50. CONTEXT BAR
============================================================

Every workspace should show current context.

Example:

Research Context

Query:
AgenticGraph

Sources:
24 Local
13 Online

Selected Papers:
4

Uploaded:
2

Evidence:
31 blocks

Context:
LOCKED

[Inspect]

This gives the user continuous awareness of what the Assistant is using.

============================================================
51. CONTEXT INSPECTOR
============================================================

Create an expandable context inspector.

Show:

Query
Source origin
Papers
Selected papers
Uploaded documents
Evidence count
Context hash
Scope
Context version

Do not expose raw internal identifiers prominently.
Technical metadata can be expandable.

============================================================
52. PERFORMANCE RULES
============================================================

Do not reload:

- BGE model for every answer
- embedding model for every request
- same search context repeatedly
- same paper metadata repeatedly
- same uploaded document repeatedly

Reuse existing model singletons and caches.

Do not introduce artificial delays.

No setTimeout hacks.

No fake workflow animations.

============================================================
53. SECURITY / ISOLATION
============================================================

Every context/artifact/document must be ownership checked.

User A must never access:

- User B papers
- User B uploads
- User B contexts
- User B sessions
- User B memories
- User B verification artifacts

Never rely only on frontend filtering.

Backend must enforce ownership.

============================================================
54. TESTING
============================================================

Create a dedicated test suite for the strict Assistant workflow.

Minimum tests:

ASSIST-01
Direct ASK creates valid ResearchContext.

ASSIST-02
Explorer context preserves exact searchId.

ASSIST-03
Opening Assistant does not start another search.

ASSIST-04
Current-evidence scope performs zero retrieval.

ASSIST-05
Single-paper scope cannot access other papers.

ASSIST-06
Selected-paper scope cannot access unselected papers.

ASSIST-07
Uploaded-document scope cannot access unrelated corpus.

ASSIST-08
ASK generates answer only from eligible evidence.

ASSIST-09
Answer citations retain evidence provenance.

ASSIST-10
COMPARE rejects fewer than 2 papers.

ASSIST-11
COMPARE rejects more than 5 papers.

ASSIST-12
COMPARE uses paper-specific evidence.

ASSIST-13
Incompatible metrics are marked Not directly comparable.

ASSIST-14
No arbitrary winner generated.

ASSIST-15
PROVE Stage A detects numerical mismatch.

ASSIST-16
PROVE Stage B uses only provided evidence.

ASSIST-17
PROVE cannot trigger hidden retrieval.

ASSIST-18
Citation repair only occurs when unambiguous.

ASSIST-19
REFINE is limited to 2 cycles.

ASSIST-20
v1 remains immutable after refinement.

ASSIST-21
Refinement preserves contextHash.

ASSIST-22
Context mutation creates a new version.

ASSIST-23
Artifacts store contextHash.

ASSIST-24
AI-suggested memory requires user acceptance.

ASSIST-25
Cross-user access is rejected.

ASSIST-26
Workspace transitions are user-controlled.

ASSIST-27
No automatic ASK → PROVE transition.

ASSIST-28
No automatic PROVE → REFINE transition.

ASSIST-29
No generic /assistant/chat endpoint behavior.

ASSIST-30
Refreshing XAI/Assistant context restores the same context.

============================================================
55. END-TO-END TEST
============================================================

TEST FLOW A:

Research Explorer
↓
Search "AgenticGraph"
↓
Retrieve papers
↓
User explicitly selects "Use in AI Assistant"
↓
ASK
↓
Generate grounded answer
↓
User selects PROVE
↓
Verify claims
↓
Unsupported claim identified
↓
User selects REFINE
↓
Generate v2
↓
Re-verify
↓
Final answer

Verify:
- same context
- same evidence provenance
- correct searchId
- correct contextHash
- no hidden retrieval
- no automatic navigation
- v1 preserved

============================================================
56. END-TO-END TEST B
============================================================

Upload Paper A
Upload Paper B

Wait until both are READY

User selects:
COMPARE

Compare:

Objective
Research Problem
Methodology
Architecture
Dataset
Experimental Setup
Metrics
Results
Limitations
Future Work

User selects:
PROVE COMPARATIVE CLAIMS

Then:
REFINE if needed.

============================================================
57. END-TO-END TEST C
============================================================

Start Assistant directly.

Question:

"How do graph-based agent systems support tool selection?"

ASK

Verify:

- context created
- eligible evidence selected
- retrieval if required
- BGE reranking used
- Gemini generation
- citations mapped

Then:

PROVE

Then:

REFINE

No workspace should silently perform the next step.

============================================================
58. UI DESIGN REQUIREMENTS
============================================================

The UI must feel like:

Research Desk
Scientific Workspace
Research Operating System

NOT:

Generic AI chatbot
ChatGPT clone
Social chat interface

Visual characteristics:

- calm
- scholarly
- structured
- spacious
- evidence-focused
- progressive disclosure
- clear hierarchy

Avoid:

- giant chat bubbles
- excessive rounded cards
- decorative AI effects
- unnecessary gradients
- fake animations
- cluttered dashboards
- excessive badges
- unnecessary icons

The product should visually communicate:

Research
Evidence
Traceability
Verification
Scientific reasoning

============================================================
59. LANDING PAGE
============================================================

Display four clear destinations.

ASK

Research Answer
"Ask a research question and build an evidence-grounded answer."

EXPLORE PAPERS

Upload Papers
"Bring your own research papers."

Compare Papers
"Compare 2–5 studies using paper-specific evidence."

PROVE

Evidence & Verification
"Check whether claims and citations are actually supported."

REFINE

Strengthen the Answer
"Find evidence gaps and improve the research answer."

Do not make the page look like a chat home page.

============================================================
60. FINAL ACCEPTANCE CRITERIA
============================================================

Implementation is considered complete only when:

[ ] ResearchContext is shared across workspaces.
[ ] Context hashing is deterministic.
[ ] Context mutation is versioned.
[ ] ASK has strict evidence eligibility.
[ ] ASK does not perform hidden refinement.
[ ] UPLOAD uses existing corpus workflow.
[ ] COMPARE supports exactly 2–5 papers.
[ ] COMPARE uses paper-specific evidence.
[ ] Unsupported comparisons are not forced.
[ ] PROVE has deterministic Stage A.
[ ] PROVE has evidence-only Stage B.
[ ] Verification performs no hidden retrieval.
[ ] Citation repair is conservative.
[ ] REFINE is limited to 2 cycles.
[ ] Refinement versions are immutable.
[ ] All artifacts preserve contextHash.
[ ] All operations enforce user ownership.
[ ] Workspace navigation is user-controlled.
[ ] No automatic XAI navigation.
[ ] No automatic PROVE transition.
[ ] No automatic REFINE transition.
[ ] No generic chatbot endpoint.
[ ] No fake progress.
[ ] No hidden retrieval.
[ ] Existing technologies are reused.
[ ] Existing Research Explorer/XAI/Verification/Refinement systems remain compatible.
[ ] Existing tests continue to pass.
[ ] New strict Assistant tests pass.
[ ] End-to-end workflow passes.

============================================================
61. IMPLEMENTATION ORDER
============================================================

Do NOT implement everything simultaneously.

Implement in this exact order:

PHASE 1
ResearchContext + contextHash + validation

PHASE 2
Assistant routing and workspace shell

PHASE 3
ASK backend integration

PHASE 4
ASK frontend

PHASE 5
UPLOAD integration

PHASE 6
COMPARE backend

PHASE 7
COMPARE frontend

PHASE 8
PROVE backend

PHASE 9
PROVE frontend

PHASE 10
REFINE backend

PHASE 11
REFINE frontend

PHASE 12
Research Session / Artifact integration

PHASE 13
Research Memory integration

PHASE 14
End-to-end testing

After each phase:
- run tests
- inspect existing behavior
- preserve all existing working functionality
- do not move to the next phase if the previous phase introduces regressions.

============================================================
62. FINAL IMPLEMENTATION PRINCIPLE
============================================================

The system must always answer these four questions:

1. WHAT AM I ASKING?
   → Research Context

2. WHAT EVIDENCE IS BEING USED?
   → Evidence / Provenance

3. IS THE ANSWER SUPPORTED?
   → PROVE

4. HOW CAN THE ANSWER BE STRENGTHENED?
   → REFINE

The final product must behave as a Research OS, not a chatbot.

DO NOT redesign unrelated Research Explorer functionality.
DO NOT remove existing XAI functionality.
DO NOT replace existing Enhanced RAG.
DO NOT replace existing Claim Verification.
DO NOT replace existing Iterative Refinement.
DO NOT create duplicate retrieval infrastructure.
DO NOT introduce fake workflow state.

Reuse existing implementations and integrate them under the strict ResearchContext architecture.