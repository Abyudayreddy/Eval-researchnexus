import React, { useState } from 'react';
import { RefreshCw, CheckCircle2 } from 'lucide-react';

interface RefinementManifest {
  refinement_enabled: boolean;
  refinement_mode: string;
  iteration_count: number;
  max_iterations_limit: number;
  total_model_calls: number;
  answer_versions_count: number;
  refinement_history: Array<{
    iteration: number;
    feedback_category: string;
    refinement_queries: string[];
    added_evidence_count: number;
    verification_metrics: any;
  }>;
  quality_delta: {
    supported_claim_delta: number;
    unsupported_claim_delta: number;
    citation_precision_delta: number;
    claim_support_rate_delta: number;
  };
  context_snapshot_id: string;
  context_hash: string;
}

interface RefinementInspectorProps {
  manifest: RefinementManifest | null;
}

export const RefinementInspector: React.FC<RefinementInspectorProps> = ({ manifest }) => {
  const [viewMode, setViewMode] = useState<'clean' | 'advanced'>('clean');

  if (!manifest) {
    return (
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-400 text-xs text-center">
        No refinement manifest recorded for this response.
      </div>
    );
  }

  const hasRefinement = manifest.iteration_count > 0;

  return (
    <div className="space-y-4 text-xs">
      {/* View Mode Toggle */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100">
        <div className="flex items-center gap-1.5 font-bold text-slate-800">
          <RefreshCw className="w-4 h-4 text-emerald-600" />
          <span>Research Refinement Trace</span>
        </div>
        <div className="flex bg-slate-100 p-0.5 rounded-lg border border-slate-200 text-[10px] font-semibold">
          <button
            onClick={() => setViewMode('clean')}
            className={`px-2 py-0.5 rounded ${viewMode === 'clean' ? 'bg-white text-emerald-700 font-bold shadow-xs' : 'text-slate-500'}`}
          >
            Researcher View
          </button>
          <button
            onClick={() => setViewMode('advanced')}
            className={`px-2 py-0.5 rounded ${viewMode === 'advanced' ? 'bg-white text-slate-800 font-bold shadow-xs' : 'text-slate-500'}`}
          >
            Advanced / Experiment
          </button>
        </div>
      </div>

      {viewMode === 'clean' ? (
        /* CLEAN RESEARCHER VIEW */
        <div className="space-y-3 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="font-bold text-slate-700">Refinement Status</span>
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {hasRefinement ? `${manifest.iteration_count} additional evidence pass(es)` : 'Initial pass sufficient'}
            </span>
          </div>

          {hasRefinement ? (
            <div className="space-y-2 pt-2 border-t border-slate-100 text-slate-600 leading-relaxed">
              <div>
                <span className="font-semibold text-slate-800 block mb-0.5">Why refinement occurred:</span>
                <ul className="list-disc list-inside space-y-1 text-slate-600">
                  {manifest.refinement_history.map((h, i) => (
                    <li key={i}>
                      Category: <span className="font-mono text-emerald-700 font-bold">{h.feedback_category}</span> ({h.added_evidence_count} evidence block(s) added)
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-100 font-mono text-[11px]">
                <span>Quality Gain:</span>
                <span className="font-bold text-emerald-600">
                  +{manifest.quality_delta.supported_claim_delta} Supported Claim(s)
                </span>
              </div>
            </div>
          ) : (
            <p className="text-slate-500 italic pt-1">
              The initial generation was adequately grounded in the active research context. No secondary retrieval pass was required.
            </p>
          )}
        </div>
      ) : (
        /* ADVANCED REPRODUCIBILITY VIEW */
        <div className="space-y-4">
          <div className="bg-slate-900 rounded-xl p-4 font-mono text-[10px] text-slate-300 space-y-2 border border-slate-800">
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-emerald-400 font-bold">refinement_mode</span>
              <span>{manifest.refinement_mode}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-emerald-400 font-bold">iterations_executed</span>
              <span>{manifest.iteration_count} / {manifest.max_iterations_limit}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-emerald-400 font-bold">total_model_calls</span>
              <span>{manifest.total_model_calls}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-2">
              <span className="text-emerald-400 font-bold">answer_versions</span>
              <span>{manifest.answer_versions_count}</span>
            </div>
            <div>
              <span className="text-emerald-400 font-bold block">context_hash</span>
              <span className="break-all">{manifest.context_hash}</span>
            </div>
          </div>

          {/* Quality Deltas Box */}
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-800 block">Quality Deltas (Final vs Initial)</span>
            <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
              <div className="bg-white p-2 rounded border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Supported Δ</span>
                <span className="font-bold text-emerald-600">+{manifest.quality_delta.supported_claim_delta}</span>
              </div>
              <div className="bg-white p-2 rounded border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Unsupported Δ</span>
                <span className="font-bold text-rose-600">{manifest.quality_delta.unsupported_claim_delta}</span>
              </div>
              <div className="bg-white p-2 rounded border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Precision Δ</span>
                <span className="font-bold text-slate-700">{(manifest.quality_delta.citation_precision_delta * 100).toFixed(1)}%</span>
              </div>
              <div className="bg-white p-2 rounded border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Support Rate Δ</span>
                <span className="font-bold text-slate-700">{(manifest.quality_delta.claim_support_rate_delta * 100).toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
