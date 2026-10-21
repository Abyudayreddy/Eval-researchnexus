THIS IS AN UPDATE INSTRUCTION DOCUMENT ONLY.
DO NOT TREAT THIS FILE AS A PAPER DRAFT.
The existing manuscript remains the base document. Only the affected claims, tables, figures, discussion, limitations, and conclusion statements should be updated using the canonical V4 evidence.

============================================================
1. OVERALL V4 STATUS
============================================================

Readiness:
READY_WITH_EXPLICIT_LIMITATIONS

Canonical benchmark:
ds_nexus_v11

Total dataset:
N = 100

Split:
DEV = 70
VAL = 15
TEST = 15

Canonical TEST split:
- item_v11_086–090: SYNTHESIS, answerable
- item_v11_091–095: ADVERSARIAL, answerable
- item_v11_096–100: UNANSWERABLE

Important:
The five unanswerable queries have no gold papers/chunks.

Do not describe this benchmark as a held-out test set unless the canonical documentation explicitly supports that wording.

============================================================
2. RETRIEVAL RESULTS THAT MAY BE PUBLISHED
============================================================

Use only these canonical claims:

BM25:
- Hit@20 = 0.6667 (10/15)
- Recall@20 = 1.0000 on answerable queries (10/10)
- MRR = 0.0759 across all 15 test queries

Hybrid RRF:
- Hit@20 = 0.6667 (10/15)
- Recall@20 = 1.0000 on answerable queries (10/10)
- MRR = 0.0431 across all 15 test queries

BGE reranker:
- MRR = 0.0480
- Hit@20 = 0.6667
- It provides only a modest promotion relative to Hybrid RRF.
- Do NOT describe it as a +47.7% improvement.

Dense Chroma:
- TEST top-20 hit rate = 0.0000 according to the canonical raw test baseline.

Important denominator rule:
- Hit@20 uses all 15 TEST queries.
- Recall@20 is reported on the 10 answerable queries.
- MRR = all 15 unless explicitly labelled otherwise.

The paper must make these denominators explicit.

============================================================
3. RETRIEVAL TABLE — MUST BE REPLACED
============================================================

The existing retrieval table contains stale/wrong values.

The paper author should replace it with a V4-grounded table.

At minimum include:
- BM25
- Dense Chroma
- Hybrid RRF
- BGE reranking

Use the canonical files to populate the table.

Do NOT preserve old DEV/VAL/ALL values unless they are explicitly supported by the V4 canonical files.

Do NOT mix answerable-only recall with all-query hit rate.

============================================================
4. CLAIM GROUNDING / VERIFICATION
============================================================

Canonical claim accounting:

56 extracted sentences total.

Claim categories:
- 30 appropriate abstentions
- 19 insufficient-evidence findings
- 7 factual assertions

Factual assertions:
- 4 Naive
- 3 Verified

Automated NLI:
- Naive supported factual claims: 4/4
- Verified supported factual claims: 3/3
- Automated NLI precision = 100%

Critical limitation:
The factual-claim denominator is only N=7.

Therefore DO NOT write:
"the system achieved perfect factual accuracy."

Instead describe it narrowly as:
100% automated NLI precision on the small set of seven evaluated factual assertions.

Unanswerable query abstention:
- 5/5 = 100%

Human ground-truth grounding:
- NOT_MEASURED / BLOCKED

Human Claim Verifier F1:
- NOT_MEASURED / BLOCKED

Human inter-annotator agreement:
- NOT_MEASURED / BLOCKED

Do NOT imply that human validation was performed.

============================================================
5. CITATION REPAIR
============================================================

Canonical result:

Citation improvement:
NOT OBSERVED

Applied repairs:
0

The V4 audit identified candidate repair cases, but repairs were rejected because of ambiguity in the available evidence/chunk set.

The canonical V4 report identifies 4 candidate repairs rejected because of 10-chunk ambiguity.

Therefore:

Do NOT use the older "191 repair opportunities" statement.

Do NOT claim citation repair improved factual accuracy.

Post-repair factual accuracy:
NOT_MEASURED because zero repairs were applied.

The correct scientific interpretation is:
The repair mechanism behaved conservatively and did not apply ambiguous repairs, but successful citation repair was not empirically demonstrated.

============================================================
6. PROVENANCE / EXPLAINABILITY
============================================================

Canonical result:

Claim-to-Evidence Completeness:
100%

Citation-to-Evidence Completeness:
100%

This supports local provenance tracking under the automated audit protocol.

However:

Do NOT claim this proves human-readable explainability.

Use wording such as:
"Automated provenance auditing showed complete claim-to-evidence and citation-to-evidence links under the evaluated protocol."

Human readability/usability of provenance was not independently validated.

============================================================
7. ITERATIVE REFINEMENT
============================================================

Canonical result:

Net grounding gain:
0.0%

Outcome:
- 1 improved
- 98 unchanged
- 1 degraded

Statistical result:
p = 1.000

Interpretation:
No demonstrated grounding improvement.

Latency:
The iterative refinement mechanism introduces approximately a +106% latency penalty according to the canonical V4 result.

Therefore the paper must NOT present iterative refinement as a demonstrated quality improvement.

Correct interpretation:
Iterative refinement is a safety-oriented optional mechanism, but the audited experiment did not demonstrate a measurable grounding benefit and incurred substantial additional latency.

============================================================
8. LATENCY TABLE
============================================================

Replace the existing latency table with values taken from:

canonical_latency_results.csv

