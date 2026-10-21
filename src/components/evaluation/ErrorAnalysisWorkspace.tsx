import React, { useState } from 'react';

interface ErrorItem {
  id: string;
  category: string;
  count: number;
  description: string;
  exampleQuestion: string;
  retrievedEvidence: string;
}

export const ErrorAnalysisWorkspace: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const errors: ErrorItem[] = [
    { id: 'err_1', category: 'RETRIEVAL_MISS', count: 17, description: 'Expected paper not present in top-10 hybrid candidates', exampleQuestion: 'What are the limits of transformer-based climate forecasting?', retrievedEvidence: 'Retrieved 8 climate papers, missing Paper B.' },
    { id: 'err_2', category: 'RERANKING_ERROR', count: 8, description: 'Relevant candidate demoted below cut-off rank by BGE reranker', exampleQuestion: 'How does RRF constant k affect dense fusion?', retrievedEvidence: 'Relevant paper demoted to rank 14.' },
    { id: 'err_3', category: 'EVIDENCE_MISS', count: 12, description: 'Paper retrieved but relevant sentence chunk missed', exampleQuestion: 'What accuracy was reported on CIFAR-100?', retrievedEvidence: 'Chunk 2 extracted instead of Chunk 5.' },
    { id: 'err_4', category: 'CITATION_ERROR', count: 5, description: 'Citation tag attached to wrong sentence block', exampleQuestion: 'Compare accuracy across models.', retrievedEvidence: 'Citation [2] attached to Method A sentence.' },
    { id: 'err_5', category: 'UNSUPPORTED_CLAIM', count: 6, description: 'Generated numerical claim unsupported by retrieved text', exampleQuestion: 'What performance delta was measured?', retrievedEvidence: 'Generated 92% instead of 82%.' },
    { id: 'err_6', category: 'CONTEXT_LEAKAGE', count: 1, description: 'Out-of-scope paper entered context snapshot', exampleQuestion: 'Analyze Paper A.', retrievedEvidence: 'Paper B referenced.' }
  ];

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-6">
      <div>
        <h2 className="text-base font-black text-slate-900">Error Analysis Workspace</h2>
        <p className="text-xs text-slate-500 font-medium mt-0.5">
          First-class failure categorization and inspection workspace for paper error analysis
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {errors.map((err) => (
          <div
            key={err.id}
            onClick={() => setSelectedCategory(err.category)}
            className={`p-4 rounded-xl border transition cursor-pointer space-y-2 ${
              selectedCategory === err.category ? 'bg-rose-50 border-rose-500 ring-2 ring-rose-500/20' : 'bg-slate-50 border-slate-200 hover:border-slate-300'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 bg-rose-100 text-rose-800 rounded-full">
                {err.category}
              </span>
              <strong className="text-sm font-black text-rose-900">{err.count} cases</strong>
            </div>
            <p className="text-xs font-bold text-slate-800">{err.description}</p>
          </div>
        ))}
      </div>

      {selectedCategory && (
        <div className="bg-slate-50 border border-slate-200 p-5 rounded-2xl space-y-3">
          <h3 className="text-xs font-black text-slate-900 uppercase">Inspecting Category: {selectedCategory}</h3>
          <div className="bg-white p-4 rounded-xl border border-slate-200 text-xs space-y-2">
            <p><strong>Example Question:</strong> {errors.find(e => e.category === selectedCategory)?.exampleQuestion}</p>
            <p><strong>Retrieved Evidence / Trace:</strong> {errors.find(e => e.category === selectedCategory)?.retrievedEvidence}</p>
          </div>
        </div>
      )}
    </div>
  );
};
