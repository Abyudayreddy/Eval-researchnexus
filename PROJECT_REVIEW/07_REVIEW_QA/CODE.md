# ResearchNexusAI — Code Level Questions

### 1. What are the key entry points for backend and frontend?
- **Answer:** Frontend entry is `src/main.tsx` leading into `src/App.tsx`. Backend entry is `backend/app/main.py` which mounts FastAPI routers.

### 2. How is client-side authentication enforced in `src/App.tsx`?
- **Answer:** A `ProtectedRoute` wrapper component intercepts protected routes, triggers `checkAuth()` from the Zustand store, displays a loading state during verification, and replaces the URL with `/login` if unauthenticated.

### 3. In `retrieval.py`, why is $k=60$ used in RRF?
- **Answer:** $k=60$ is the established standard from Cormack et al. (SIGIR 2009). It prevents top-ranked documents in one system from overwhelmingly dominating candidates that appear consistently across multiple systems.

### 4. How does `claim_verifier.py` classify factual claims?
- **Answer:** It evaluates Natural Language Inference (NLI) entailment to output: Entailed (supported by chunk), Contradicted (directly conflicts), or Unverified (insufficient context proof).
