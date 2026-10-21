# ResearchNexusAI — Technology Stack

| Layer | Component / Tool | Version / Model | Role in Project |
|---|---|---|---|
| **Frontend UI** | React | 18.x | Reactive component rendering |
| **Frontend Language** | TypeScript | 5.x | Type safety across API responses and UI state |
| **Build Tool** | Vite | 5.x | Fast HMR development server & production bundler |
| **State Management** | Zustand | 4.x | Lightweight global store (auth, search, XAI) |
| **Client Routing** | React Router DOM | 6.x | Client-side declarative routing and protected routes |
| **Styling** | TailwindCSS | 3.x | Modern utility-first design system |
| **Backend Framework** | FastAPI | 0.100+ | Asynchronous RESTful API services |
| **Server Engine** | Uvicorn | Standard | ASGI production web server |
| **Database ORM** | SQLAlchemy | 2.x | Relational mapping for papers, chunks, sessions |
| **Relational Store** | SQLite / PostgreSQL | Standard | Persistent metadata, search history, workspaces |
| **Vector Database** | ChromaDB | 0.4+ | Persistent embeddings store for cosine retrieval |
| **Lexical Search** | rank_bm25 | Standard | Fast in-memory Okapi BM25 implementation |
| **Dense Embeddings** | SentenceTransformers | `BAAI/bge-base-en-v1.5` | 768-dimensional neural passage embeddings |
| **Cross-Encoder Reranker**| HuggingFace Transformers | `BAAI/bge-reranker-large` | Query-passage cross-attention rescoring |
| **LLM Synthesis** | Groq / Google Gemini | Llama 3.3 70B / Gemini 1.5 | Multi-paper literature synthesis generation |
