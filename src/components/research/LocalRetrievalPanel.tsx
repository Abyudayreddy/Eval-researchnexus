import { Database, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { cn } from '../../utils/cn';

interface LocalRetrievalPanelProps {
  status: {
    status: string;
    stage: string;
    progress: number | null;
    result_count?: number;
    trace?: any;
    latency?: number;
  };
}

export default function LocalRetrievalPanel({ status }: LocalRetrievalPanelProps) {
  const isComplete = status.status === 'success' || status.status === 'complete' || status.status === 'insufficient';
  const isNoResults = status.status === 'no_results' || status.status === 'insufficient'; // legacy mapping
  const isFailed = status.status === 'failed';
  const isRunning = !isComplete && !isFailed && !isNoResults;

  const getStages = () => {
    if (status.trace?.stages && status.trace.stages.length > 0) {
      return status.trace.stages;
    }
    if (isComplete && !isNoResults) return ['Query Analysis', 'PostgreSQL', 'BM25 + ChromaDB', 'RRF', 'Relevance Filtering', 'Evidence Selection'];
    if (isNoResults) return ['Query Analysis', 'PostgreSQL', 'BM25 + ChromaDB', 'RRF', 'Relevance Filtering', 'No relevant evidence found'];
    if (isFailed) return ['Query Analysis', 'Index Lookup', 'Retrieval Halted (Technical Failure)'];
    return [status.stage || 'Waiting...'];
  };

  const stages = getStages();
  const currentStageIndex = isRunning ? stages.length - 1 : stages.length;

  return (
    <div className={cn("p-6 border rounded-2xl shadow-sm bg-white/80 backdrop-blur-sm relative overflow-hidden transition-all duration-500",
      (isComplete || isNoResults) ? "border-emerald-200" : isFailed ? "border-rose-200" : "border-emerald-300 ring-4 ring-emerald-500/10"
    )}>
      {/* Accent Background Glow */}
      <div className={cn("absolute inset-0 opacity-10 bg-gradient-to-br transition-colors duration-1000",
        (isComplete || isNoResults) ? "from-emerald-400 to-transparent" : isFailed ? "from-rose-400 to-transparent" : "from-emerald-500 via-transparent to-transparent"
      )} />

      <div className="relative z-10 flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className={cn("p-2 rounded-xl border", (isComplete || isNoResults) ? "bg-emerald-50 border-emerald-100" : isFailed ? "bg-rose-50 border-rose-100" : "bg-emerald-50 border-emerald-200 animate-pulse")}>
            <Database className={cn("w-5 h-5", (isComplete || isNoResults) ? "text-emerald-600" : isFailed ? "text-rose-600" : "text-emerald-600")} />
          </div>
          <div>
            <h3 className="font-black text-slate-800 tracking-tight">LOCAL RESEARCH</h3>
            <p className={cn("text-[10px] font-bold uppercase tracking-widest", (isComplete || isNoResults) ? "text-emerald-600" : isFailed ? "text-rose-600" : "text-emerald-500 animate-pulse")}>
              {isNoResults ? 'No Results' : isComplete ? 'Complete' : isFailed ? 'Failed' : 'Running...'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {isRunning && <Loader2 className="w-5 h-5 text-emerald-500 animate-spin" />}
          {(isComplete || isNoResults) && <CheckCircle2 className="w-6 h-6 text-emerald-500" />}
          {isFailed && <AlertCircle className="w-6 h-6 text-rose-500" />}
        </div>
      </div>

      <div className="relative z-10 space-y-4 pl-4 border-l-2 border-slate-100 py-2">
        {stages.map((st: string, idx: number) => {
          const isDone = isComplete || isNoResults || (isRunning && idx < currentStageIndex);
          const isCurrent = isRunning && idx === currentStageIndex;
          const isThisStageFailed = isFailed && idx === stages.length - 1;
          
          return (
            <div key={idx} className="relative flex items-center gap-3">
              {/* Vertical node indicator */}
              <div className={cn("absolute -left-[21px] w-2.5 h-2.5 rounded-full border-2 transition-all duration-300 bg-white",
                isDone ? "border-emerald-500 bg-emerald-500 scale-110" :
                isThisStageFailed ? "border-rose-500 bg-rose-500 scale-110" :
                isCurrent ? "border-emerald-500 ring-4 ring-emerald-500/20" :
                "border-slate-300"
              )} />
              <span className={cn("text-sm font-semibold transition-colors duration-300", 
                isDone ? "text-slate-700" : isThisStageFailed ? "text-rose-700" : isCurrent ? "text-emerald-700" : "text-slate-400"
              )}>
                {st}
              </span>
              {isDone && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 opacity-70" />}
              {isThisStageFailed && <AlertCircle className="w-3.5 h-3.5 text-rose-500 opacity-70" />}
              {isCurrent && <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />}
            </div>
          );
        })}
      </div>

      <div className="relative z-10 mt-6 pt-4 border-t border-slate-100 flex justify-between items-center text-xs">
        {status.latency !== undefined ? (
          <span className="text-slate-400 font-bold font-mono uppercase tracking-widest">{status.latency.toFixed(2)}s</span>
        ) : (
          <span className="text-slate-400 font-bold uppercase tracking-widest">PostgreSQL • Chroma</span>
        )}
        
        {(isComplete || isNoResults) && status.result_count !== undefined && (
          <span className="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-lg font-black shadow-sm">
            {status.result_count} Candidates
          </span>
        )}
      </div>
    </div>
  );
}
