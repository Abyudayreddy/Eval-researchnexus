import re

with open('src/pages/XaiPage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's completely rewrite LocalXaiDetail
new_local_xai_detail = """
function LocalXaiDetail({ trace, results, onBack }: { trace: any, results: any[], onBack: () => void }) {
  if (!trace) return <div className="p-8 text-center text-slate-500">No local trace data available.</div>;

  const localResults = results.filter(r => r.retrieval_source === 'local' || r.retrieval_source === 'mixed');
  const latencies = trace.latencies || {};

  const Section = ({ title, children }: { title: string, children: React.ReactNode }) => (
    <div className="bg-white border border-slate-200 rounded-xl p-5 mb-4 shadow-sm">
      <h3 className="font-black text-slate-800 text-sm mb-3 border-b border-slate-100 pb-2">{title}</h3>
      <div className="text-sm text-slate-600 space-y-2">
        {children}
      </div>
    </div>
  );

  const Item = ({ label, value }: { label: string, value: any }) => (
    <div className="flex justify-between items-start gap-4">
      <span className="font-bold text-slate-500 min-w-[140px] text-xs">{label}</span>
      <span className="text-slate-800 text-right flex-1 break-words">{value !== undefined && value !== null ? value : <span className="italic text-slate-400">Not available from source trace.</span>}</span>
    </div>
  );

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
      
      <div className="p-6 max-w-4xl mx-auto w-full space-y-6">
        
        <Section title="A. Query Understanding">
          <Item label="Original Query" value={trace.query} />
          <Item label="Normalized Query" value={trace.search_query} />
          <Item label="Extracted Keywords" value={undefined} />
          <Item label="Extracted Phrases" value={undefined} />
          <Item label="Domain/Subdomain" value={undefined} />
        </Section>

        <Section title="B. Structured Retrieval">
          <Item label="PostgreSQL Fields" value={undefined} />
          <Item label="Candidate Count" value={undefined} />
          <Item label="Actual Latency" value={undefined} />
        </Section>

        <Section title="C. Keyword Retrieval">
          <Item label="Algorithm" value="BM25" />
          <Item label="Candidate Count" value={trace.candidates} />
          <Item label="Latency" value={latencies.bm25 ? `${(latencies.bm25 * 1000).toFixed(1)}ms` : undefined} />
          <Item label="Top Ranks/Scores" value={undefined} />
        </Section>

        <Section title="D. Semantic Retrieval">
          <Item label="Model" value="BAAI/bge-base-en-v1.5" />
          <Item label="Embedding Dimension" value={undefined} />
          <Item label="Candidate Count" value={trace.candidates} />
          <Item label="Latency" value={latencies.dense ? `${(latencies.dense * 1000).toFixed(1)}ms` : undefined} />
        </Section>

        <Section title="E. RRF Fusion">
          <Item label="Input Candidates" value={trace.candidates} />
          <Item label="RRF k value" value={trace.rrf_k || 60} />
          <Item label="Fused Candidate Count" value={trace.candidates} />
          <Item label="Latency" value={latencies.rrf ? `${(latencies.rrf * 1000).toFixed(1)}ms` : undefined} />
        </Section>

        <Section title="F. Local Relevance Filtering">
          <Item label="Before Filter" value={trace.candidates} />
          <Item label="After Filter" value={trace.evidence_ready} />
          <Item label="Filtering Criteria" value={undefined} />
          <Item label="Latency" value={latencies.build ? `${(latencies.build * 1000).toFixed(1)}ms` : undefined} />
        </Section>

        <Section title="G. BGE Reranking">
          <Item label="Model" value="BAAI/bge-reranker-base" />
          <Item label="Candidates Reranked" value={trace.stages?.includes('BGE Reranking') ? trace.evidence_ready : 'Not used'} />
          <Item label="Final Top-K" value={localResults.length} />
          <Item label="Reranking Score" value={undefined} />
          <Item label="Latency" value={undefined} />
        </Section>

        <Section title="H. Evidence">
          {localResults.length === 0 ? (
            <div className="text-slate-400 italic">No local evidence available.</div>
          ) : (
            <div className="space-y-4">
              {localResults.map((r, i) => (
                <div key={i} className="bg-slate-50 p-4 rounded border border-slate-200">
                  <div className="font-bold text-slate-800 text-xs mb-1">{r.title}</div>
                  <div className="text-emerald-700 text-[10px] mb-2">{r.authors}</div>
                  <Item label="Paper ID" value={r.id || r.paper_id} />
                  <Item label="Chunk ID" value={r.chunk_id} />
                  <Item label="Section" value={r.section} />
                  <Item label="Page" value={r.page} />
                  <div className="mt-3">
                    <span className="font-bold text-slate-500 text-xs block mb-1">Evidence Text:</span>
                    <p className="text-xs text-slate-700 bg-white p-2 rounded border border-slate-100">{r.evidence_text || <span className="italic text-slate-400">Not available from source trace.</span>}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Section>

        <Section title="I. Final Local Ranking">
          <Item label="Ranking Reason" value={undefined} />
        </Section>

        <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5 mb-8">
          <h3 className="font-black text-emerald-900 text-lg mb-3">Local Retrieval Summary</h3>
          <Item label="Candidate Count" value={trace.candidates} />
          <Item label="Final Count" value={localResults.length} />
          <Item label="Total Latency" value={trace.total_latency ? `${(trace.total_latency * 1000).toFixed(1)}ms` : undefined} />
        </div>
      </div>
    </div>
  );
}
"""

content = re.sub(r'function LocalXaiDetail\(\{ trace, onBack \}: \{ trace: any, onBack: \(\) => void \}\) \{[\s\S]*?\}\n(?=export default function XaiPage)', new_local_xai_detail, content)

# I must update the call to LocalXaiDetail to pass `results`
content = content.replace("<LocalXaiDetail trace={experimentStatus.trace.local_trace} onBack={() => navigate('/xai')} />", "<LocalXaiDetail trace={experimentStatus.trace.local_trace} results={experimentStatus.results || []} onBack={() => navigate('/xai')} />")

with open('src/pages/XaiPage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
