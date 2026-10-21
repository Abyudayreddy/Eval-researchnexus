# ResearchNexus AI — Phase 0: UX Architecture

## Core Navigation
Primary Navigation Architecture:
- **Explorer**
- **Assistant**
- **XAI**
- **Literature Builder**
- **Projects**
- **Library**
- **Notebook**

Supporting modules (Dashboard, Analytics, Settings, Notifications) must remain accessible but secondary to the core scientific research flow.

## Module UX Definitions

### 1. Research Explorer UX
- **Purpose:** Primary discovery engine ("What should I read?").
- **Flow:** Submit query → View live retrieval state (Local/Online) → See source provenance → Explore relevant papers → Read extracted evidence.
- **Rules:** Links deeply to XAI and AI Assistant. Should NOT become a long-form synthesis page.

### 2. AI Research Assistant UX
- **Purpose:** Understanding engine ("What does this research tell me?").
- **Context Modes:** Open Research, Single Paper, Multi Paper, Project Research, Uploaded Research.
- **Rules:** Must explicitly show its allowed context using the `ResearchContextHeader`. Grounded in evidence.

### 3. XAI UX
- **Purpose:** Explainability engine ("Why did this result appear?").
- **Structure:** Two independent tabs: `[ LOCAL RETRIEVAL ]` and `[ ONLINE RETRIEVAL ]`.
- **Rules:** No single merged ambiguous timeline. Shows actual query understanding, retrieval, ranking, provenance, and timing. Must not act as an AI answer page.

### 4. Literature Builder UX
- **Purpose:** Synthesis engine ("What does the body of literature collectively show?").
- **Flow:** Collect → Organize → Extract Evidence → Compare → Synthesize → Review → Export.

### 5. Projects UX
- **Purpose:** Persistent research workspace.
- **Rules:** Contains papers, evidence, questions, literature work, notes. Does NOT introduce a separate retrieval engine.

### 6. Notebook & Library UX
- **Notebook:** Stores notes, paper/evidence references. Preserves strict provenance.
- **Library:** Curates saved papers and collections without independent retrieval architecture.

## Persistent Research Context Flow
When moving between modules (e.g., Explorer → Assistant → XAI → Literature Builder), the system must **preserve**:
- `search_id`
- Selected papers
- Active research context

*Rule:* Do not automatically start new searches when navigating between tools.

## URL Rules
Use query parameters to maintain durable research context:
- `/xai?search_id=...`
- `/assistant?search_id=...`
- `/literature?context_id=...`
(Router state is acceptable as a fallback).

## Error Design & Empty States
### Contextual Errors
- **Local Failure:** "Local retrieval failed. Online research remains available."
- **Online Failure:** "Online retrieval failed. Local research remains available."
- **Combined Failure:** "Unable to retrieve sufficient evidence."
*Rule:* Do not show raw stack traces in the UI.

### Empty States
Teach the user what to do:
- **Explorer:** "Ask a research question to begin."
- **Assistant:** "Select a research focus to begin."
- **XAI:** "Run a research search to generate an explainability trace."
- **Literature Builder:** "Add papers to begin building your literature review."
