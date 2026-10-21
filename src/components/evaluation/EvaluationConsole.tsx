import React, { useState, useEffect } from 'react';
import { ShieldCheck } from 'lucide-react';
import { ExperimentRunner } from './ExperimentRunner';
import { AblationView } from './AblationView';
import { HumanEvalPanel } from './HumanEvalPanel';
import { ErrorAnalysisWorkspace } from './ErrorAnalysisWorkspace';
import { PublicationTables } from './PublicationTables';

export const EvaluationConsole: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'experiments' | 'ablation' | 'humaneval' | 'errors' | 'publication'>('experiments');
  const [datasets, setDatasets] = useState<any[]>([]);
  const [claims, setClaims] = useState<any[]>([]);

  const fetchConsoleData = async () => {
    try {
      const [dsRes, clmRes] = await Promise.all([
        fetch('/api/evaluation/datasets'),
        fetch('/api/evaluation/claims/audit')
      ]);
      if (dsRes.ok) setDatasets(await dsRes.json());
      if (clmRes.ok) setClaims(await clmRes.json());
    } catch (e) {
      console.error('Failed to fetch evaluation console data', e);
    }
  };

  useEffect(() => {
    fetchConsoleData();
  }, []);

  return (
    <div className="w-full flex flex-col gap-6 p-6 bg-slate-50 min-h-screen">
      {/* Console Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-100 text-purple-800 uppercase tracking-wide">
              Evaluation & Publication Console
            </span>
            <span className="text-xs font-semibold text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-full flex items-center gap-1">
              <ShieldCheck className="w-3 h-3 text-purple-600" /> Measurement, Not Marketing
            </span>
          </div>
          <h1 className="text-xl font-black text-slate-900">Experimental Validation Platform</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Controlled baseline comparisons, component ablations, blinded human evaluation, & reproducible publication tables
          </p>
        </div>

        <div className="flex items-center gap-2">
          {['experiments', 'ablation', 'humaneval', 'errors', 'publication'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-3 py-1.5 text-xs font-bold rounded-xl transition uppercase ${
                activeTab === tab ? 'bg-purple-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Main Workspace View */}
      {activeTab === 'experiments' && <ExperimentRunner datasets={datasets} />}
      {activeTab === 'ablation' && <AblationView datasetId={datasets[0]?.dataset_id || 'ds_default'} />}
      {activeTab === 'humaneval' && <HumanEvalPanel experimentId="exp_default" itemId="item_default" />}
      {activeTab === 'errors' && <ErrorAnalysisWorkspace />}
      {activeTab === 'publication' && <PublicationTables claims={claims} />}
    </div>
  );
};
