import re

with open('src/pages/XaiPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace `export default function XaiPage() { ... }` with our new version.

new_page = """export default function XaiPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const searchParams = new URLSearchParams(location.search);
  const searchId = searchParams.get('search_id') || location.state?.search_id;

  const { xaiTraces, activeTraceId, setActiveTraceId, clearXaiHistory } = useResearchSessionStore();
  const [experimentStatus, setExperimentStatus] = useState<ExperimentStatus | null>(null);
  const [activeTab, setActiveTab] = useState<'local' | 'online'>('local');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (searchId) {
      setIsLoading(true);
      let pollingInterval = setInterval(async () => {
        try {
          const rawStatus = await api.papers.getStatus(searchId);
          const st = normalizeSearchExperimentResponse(rawStatus);
          setExperimentStatus(st);
          
          if (['complete', 'partial', 'failed'].includes(st.overall_status)) {
            clearInterval(pollingInterval);
            setIsLoading(false);
          }
        } catch (e) {
          console.error("Failed to poll status", e);
          clearInterval(pollingInterval);
          setIsLoading(false);
        }
      }, 1000);
      return () => clearInterval(pollingInterval);
    } else {
      setActiveTraceId(null);
    }
  }, [searchId, setActiveTraceId]);

  if (!searchId && !activeTraceId) {
    return <XaiHome traces={xaiTraces} onSelect={(id) => navigate(`?search_id=${id}`)} onClear={clearXaiHistory} />;
  }

  if (searchId) {
    if (isLoading && experimentStatus && !['complete', 'partial', 'failed'].includes(experimentStatus.overall_status)) {
      return (
        <div className="h-full flex flex-col items-center justify-center bg-[#FBFDFB]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-4"></div>
          <h2 className="text-xl font-bold text-slate-800">Retrieval is still in progress.</h2>
          <p className="text-slate-500 mt-2">Local: {experimentStatus.local.stage}</p>
          <p className="text-slate-500">Online: {experimentStatus.online.stage}</p>
        </div>
      );
    }

    if (!experimentStatus) {
      return (
        <div className="h-full flex items-center justify-center bg-[#FBFDFB]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
        </div>
      );
    }

    return (
      <div className="h-full flex flex-col">
        <div className="flex justify-center gap-2 p-4 bg-white border-b border-slate-200 shrink-0">
          <button 
            onClick={() => setActiveTab('local')}
            className={`px-4 py-2 text-sm font-bold rounded-lg transition-colors ${activeTab === 'local' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
          >
            [ LOCAL RETRIEVAL ]
          </button>
          <button 
            onClick={() => setActiveTab('online')}
            className={`px-4 py-2 text-sm font-bold rounded-lg transition-colors ${activeTab === 'online' ? 'bg-blue-100 text-blue-800' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
          >
            [ ONLINE RETRIEVAL ]
          </button>
        </div>
        <div className="flex-1 overflow-hidden">
          {activeTab === 'online' && experimentStatus.trace?.online_trace ? (
            <XaiDetail trace={experimentStatus.trace.online_trace} onBack={() => navigate('/xai')} />
          ) : activeTab === 'local' && experimentStatus.trace?.local_trace ? (
            <LocalXaiDetail trace={experimentStatus.trace.local_trace} onBack={() => navigate('/xai')} />
          ) : (
             <div className="flex items-center justify-center h-full text-slate-500">No trace available for this branch.</div>
          )}
        </div>
      </div>
    );
  }

  // Fallback for old traces
  const trace = xaiTraces.find(t => t.id === activeTraceId) || xaiTraces[0];
  if (!trace) {
    return <XaiHome traces={xaiTraces} onSelect={(id) => navigate(`?search_id=${id}`)} onClear={clearXaiHistory} />;
  }
  return <XaiDetail trace={trace} onBack={() => setActiveTraceId(null)} />;
}
"""

# I need to add LocalXaiDetail
local_xai_detail = """
function LocalXaiDetail({ trace, onBack }: { trace: any, onBack: () => void }) {
  if (!trace || !trace.stages) return <div className="p-8 text-center text-slate-500">No local trace data available.</div>;
  return (
    <div className="h-full flex flex-col bg-[#FBFDFB] font-sans overflow-y-auto relative border border-slate-200 rounded-b-xl">
      <header className="px-6 py-4 border-b border-slate-200 bg-white shrink-0 z-10">
        <button onClick={onBack} className="text-xs font-bold text-slate-500 hover:text-slate-800 flex items-center gap-1 mb-2 transition-colors uppercase tracking-wider">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Queries
        </button>
        <h1 className="text-2xl font-black text-emerald-900 mb-1">
          Local Retrieval Timeline
        </h1>
      </header>
      <div className="p-8 max-w-3xl mx-auto w-full">
        <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
          {trace.stages.map((stage: any, idx: number) => (
            <div key={idx} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-slate-100 text-slate-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                <ChevronRight className="w-5 h-5" />
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div className="flex items-center justify-between space-x-2 mb-1">
                  <div className="font-bold text-slate-900 capitalize">{stage.name || stage.stage}</div>
                </div>
                <div className="text-sm text-slate-500">
                  <pre className="whitespace-pre-wrap text-xs bg-slate-50 p-2 rounded mt-2 overflow-x-auto">
                    {JSON.stringify(stage, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""

content = re.sub(r'export default function XaiPage\(\) \{[\s\S]*', local_xai_detail + new_page, content)

with open('src/pages/XaiPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
