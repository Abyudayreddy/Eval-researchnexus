import re

with open('src/pages/XaiPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure normalizeSearchId is imported
if 'normalizeSearchId' not in content:
    content = content.replace('normalizeSearchExperimentResponse, ExperimentStatus', 'normalizeSearchExperimentResponse, ExperimentStatus, normalizeSearchId')

xai_page_start = """export default function XaiPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const searchParams = new URLSearchParams(location.search);
  const rawSearchId = searchParams.get('search_id') || location.state?.search_id;
  const searchId = normalizeSearchId(rawSearchId);

  const { xaiTraces, activeTraceId, setActiveTraceId, clearXaiHistory } = useResearchSessionStore();
  const [experimentStatus, setExperimentStatus] = useState<ExperimentStatus | null>(null);
  const [activeTab, setActiveTab] = useState<'local' | 'online'>('local');
  const [isLoading, setIsLoading] = useState(false);
  const [errorStatus, setErrorStatus] = useState<number | null>(null);

  useEffect(() => {
    if (searchId) {
      setIsLoading(true);
      setErrorStatus(null);
      let pollingInterval = setInterval(async () => {
        try {
          if (process.env.NODE_ENV === 'development') {
            console.log('[XAI] search_id =', searchId);
            console.log('[XAI] status URL =', `/api/papers/${encodeURIComponent(searchId)}/status`);
          }
          const rawStatus = await api.papers.getStatus(searchId);
          const st = normalizeSearchExperimentResponse(rawStatus);
          setExperimentStatus(st);
          
          if (['complete', 'partial', 'failed'].includes(st.overall_status)) {
            clearInterval(pollingInterval);
            setIsLoading(false);
          }
        } catch (e: any) {
          console.error("Failed to poll status", e);
          clearInterval(pollingInterval);
          setIsLoading(false);
          
          // Basic status extraction assuming fetch or axios
          const status = e.response?.status || e.status || (e.message?.includes('400') ? 400 : e.message?.includes('404') ? 404 : e.message?.includes('401') || e.message?.includes('403') ? 401 : 500);
          setErrorStatus(status);
        }
      }, 1000);
      return () => clearInterval(pollingInterval);
    } else {
      setActiveTraceId(null);
    }
  }, [searchId, setActiveTraceId]);

  if (!searchId) {
    return <XaiHome traces={xaiTraces} onSelect={(id) => navigate(`?search_id=${id}`)} onClear={clearXaiHistory} />;
  }

  if (errorStatus === 400) {
    return <div className="h-full flex items-center justify-center p-8 text-center text-slate-500 font-medium">Invalid research search reference.</div>;
  }
  if (errorStatus === 404) {
    return <div className="h-full flex items-center justify-center p-8 text-center text-slate-500 font-medium">Research search not found. Run a new search from Research Explorer.</div>;
  }
  if (errorStatus === 401 || errorStatus === 403) {
    return <div className="h-full flex items-center justify-center p-8 text-center text-slate-500 font-medium">You are not authorized to view this research search.</div>;
  }
  if (errorStatus) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center text-slate-500 font-medium">
        Research explainability is temporarily unavailable.
        <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 bg-emerald-100 text-emerald-700 font-bold rounded-lg hover:bg-emerald-200">Retry</button>
      </div>
    );
  }

  if (searchId) {
    if (isLoading && experimentStatus && !['complete', 'partial', 'failed'].includes(experimentStatus.overall_status)) {
"""
content = re.sub(r'export default function XaiPage\(\) \{[\s\S]*?if \(isLoading && experimentStatus && !\[\'complete\', \'partial\', \'failed\'\]\.includes\(experimentStatus\.overall_status\)\) \{', xai_page_start, content)

with open('src/pages/XaiPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