Canonical component p50 values:

BM25:
0.69 ms

Dense:
13.51 ms

Hybrid RRF:
6.56 ms

BGE:
531.41 ms

Hybrid + BGE:
535.06 ms

Complete request:
mean = 12.12 s

Important:

Component percentiles are NOT additive.

Do not sum:
BM25 + Dense + RRF + BGE
and call that end-to-end latency.

Clearly distinguish:
1. component latency
2. complete request end-to-end latency

Do not automatically preserve older generation means or old verified-pipeline numbers unless the canonical latency CSV explicitly contains and supports them.

If the paper includes refinement-off vs refinement-on latency, use the exact paired canonical values from the V4 source.

============================================================
9. MODEL CONFIGURATION / INTERNAL VALIDITY
============================================================

Canonical configuration:

E04 historical:
gemini-2.5-flash
T = 0.0

E04.1 authoritative:
gemini-3.5-flash-lite
T = 0.0

Current backend target:
gemini-2.5-flash
T = 0.0

The paper must distinguish historical, authoritative evaluation, and current backend configuration.

Do NOT imply that every experiment was performed with the same model.

Model evolution must be listed as an internal-validity threat.

============================================================
10. FIGURE 1 — ARCHITECTURE
============================================================

Keep the existing architecture figure.

However:

- Do not hard-code Gemini 2.5 Flash as though it represents every benchmark experiment.
- Use a model/version-per-experiment label OR clearly distinguish current backend from benchmark configuration.
- Citation repair should be represented as ambiguity-gated/conservative.
- Do not visually imply that citation repair was successfully demonstrated.
- Iterative refinement should be represented as optional.
- Do not visually imply that refinement necessarily improves grounding.

The figure itself should remain conceptually consistent with the actual implementation.

============================================================
11. FIGURE 2 — REFINEMENT / LATENCY GRAPH
============================================================

Current quality counts are valid:

- 1 improved
- 98 unchanged
- 1 degraded
- p = 1.000

However, the existing latency bars use older values:

5,691.4 ms
12,655.7 ms

and show approximately 2.22×.

These must NOT be copied blindly.

Rebuild the latency comparison only from canonical_latency_results.csv using the same measurement boundary and experiment on both sides.

Do NOT manually alter values simply to force the graph to show +106%.

If the canonical file does not provide a directly comparable pair, remove the latency part of the figure and report only the supported V4 latency result in prose.

Do not fabricate a new plot.

============================================================
12. FIGURES 3–5 — UI SCREENSHOTS
============================================================

These figures are platform/interface illustrations, NOT experimental evidence.

Existing screenshots may be retained.

Recommended structure:

One multi-panel figure:

(a) Research Explorer
(b) AI Assistant
(c) Claim-Level Explainability

Use one caption.

If the paper's page limit makes this impractical, retain only the most scientifically relevant one or two screenshots.

Priority:
Claim-Level Explainability > AI Assistant > Research Explorer

because the first is most directly connected to the paper's explainability contribution.

Improve cropping/readability only if needed.

Do not invent or redesign the UI.

============================================================
13. FIGURE NUMBERING / LATEX FORMATTING
============================================================

The current manuscript has manually written figure numbering in some places.

The author should use proper LaTeX:

\begin{figure}
...
\caption{...}
\label{fig:...}
\end{figure}

Use automatic numbering.

All in-text figure references should use:

\ref{fig:...}

Do not manually type:
"Fig. 3"
"Fig. 4"
"Fig. 5"

inside captions or body text when automatic references can be used.

Check all figure references after rearranging figures.

============================================================
14. TABLE / FIGURE CONSISTENCY CHECK
============================================================

Before final manuscript submission, verify:

- Every figure has one correct caption.
- Every table has one correct caption.
- Every figure/table is referenced in the text.
- Figure numbering is sequential.
- Table numbering is sequential.
- No figure references point to the wrong image.
- Units are consistent.
- Percentages and decimal values use consistent formatting.
- Metric denominators are stated.
- All V4 values match the canonical files.
- No withdrawn metrics remain anywhere in the manuscript.

============================================================
15. SECTIONS THAT REQUIRE UPDATE
============================================================

The existing manuscript remains the base.

Only affected portions should be regenerated.

Mandatory review/update areas:

1. Experimental Results and Discussion
2. First-stage retrieval results
3. Retrieval performance table
4. Grounding / claim verification discussion
5. Citation repair discussion
6. Provenance/explainability discussion
7. Iterative refinement discussion
8. Latency table and latency discussion
9. Model configuration wording
10. Limitations and Threats to Validity
11. Conclusion — ONLY sentences containing stale metrics or unsupported claims
12. Figure/table captions and cross-references where affected

Do NOT unnecessarily rewrite:
- Abstract
- Introduction
- Literature Survey
- General Methodology
- Web Platform section

unless an existing statement there directly contradicts the V4 evidence.

============================================================
16. FINAL PAPER SAFETY CHECK
============================================================

Before the research-paper author uses these documents, verify that no manuscript claim suggests:

- Hybrid MRR = 0.3685
- BGE MRR = 0.5444
- BGE +47.7%
- Hybrid Hit@20 = 1.0 on the canonical TEST split
- 11/15 hybrid retrieval success
- Human grounding validation was completed
- Citation repair improved accuracy
- Iterative refinement improved grounding
- Component latency values can be summed to obtain E2E latency
- Gemini 2.5 Flash was the model for every historical/authoritative experiment

The V4 package is the source of truth.
