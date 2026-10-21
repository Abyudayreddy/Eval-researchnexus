# ResearchNexus AI — Phase 0: Research Principles

## 1. Unified Evidence Principle
The fundamental relationship chain is strictly hierarchical:
`QUESTION → PAPER → EVIDENCE → CLAIM → ANSWER`

- **Local:** `chunk_id` → `paper_id` → PostgreSQL metadata → evidence text.
- **Online:** Existing online paper/evidence structure.
- **Strict Rule:** The UI and AI must NEVER invent or fabricate source information, missing metadata, page numbers, sections, or passages.

## 2. Context Control
The AI Assistant is strictly context-controlled through `ResearchContext` modes (Open Research, Single Paper, Multi Paper, Uploaded Document, Project).
- **Strict Rule:** The Assistant must NEVER silently broaden its allowed evidence context. If the provided evidence is insufficient to answer a claim, it must return an honest limitation rather than hallucinating.

## 3. Grounding & Provenance
The UI must make the following visible and unambiguous at all times:
- Source
- Evidence
- Provenance
- Context
- Limitations

The user should always be able to answer:
- What was searched?
- Where did this come from?
- Why was it selected?
- What evidence supports it?
- What context is the AI using?

## 4. Explainability (XAI) Rule
Explainability is distinct from Answering.
- XAI exclusively answers "HOW did we retrieve this?"
- It reflects reality: every trace stage must represent an operation that was actually executed by the backend. Do not invent missing internal stages for external/online APIs.

## 5. Canonical Proof Chain
CLAIM → CITATION → PAPER → SECTION → PAGE → EVIDENCE
- When evidence or specific placement data (like page numbers) is unavailable, state it clearly. Do not fabricate placement data.

## 6. Research Paper Alignment
All major architecture and UX decisions exist to support measurable research experiments. Features and changes will be evaluated against:
- Retrieval quality and latency
- Source diversity
- Reranking effectiveness
- Grounding and citation correctness
- Evidence coverage
- Explainability clarity
- User workflow efficiency

*Strict Rule:* Do not claim improvements or use labels like "Enhanced RAG" purely for marketing. Claims must be measurable and aligned with the architectural definition.
