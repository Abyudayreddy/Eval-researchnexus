const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || "http://localhost:8000/api";

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  // Assuming JWT token will be stored in localStorage after auth
  const token = localStorage.getItem("researchnexus_token");
  
  const headers = new Headers(options.headers || {});
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const detailMsg = typeof errorData.detail === 'string' 
      ? errorData.detail 
      : (Array.isArray(errorData.detail) ? errorData.detail.map((e: any) => e.msg).join(', ') : `API call failed: ${response.statusText}`);
    throw new Error(detailMsg);
  }
  
  return response.json();
}

export const api = {
  auth: {
    login: (data: any) => {
      const formData = new URLSearchParams();
      formData.append('username', data.email);
      formData.append('password', data.password);
      return fetchWithAuth("/auth/login", { 
        method: "POST", 
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData 
      });
    },
    register: (data: any) => fetchWithAuth("/auth/register", { method: "POST", body: JSON.stringify(data) }),
    me: () => fetchWithAuth("/auth/me"),
    updateProfile: (data: any) => fetchWithAuth("/auth/profile", { method: "PUT", body: JSON.stringify(data) })
  },
  dashboard: {
    getStats: () => fetchWithAuth("/dashboard/stats"),
  },
  papers: {
    getDomainCounts: () => fetchWithAuth("/papers/domain-counts"),
    getDomainPapers: (domainId: string) => fetchWithAuth(`/papers/domain/${domainId}`),
    search: (params: { query: string; search_mode?: string; retrieval_mode?: string; publication_year?: string | null; sort_by?: string; domain?: string }) => fetchWithAuth("/papers/search", { 
      method: "POST", 
      body: JSON.stringify(params) 
    }),
    getStatus: (searchId: string) => fetchWithAuth(`/papers/${searchId}/status`),
    get: (id: string) => fetchWithAuth(`/papers/${id}`),
  },
  documents: {
    upload: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      const token = localStorage.getItem("researchnexus_token");
      const headers: Record<string, string> = {};
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        headers,
        body: formData
      });
      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Document upload failed");
      }
      return response.json();
    },
    getStatus: (documentId: string) => fetchWithAuth(`/documents/${documentId}/status`),
    getDetails: (documentId: string) => fetchWithAuth(`/documents/${documentId}`)
  },
  ai: {
    ask: (query: string, searchMode: string = "hybrid", contextPapers?: any[], searchId?: string, extraParams?: Record<string, any>) => fetchWithAuth("/ai/ask", {
      method: "POST",
      body: JSON.stringify({ query, search_mode: searchMode, context_papers: contextPapers, search_id: searchId, ...(extraParams || {}) })
    }),
    compare: (paperIds: string[], searchId?: string, query?: string) => fetchWithAuth("/ai/compare", {
      method: "POST",
      body: JSON.stringify({
        query: query || "Multi-paper dimension comparison",
        paper_ids: paperIds,
        search_id: searchId,
        mode: "compare"
      })
    }),
    getComparison: (comparisonId: string) => fetchWithAuth(`/ai/comparison/${comparisonId}`),
    explain: (session_id: string) => fetchWithAuth(`/ai/explain?session_id=${session_id}`)
  },
    projects: {
    getAll: () => fetchWithAuth("/projects/"),
    create: (data: any) => fetchWithAuth("/projects/", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: any) => fetchWithAuth(`/projects/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    delete: (id: string) => fetchWithAuth(`/projects/${id}`, { method: "DELETE" }),
    addPaper: (projectId: string, paperId: string, metadata: any) => fetchWithAuth(`/projects/${projectId}/papers`, { method: "POST", body: JSON.stringify({ paper_id: paperId, ...metadata }) }),
    removePaper: (projectId: string, paperId: string) => fetchWithAuth(`/projects/${projectId}/papers/${encodeURIComponent(paperId)}`, { method: "DELETE" }),
    getPapers: (projectId: string) => fetchWithAuth(`/projects/${projectId}/papers`),
    getNotes: (projectId: string) => fetchWithAuth(`/projects/${projectId}/notes`)
  },
    notes: {
    getAll: (params?: { project_id?: string, paper_id?: string }) => {
      let query = "";
      if (params) {
        const urlParams = new URLSearchParams();
        if (params.project_id) urlParams.append("project_id", params.project_id);
        if (params.paper_id) urlParams.append("paper_id", params.paper_id);
        query = "?" + urlParams.toString();
      }
      return fetchWithAuth(`/notes/${query}`);
    },
    create: (data: any) => fetchWithAuth("/notes/", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: any) => fetchWithAuth(`/notes/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    delete: (id: string) => fetchWithAuth(`/notes/${id}`, { method: "DELETE" })
  },
  bookmarks: {
    getAll: () => fetchWithAuth("/bookmarks/"),
    add: (paper: any) => fetchWithAuth("/bookmarks/", { method: "POST", body: JSON.stringify({ paper }) }),
    remove: (paperId: string) => fetchWithAuth(`/bookmarks/${encodeURIComponent(paperId)}`, { method: "DELETE" })
  },
  analytics: {
    trackSearch: async (payload: { query: string, search_mode?: string, domain?: string, subdomain?: string, result_count?: number }) => {
      try {
        await fetchWithAuth('/analytics/search', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
      } catch (error) {
        console.error("Analytics trackSearch failed:", error);
      }
    },
    trackPaperView: async (paperId: string) => {
      try {
        await fetchWithAuth('/analytics/paper_view', {
          method: 'POST',
          body: JSON.stringify({ paper_id: paperId }),
        });
      } catch (error) {
        console.error("Analytics trackPaperView failed:", error);
      }
    },
    getOverview: async () => {
      return fetchWithAuth('/analytics/overview');
    }
  },
  goals: {
    getAll: () => fetchWithAuth("/goals/"),
    create: (data: any) => fetchWithAuth("/goals/", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: any) => fetchWithAuth(`/goals/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    delete: (id: string) => fetchWithAuth(`/goals/${id}`, { method: "DELETE" })
  },
  literatureReview: {
    synthesize: (paperIds: string[]) => fetchWithAuth("/literature-review/synthesize", {
      method: "POST",
      body: JSON.stringify({ paper_ids: paperIds })
    })
  },
  history: {
    getAll: () => fetchWithAuth("/history/"),
    delete: (id: string) => fetchWithAuth(`/history/${id}`, { method: "DELETE" }),
    update: (id: string, data: any) => fetchWithAuth(`/history/${id}`, { method: "PATCH", body: JSON.stringify(data) })
  }
};

