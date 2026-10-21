import React, { useState, useEffect } from 'react';

interface AblationViewProps {
  datasetId: string;
}

export const AblationView: React.FC<AblationViewProps> = ({ datasetId }) => {
  const [matrix, setMatrix] = useState<any[]>([]);

  useEffect(() => {
    fetch(`/api/evaluation/experiments/${datasetId}/ablation`)
      .then(res => res.json())
      .then(data => setMatrix(data.matrix || []))
      .catch(err => console.error('Failed to fetch ablation study matrix', err));
  }, [datasetId]);

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
      <div>
        <h2 className="text-base font-black text-slate-900">Component Ablation Study Matrix</h2>
        <p className="text-xs text-slate-500 font-medium mt-0.5">
          Controlled component removal study evaluating impact of BGE Reranker, Claim Verification, and Iterative Refinement
        </p>
      </div>

      <div className="overflow-x-auto border border-slate-200 rounded-xl">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-100 font-extrabold text-slate-700 uppercase border-b border-slate-200">
            <tr>
              <th className="p-3">Configuration</th>
              <th className="p-3">Baseline ID</th>
              <th className="p-3">Citation Precision</th>
              <th className="p-3">Claim Support Rate</th>
              <th className="p-3">P95 Latency</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 font-medium text-slate-800">
            {matrix.map((row, idx) => (
              <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}>
                <td className="p-3 font-bold text-slate-900">{row.configuration}</td>
                <td className="p-3 font-mono text-[10px] text-purple-700">{row.baseline_id}</td>
                <td className="p-3 font-bold text-emerald-700">{row.citation_precision}</td>
                <td className="p-3 font-bold text-blue-700">{row.claim_support_rate}</td>
                <td className="p-3">{row.p95_latency_ms}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
