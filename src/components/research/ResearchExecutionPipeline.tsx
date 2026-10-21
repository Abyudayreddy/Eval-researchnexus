import { ExperimentStatus, PipelineStage, ExecutionState } from '../../utils/apiAdapter';
import { Check, AlertCircle } from 'lucide-react';
import { cn } from '../../utils/cn';

interface ResearchExecutionPipelineProps {
  status: ExperimentStatus | null;
  query?: string;
}

type StepStatus = 'completed' | 'running' | 'pending' | 'failed';

interface PipelineStep {
  id: string;
  title: string;
  subtitle: string;
  status: StepStatus;
}

export const ResearchExecutionPipeline: React.FC<ResearchExecutionPipelineProps> = ({ status, query }) => {
  if (!status) return null;

  const execState = status.execution_state || 'INITIALIZING';
  const currentStage = status.current_stage || (status.terminal ? "RESULTS_READY" : "QUERY_PROCESSING");
  const isTerminal = Boolean(status.terminal);

  const getStepStatuses = (): PipelineStep[] => {
    // Stage Order
    const stageOrder: PipelineStage[] = [
      "QUERY_PROCESSING",
      "LOCAL_RETRIEVAL",
      "RESULT_FUSION",
      "BGE_RERANKING",
      "ONLINE_RESEARCH",
      "EVIDENCE_PREPARATION",
      "RESULTS_READY"
    ];

    const currentIdx = isTerminal ? stageOrder.length - 1 : stageOrder.indexOf(currentStage);

    const getStageStatus = (stage: PipelineStage, stateReqs: ExecutionState[]): StepStatus => {
      const idx = stageOrder.indexOf(stage);
      if (isTerminal) {
        return execState === 'FAILED' && stage === 'RESULTS_READY' ? 'failed' : 'completed';
      }
      if (currentStage === stage || stateReqs.includes(execState)) {
        return 'running';
      }
      if (currentIdx > idx || idx < stageOrder.indexOf(currentStage)) {
        return 'completed';
      }
      return 'pending';
    };

    return [
      {
        id: 'query',
        title: 'Query Processing',
        subtitle: query ? `Understanding "${query}"` : 'Understanding your research question',
        status: getStageStatus("QUERY_PROCESSING", ["INITIALIZING"])
      },
      {
        id: 'local_retrieval',
        title: 'Local Retrieval',
        subtitle: 'PostgreSQL metadata • BM25 keywords • ChromaDB vectors',
        status: getStageStatus("LOCAL_RETRIEVAL", ["LOCAL_RETRIEVING"])
      },
      {
        id: 'result_fusion',
        title: 'Result Fusion',
        subtitle: 'Combining keyword and semantic results using RRF',
        status: getStageStatus("RESULT_FUSION", ["MERGING"])
      },
      {
        id: 'reranking',
        title: 'Re-ranking',
        subtitle: 'BGE Cross-Encoder refining evidence relevance',
        status: getStageStatus("BGE_RERANKING", ["RERANKING"])
      },
      {
        id: 'online_research',
        title: 'Online Research',
        subtitle: 'Searching academic sources (Crossref • OpenAlex)',
        status: getStageStatus("ONLINE_RESEARCH", ["ONLINE_RETRIEVING"])
      },
      {
        id: 'evidence_prep',
        title: 'Evidence Preparation',
        subtitle: 'Deduplicating evidence and assembling context',
        status: getStageStatus("EVIDENCE_PREPARATION", ["EVIDENCE_ASSEMBLY"])
      },
      {
        id: 'results_ready',
        title: 'Results Ready',
        subtitle: 'Combining the strongest local and online evidence',
        status: isTerminal ? (execState === 'FAILED' ? 'failed' : 'completed') : 'pending'
      }
    ];
  };

  const steps = getStepStatuses();

  // Dynamic counter display based on canonical accumulation
  const localCountDisplay = isTerminal || status.local?.status === 'complete' ? String(status.local?.result_count || 0) : 'retrieving…';
  const onlineCountDisplay = isTerminal || status.online?.status === 'complete' ? String(status.online?.result_count || 0) : (execState === 'ONLINE_RETRIEVING' ? 'searching…' : String(status.online?.result_count || 0));
  const uniqueCountDisplay = isTerminal || ['MERGING', 'RERANKING', 'EVIDENCE_ASSEMBLY'].includes(execState) ? String(status.combined_result_count || (status.results ? status.results.length : 0)) : 'merging…';
  const evidenceBlocksCountDisplay = isTerminal ? String(status.results ? status.results.filter(r => r.evidence_text || r.abstract).length : 0) : 'preparing…';

  const renderIcon = (st: StepStatus) => {
    switch (st) {
      case 'completed':
        return (
          <div className="w-4 h-4 rounded-full bg-emerald-500 text-white flex items-center justify-center shrink-0">
            <Check className="w-2.5 h-2.5 stroke-[3]" />
          </div>
        );
      case 'running':
        return (
          <div className="w-4 h-4 rounded-full bg-emerald-100 border border-emerald-500 text-emerald-600 flex items-center justify-center shrink-0 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          </div>
        );
      case 'failed':
        return (
          <div className="w-4 h-4 rounded-full bg-rose-500 text-white flex items-center justify-center shrink-0">
            <AlertCircle className="w-2.5 h-2.5 stroke-[3]" />
          </div>
        );
      case 'pending':
      default:
        return (
          <div className="w-4 h-4 rounded-full border border-slate-300 bg-slate-50 flex items-center justify-center shrink-0">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-300"></span>
          </div>
        );
    }
  };

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-sm space-y-4 font-sans text-xs">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2 font-bold text-slate-800 text-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span>Research Execution Pipeline</span>
        </div>
        <span className={cn("px-2.5 py-0.5 rounded-full font-bold text-[10px] uppercase tracking-wider",
          isTerminal ? "bg-emerald-50 text-emerald-700 border border-emerald-200" : "bg-blue-50 text-blue-700 border border-blue-200 animate-pulse"
        )}>
          {isTerminal ? 'Execution Completed' : 'Pipeline Active'}
        </span>
      </div>

      <div className="space-y-3 py-1">
        {steps.map((step) => (
          <div key={step.id} className="flex items-start gap-3 transition-all">
            <div className="mt-0.5">{renderIcon(step.status)}</div>
            <div className="flex-1 min-w-0">
              <div className={cn("font-bold text-xs leading-none", 
                step.status === 'completed' ? "text-slate-800" : 
                step.status === 'running' ? "text-emerald-700" : 
                step.status === 'failed' ? "text-rose-600" : "text-slate-400"
              )}>
                {step.title}
              </div>
              <div className={cn("text-[11px] mt-0.5 truncate",
                step.status === 'running' ? "text-emerald-600 font-medium" : "text-slate-500"
              )}>
                {step.subtitle}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* METRICS COUNTER BAR */}
      <div className="pt-3 border-t border-inherit/20 flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-500 -mx-5 -mb-5 px-5 py-3 rounded-b-2xl bg-slate-50/80">
        <div className="flex items-center gap-3">
          <span>Local: <strong className="text-emerald-500 font-bold">{localCountDisplay}</strong></span>
          <span className="opacity-40">•</span>
          <span>Online: <strong className="text-sky-400 font-bold">{onlineCountDisplay}</strong></span>
          <span className="opacity-40">•</span>
          <span>Unique: <strong className="text-violet-400 font-bold">{uniqueCountDisplay}</strong></span>
        </div>
        <div className="font-sans font-semibold text-[11px]">
          Evidence blocks: <strong className="text-amber-500 font-mono">{evidenceBlocksCountDisplay}</strong>
        </div>
      </div>
    </div>
  );
};
