import re

with open('src/pages/HybridSearchPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add imports
content = content.replace(
  "import { CenteredSheet, SideDrawer, ActionSheet } from '../components/ui/Overlays';",
  "import { CenteredSheet, SideDrawer, ActionSheet } from '../components/ui/Overlays';\nimport { normalizeSearchExperimentResponse, ExperimentStatus } from '../utils/apiAdapter';\nimport LocalProgressPanel from '../components/LocalProgressPanel';\nimport OnlineProgressPanel from '../components/OnlineProgressPanel';\nimport ExperimentOverallStatus from '../components/ExperimentOverallStatus';"
)

# 2. Add state
content = content.replace(
  "  const [isLoading, setIsLoading] = useState(false);",
  "  const [isLoading, setIsLoading] = useState(false);\n  const [activeSearchId, setActiveSearchId] = useState<string | null>(new URLSearchParams(location.search).get('search_id') || null);\n  const [experimentStatus, setExperimentStatus] = useState<ExperimentStatus | null>(null);"
)

# 3. Remove automatic search in useEffect
content = content.replace(
  "  useEffect(() => {\n    if (hasSearched && query.trim()) {\n      performSearch(query, searchMode, publicationYear, sortBy);\n    }\n  }, [searchMode, publicationYear, sortBy]);",
  "  useEffect(() => {\n    if (hasSearched && query.trim() && !activeSearchId) {\n      // removed auto search\n    }\n  }, [searchMode, publicationYear, sortBy]);"
)

# 4. Update performSearch
new_perform = """  const performSearch = async (
    searchQuery: string, 
    mode = searchMode,
    year = publicationYear,
    sort = sortBy
  ) => {
    if (!searchQuery.trim()) return;
    setIsLoading(true);
    setHasSearched(true);
    setResults([]);
    setExperimentStatus(null);
    setRetrievalMeta(null);

    try {
      const response = await api.papers.search({
        query: searchQuery,
        search_mode: mode,
        retrieval_mode: "local_online",
        publication_year: year,
        sort_by: sort
      });
      
      if (response.search_id) {
        setActiveSearchId(response.search_id);
        navigate(`?search_id=${response.search_id}`, { replace: true, state: { query: searchQuery } });
      }
      
      try {
        api.analytics.trackSearch({
          query: searchQuery,
          search_mode: mode,
          domain: activeDomain,
          result_count: 0
        });
      } catch (e) {
        console.error("Analytics tracking failed", e);
      }
      
    } catch (err) {
      console.error("Search failed", err);
      toast.error("Search failed");
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let pollingInterval: NodeJS.Timeout;
    if (activeSearchId) {
      setIsLoading(true);
      setHasSearched(true);
      pollingInterval = setInterval(async () => {
        try {
          const rawStatus = await api.papers.getStatus(activeSearchId);
          const st = normalizeSearchExperimentResponse(rawStatus);
          setExperimentStatus(st);
          
          if (['complete', 'partial', 'failed'].includes(st.overall_status)) {
            clearInterval(pollingInterval);
            setIsLoading(false);
            
            setRetrievalMeta({
              retrieval_source: rawStatus.retrieval_source || 'mixed',
              local_status: st.local.status,
              online_status: st.online.status,
              local_count: st.metrics?.local_metrics?.result_count || 0,
              online_count: st.metrics?.online_metrics?.result_count || 0,
              combined_count: st.metrics?.combined_metrics?.result_count || 0
            });
            
            setResults(rawStatus.results || rawStatus.papers || []);
            
            if (st.trace) {
              st.trace.results = rawStatus.results || [];
              import('../store/researchSessionStore').then(({ useResearchSessionStore }) => {
                const id = useResearchSessionStore.getState().addXaiTrace(st.trace);
                useResearchSessionStore.getState().setActiveTraceId(id);
              });
            }
          }
        } catch (e) {
          console.error("Failed to poll status", e);
          clearInterval(pollingInterval);
          setIsLoading(false);
        }
      }, 1000);
    }
    return () => clearInterval(pollingInterval);
  }, [activeSearchId]);
"""

content = re.sub(r'  const performSearch = async \([\s\S]*?  \};\n', new_perform, content)

# 5. Remove location.state.query auto search
content = content.replace(
  "  useEffect(() => {\n    if (location.state?.query) {\n      setQuery(location.state.query);\n      performSearch(location.state.query);\n    }\n  }, [location.state]);",
  "  useEffect(() => {\n    if (location.state?.query && !hasSearched) {\n      setQuery(location.state.query);\n    }\n  }, [location.state]);"
)

old_ui = """          ) : isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 animate-in fade-in">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-4"></div>
              <div className="text-emerald-700 font-bold flex items-center gap-2">
                <span className="animate-pulse">
                  Searching ResearchNexus...
                </span>
              </div>
            </div>"""
            
new_ui = """          ) : isLoading && experimentStatus ? (
            <div className="flex flex-col gap-4 max-w-4xl mx-auto py-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <LocalProgressPanel local={experimentStatus.local} />
                <OnlineProgressPanel online={experimentStatus.online} />
              </div>
              <ExperimentOverallStatus status={experimentStatus} />
            </div>
          ) : isLoading ? (
            <div className="flex flex-col items-center justify-center py-20 animate-in fade-in">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-4"></div>
              <div className="text-emerald-700 font-bold flex items-center gap-2">
                <span className="animate-pulse">
                  Initializing...
                </span>
              </div>
            </div>"""

content = content.replace(old_ui, new_ui)

content = content.replace(
  "navigate('/assistant', { \n                    state: { \n                      query,\n                      search_mode: searchMode,\n                      selected_papers: selectedPapersContext\n                    }\n                  });",
  "navigate('/assistant', { \n                    state: { \n                      query,\n                      search_mode: searchMode,\n                      selected_papers: selectedPapersContext,\n                      search_id: activeSearchId\n                    }\n                  });"
)

with open('src/pages/HybridSearchPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
