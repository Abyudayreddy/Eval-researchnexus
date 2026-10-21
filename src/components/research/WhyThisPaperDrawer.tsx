import { SideDrawer } from '../ui/Overlays';
import { FileText, Activity, Globe } from 'lucide-react';

interface WhyThisPaperDrawerProps {
  paper: any;
}

function MetricRow({ label, value }: { label: string, value: any }) {
  if (value === undefined || value === null) return null;
  return (
    <div className="flex justify-between items-center text-xs py-2 border-b border-slate-100 last:border-0">
      <span className="text-slate-500 font-medium">{label}</span>
      <span className="font-bold text-slate-800">{value}</span>
    </div>
  );
}

export default function WhyThisPaperDrawer({ paper }: WhyThisPaperDrawerProps) {
  if (!paper) return null;

  const isOnline = paper.retrieval_source === 'online';

  return (
    <SideDrawer id="why_this_paper" title="Why this paper?" position="right">
      <div className="space-y-6 pb-8">
        
        <div className="space-y-1">
          <h3 className="font-bold text-slate-900">{paper.title}</h3>
          <p className="text-xs font-medium text-slate-500">{paper.authors}</p>
        </div>

        <div className="bg-slate-50 border border-slate-100 rounded-xl p-4">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5" /> Retrieval Signals
          </h4>
          
          <div className="space-y-0">
            <div className="flex justify-between items-center text-xs pb-2 border-b border-slate-100">
              <span className="text-slate-500 font-medium">Source Pipeline</span>
              <span className="font-bold uppercase tracking-widest text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
                {paper.retrieval_source}
              </span>
            </div>
            
            <MetricRow label="Final Rank" value={paper.rank} />
            <MetricRow label="BM25 Rank" value={paper.bm25_rank} />
            <MetricRow label="Dense Rank" value={paper.dense_rank} />
            <MetricRow label="RRF Rank" value={paper.rrf_rank} />
            <MetricRow label="RRF Score" value={paper.rrf_score?.toFixed(4)} />
            <MetricRow label="Pre-Rerank Rank" value={paper.pre_rerank_rank} />
            <MetricRow label="BGE Rank" value={paper.bge_rank || paper.post_rerank_rank} />
            <MetricRow label="BGE Score" value={paper.bge_score?.toFixed(4) || paper.reranker_score?.toFixed(4)} />
            <MetricRow label="Filter Decision" value={paper.filter_decision || 'Accepted'} />
            
            {isOnline && (
              <MetricRow label="Online Relevance" value={paper.relevance_score} />
            )}
          </div>
        </div>

        {paper.evidence_text && (
          <div className="border border-emerald-100 rounded-xl overflow-hidden">
            <div className="bg-emerald-50 px-4 py-2 border-b border-emerald-100 flex items-center justify-between">
              <h4 className="text-[10px] font-bold text-emerald-700 uppercase tracking-widest flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5" /> Supporting Evidence
              </h4>
              {paper.section && (
                 <span className="text-[10px] font-bold text-emerald-600 bg-white px-2 py-0.5 rounded border border-emerald-100 shadow-sm">
                   Section: {paper.section} {paper.page_start ? `| Page ${paper.page_start}` : ''}
                 </span>
              )}
            </div>
            <div className="p-4 bg-white">
              <p className="text-sm text-slate-700 italic font-serif leading-relaxed">
                "...{paper.evidence_text}..."
              </p>
            </div>
          </div>
        )}
        
        {(!paper.evidence_text && isOnline) && (
          <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
             <h4 className="text-[10px] font-bold text-blue-700 uppercase tracking-widest mb-2 flex items-center gap-1.5">
                <Globe className="w-3.5 h-3.5" /> Online Source
              </h4>
              <p className="text-sm text-slate-600">
                This result was retrieved via the {paper.source_repository || 'online'} connector based on semantic metadata match. Direct localized evidence extraction is not available for online-only results.
              </p>
          </div>
        )}

      </div>
    </SideDrawer>
  );
}
