import React, { useState, useEffect } from 'react';
import { Play } from 'lucide-react';

interface ExperimentRunnerProps {
  datasets: any[];
}

export const ExperimentRunner: React.FC<ExperimentRunnerProps> = ({ datasets }) => {
  const [experiments, setExperiments] = useState<any[]>([]);
  const [selectedBaseline, setSelectedBaseline] = useState<string>('B5_ENHANCED_RAG');
  const [isRunning, setIsRunning] = useState<boolean>(false);

  const fetchExperiments = async () => {
    try {
      const res = await fetch('/api/evaluation/experiments');
      if (res.ok) setExperiments(await res.json());
    } catch (e) {
      console.error('Failed to fetch experiments', e);
    }
  };

  useEffect(() => {
    fetchExperiments();
  }, []);

  const handleLaunchExperiment = async () => {
    if (!datasets || datasets.length === 0) return;
    setIsRunning(true);
    try {
      const createRes = await fetch('/api/evaluation/experiments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: `Controlled Run (${selectedBaseline})`,
          dataset_id: datasets[0].dataset_id,
          baseline_id: selectedBaseline
        })
      });

      if (createRes.ok) {
        const expData = await createRes.json();
        await fetch(`/api/evaluation/experiments/${expData.experiment_id}/run`, { method: 'POST' });
        await fetchExperiments();
      }
    } catch (e) {
      console.error('Failed to launch experiment', e);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-black text-slate-900">Baseline Experiment Runner</h2>
          <p className="text-xs text-slate-500 font-medium mt-0.5">
            Select an operationally real baseline (B0–B7) and launch controlled evaluation on benchmark dataset splits
          </p>
        </div>

        <button
          onClick={handleLaunchExperiment}
          disabled={isRunning}
          className="flex items-center gap-1.5 px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-slate-300 text-white font-bold text-xs rounded-xl transition shadow-sm"
        >
          <Play className="w-3.5 h-3.5 fill-white" /> {isRunning ? 'Running Experiment...' : 'Launch Baseline Run'}
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { id: 'B0_LLM_ONLY', label: 'B0 LLM-Only' },
          { id: 'B1_DENSE_RAG', label: 'B1 Dense RAG' },
          { id: 'B2_BM25_RAG', label: 'B2 BM25 RAG' },
          { id: 'B3_HYBRID_RAG', label: 'B3 Hybrid RAG' },
          { id: 'B4_HYBRID_BGE', label: 'B4 Hybrid + BGE' },
          { id: 'B5_ENHANCED_RAG', label: 'B5 Enhanced RAG' },
          { id: 'B6_ENHANCED_VERIFICATION', label: 'B6 Enhanced + Verification' },
          { id: 'B7_ITERATIVE_RAG', label: 'B7 Iterative RAG' }
        ].map((b) => (
          <button
            key={b.id}
            onClick={() => setSelectedBaseline(b.id)}
            className={`p-3 rounded-xl border text-left text-xs font-bold transition ${
              selectedBaseline === b.id ? 'bg-purple-50 border-purple-500 ring-2 ring-purple-500/20 text-purple-900' : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
            }`}
          >
            {b.label}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        <h3 className="text-xs font-black text-slate-800 uppercase tracking-wider">Executed Experiments ({experiments.length})</h3>
        <div className="space-y-2">
          {experiments.map((e) => (
            <div key={e.experiment_id} className="bg-slate-50 border border-slate-200 p-3.5 rounded-xl flex items-center justify-between text-xs">
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-extrabold text-slate-900">{e.name}</h4>
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.2 bg-purple-100 text-purple-800 rounded-full">{e.baseline_id}</span>
                </div>
                <span className="text-[10px] text-slate-400 font-medium">Executed: {e.created_at ? new Date(e.created_at).toLocaleTimeString() : ''}</span>
              </div>
              <span className="text-xs font-extrabold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">{e.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
