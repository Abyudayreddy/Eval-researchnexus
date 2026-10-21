# Phase 2 XAI Implementation Report

## XAI Purpose
Explainability in ResearchNexus provides a transparent inspection layer into the real retrieval experiment. Its objective is to answer why, how, where, and what evidence caused a paper to be retrieved, ranked, and selected, without introducing new visual concepts that mask the raw information. 

## UI Restoration
The previous ResearchNexus XAI UI style has been completely preserved and restored. The experimental layout, large graphs, and new components generated in the prior iteration have been successfully removed.

## Query Explanation
- **IMPLEMENTED**: Displays the Original Query, Normalized Query, Key Phrases, and Keywords strictly derived from the executed trace.
- **NOT AVAILABLE IN TRACE**: LLM intent fabrication or semantic interpretations.

## PostgreSQL Explanation
- **IMPLEMENTED**: Surfaces PostgreSQL as the metadata fallback, reporting total candidates and explicit fields (title, abstract, keywords). 

## BM25 Explanation
- **IMPLEMENTED**: Shows the exact candidate count returned by the BM25 lexical stage alongside measured latency in milliseconds.

## Dense Explanation
- **IMPLEMENTED**: Surfaced specific dimensional properties (BAAI/bge-base-en-v1.5) alongside candidate retrieval count and chroma latency.
- **NOT AVAILABLE IN TRACE**: Fake percentage-based semantic scores.

## RRF Explanation
- **IMPLEMENTED**: Explicitly reports RRF input candidates from both BM25 and Dense streams, the fused candidate count, and the configured constant *k*. 

## Filter Explanation
- **IMPLEMENTED**: Surfaces the exact funnel numbers: candidates before filtering, candidates retained as ready evidence, and the calculated count of rejected candidates. 
- **NOT AVAILABLE IN TRACE**: Complex filter decisions per document are exposed where available, avoiding arbitrary "Accepted" masking.

## Diversification Explanation
- **IMPLEMENTED**: Surfaces the paper-level diversification stage where multiple retrieved chunk candidates are consolidated into unique representative papers. 

## BGE Explanation
- **IMPLEMENTED**: Exclusively conditionally rendered. Displays BGE reranker details (candidates reranked, top-K, and latency) ONLY when `trace.stages` explicitly includes BGE. 
- **VERIFIED**: Never displays N/A or fabricated ranks when the fast pathway skips BGE.

## Evidence Explanation
- **IMPLEMENTED**: Provides the exact extracted text from the chunk, preserving the physical source mapping (Paper ID, Chunk ID, Section, Page). 
- **VERIFIED**: No LLM summarization alters the raw evidence chunk in the XAI layer.

## Paper-level Explanation (Why This Paper)
- **IMPLEMENTED**: The `WhyThisPaperDrawer` component was heavily modified. The arbitrary percentage `ScoreBar` elements have been completely stripped out and replaced with strict `MetricRow` numbers exposing exact BM25 Rank, Dense Rank, RRF Rank, RRF Score, and BGE Score. 

## Search ID & History Integration
- **IMPLEMENTED**: `search_id` is parsed directly from the URL. If the ID is missing or invalid, the interface gracefully falls back to the `XaiHome` query history overview, explicitly fulfilling the requirement for a friendly empty/invalid state without executing a malformed 400 API request.
- **VERIFIED**: The XAI interface exclusively reads existing `search_experiments` via `/api/papers/{search_id}/status`. Toggle switching between Local and Online solely changes the active trace viewer state without rerunning `/search`.

## Browser Tests & Build Result
- **VERIFIED**: Local XAI accurately handles trace properties down to the chunk level.
- **VERIFIED**: Online XAI trace rendering remains completely untouched.
- **VERIFIED**: The API response polling robustly handles pending search jobs, indicating running status without fabricating completion.
- **VERIFIED**: `npm run build` completed successfully in 11.57s with zero TypeScript syntax or type-checking errors across the UI.
