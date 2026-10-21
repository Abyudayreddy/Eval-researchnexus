import React from 'react';
import { RefreshCw, Zap } from 'lucide-react';

interface RefinementModeSelectorProps {
  mode: 'automatic' | 'single_pass';
  onChange: (mode: 'automatic' | 'single_pass') => void;
}

export const RefinementModeSelector: React.FC<RefinementModeSelectorProps> = ({ mode, onChange }) => {
  return (
    <div className="inline-flex items-center p-0.5 bg-slate-100 rounded-lg border border-slate-200/80 text-[11px] font-semibold">
      <button
        type="button"
        onClick={() => onChange('automatic')}
        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md transition ${
          mode === 'automatic'
            ? 'bg-white text-emerald-700 shadow-xs border border-slate-200/60 font-bold'
            : 'text-slate-500 hover:text-slate-800'
        }`}
        title="Automatic iterative refinement (at most 2 cycles)"
      >
        <RefreshCw className="w-3 h-3 text-emerald-600" />
        Automatic (Iterative)
      </button>

      <button
        type="button"
        onClick={() => onChange('single_pass')}
        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md transition ${
          mode === 'single_pass'
            ? 'bg-white text-slate-800 shadow-xs border border-slate-200/60 font-bold'
            : 'text-slate-500 hover:text-slate-800'
        }`}
        title="Single pass generation (no refinement cycles)"
      >
        <Zap className="w-3 h-3 text-amber-500" />
        Single Pass
      </button>
    </div>
  );
};
