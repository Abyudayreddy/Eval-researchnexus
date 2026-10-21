# ResearchNexus AI — Phase 0: Design System

## Global Style & Vibe
**One ResearchNexus design language.**
- **Style:** Structured, Scholarly, Modern, Interactive, Intelligent, Alive.
- **Avoid:** Generic SaaS layouts, Google Scholar imitation, generic ChatGPT clones, excessive glassmorphism, random neon AI effects, and constant decorative animation.

## Visual Hierarchy
- Large research-oriented headings.
- Clear section hierarchy.
- Strong typography and structured cards.
- Evidence blocks and source badges.
- Semantic spacing and subtle depth.
*(Important information must dominate visually.)*

## Color System
Semantic Colors:
- **Primary / Secondary**
- **Success / Warning / Error**
- **Local:** Distinct color indicating Local PostgreSQL/ChromaDB retrieval.
- **Online:** Distinct color indicating Online Repository retrieval.
- **Evidence / AI / XAI**

*Rule:* Local and Online must remain visually distinguishable, but source colors should not overwhelm the UI.

## Typography
Definitions:
- **Display**, **Heading**, **Subheading**
- **Body**, **Caption**, **Metadata**
- **Code / Technical Evidence**

*Rule:* Prioritize strong readability for paper abstracts, evidence passages, citations, and AI answers. Do not optimize everything for tiny dense text.

## Source Badges
Standard component across all views:
- `[LOCAL]`
- `[ONLINE]`
- `[MIXED]`
- `[UPLOADED]`
Every result and citation uses the exact same badge system.

## Core Reusable Components

### 1. EvidenceCard
Must support:
- Paper title, Source badge
- Section, Page
- Evidence text, Citation
- Actions: [Open Paper], [Explain]

### 2. PaperCard / PaperSummary
Canonical component supporting:
- Title, Authors, Publication data
- Source badge
- Evidence preview
- Actions
*(Reused in Explorer, Library, Projects, Literature Builder).*

### 3. ResearchContextHeader
Shows current context in Assistant / Literature Builder:
- Current mode (e.g., OPEN RESEARCH, THIS PAPER)
- Selected paper(s) / Allowed sources / Search context

## Motion Principles
- Animation communicates state. Use for: retrieval progress, stage transitions, evidence opening, panel expansion, navigation, paper selection, source flow.
- **DO NOT** animate continuously.
- **Live Retrieval Animation:** Animate only active stages reflecting actual backend operations (Query → Local/Online → Evidence → Results). No fake timers or fake progress.
- **XAI Animation:** Animate candidate flow, ranking movement, and evidence selection strictly using actual trace data.
- **AI Response Animation:** Subtle streaming or staged rendering (Understanding → Retrieving → Checking Evidence → Generating) tied to backend states.

## Responsive Design
- **Desktop:** Multi-panel research workspace.
- **Tablet:** Collapsible evidence/context panels.
- **Mobile:** Single-column research flow with bottom sheets/drawers.
*Rule:* No core functionality may depend on hover states.

## Accessibility
- Full keyboard navigation and focus states.
- Proper `aria` labels and screen-reader-friendly source labels.
- Readable contrast.
- Respect `prefers-reduced-motion` for all animated content.
