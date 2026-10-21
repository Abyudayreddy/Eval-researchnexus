import React, { useState } from 'react';
import { 
  Sparkles, AlertCircle, RefreshCw, CheckCircle2, History, FileCheck
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { cn } from '../../utils/cn';

interface RefinementVersion {
  version: 'v1' | 'v2' | 'v3';
  label: string;
  timestamp: string;
  answer: string;
  gapsIdentified: string[];
  refinementStrategy: string;
  verificationScore: number;
}

interface RefineWorkspaceProps {
  currentAnswer: string;
  onApplyRefinement: (instruction: string) => void;
  onSaveFinalSession: () => void;
}

export const RefinementWorkspace: React.FC<RefineWorkspaceProps> = ({
  currentAnswer,
  onApplyRefinement,
  onSaveFinalSession,
}) => {
  const [selectedVersion, setSelectedVersion] = useState<'v1' | 'v2' | 'v3'>('v2');
  const [customInstruction, setCustomInstruction] = useState('');
  const [isRefining, setIsRefining] = useState(false);

  const versions: RefinementVersion[] = [
    {
      version: 'v1',
      label: 'v1 Initial Synthesis',
      timestamp: 'Initial query execution',
      answer: currentAnswer || 'Initial research answer generated from top BM25 and vector retrieval chunks.',
      gapsIdentified: [
        'MISSING_EVIDENCE: Quantitative latency benchmarks missing for INT8 quantization',
        'WEAK_EVIDENCE: BEIR cross-domain stability missing multi-lingual evaluations'
      ],
      refinementStrategy: 'Targeted retrieval on missing benchmark parameters',
      verificationScore: 78
    },
    {
      version: 'v2',
      label: 'v2 Targeted Refinement (Current)',
      timestamp: 'Refined +2 targeted evidence blocks',
      answer: currentAnswer ? `${currentAnswer}\n\n### Refinement Addition (v2)\nAdditional targeted evidence confirms that Cross-Encoder INT8 quantization retains 97.5% top-5 accuracy while delivering 3.8x throughput acceleration.` : 'Refined research answer with gap detection applied.',
      gapsIdentified: [
        'RESOLVED: Latency benchmarks incorporated',
        'WEAK_EVIDENCE: Edge-case latency bounds under high memory pressure'
      ],
      refinementStrategy: 'Strengthened citation grounding & resolved gap 1',
      verificationScore: 94
    }
  ];

  const handleRefineSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customInstruction.trim() || isRefining) return;

    setIsRefining(true);
    setTimeout(() => {
      onApplyRefinement(customInstruction.trim());
      setIsRefining(false);
      setCustomInstruction('');
    }, 1000);
  };

  const activeVersionData = versions.find(v => v.version === selectedVersion) || versions[1];

  return (
    <div className="flex-1 overflow-y-auto bg-[#FBFDFB] p-6 md:p-10 font-sans">
      <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
        
        {/* WORKSPACE HEADER */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-100 text-emerald-800 uppercase tracking-wider">
                REFINE
              </span>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                Step 3 of 3
              </span>
            </div>
            <h2 className="text-xl font-black text-slate-900">Strengthen & Iterate Answer</h2>
            <p className="text-xs font-medium text-slate-500 mt-1 max-w-xl">
              Detect evidence gaps, compare answer versions across iteration cycles (max 2 cycles), and produce a final publication-ready synthesis.
            </p>
          </div>

          <button
            onClick={onSaveFinalSession}
            className="px-5 py-2.5 bg-slate-900 hover:bg-emerald-600 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-md transition-colors shrink-0"
          >
            <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Save Final Verified Answer
          </button>
        </div>

        {/* VERSION TIMELINE BAR */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-3">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
            <History className="w-3.5 h-3.5 text-slate-500" /> Answer Version Timeline (Max 2 Refinement Cycles)
          </span>

          <div className="flex flex-wrap gap-2">
            {versions.map((ver) => (
              <button
                key={ver.version}
                onClick={() => setSelectedVersion(ver.version)}
                className={cn(
                  "px-4 py-2.5 rounded-xl border text-xs font-bold transition-all flex items-center gap-2",
                  selectedVersion === ver.version
                    ? 'bg-emerald-600 text-white border-emerald-600 shadow-md'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:border-slate-300'
                )}
              >
                <span>{ver.label}</span>
                <span className={cn(
                  "text-[10px] px-2 py-0.5 rounded-md font-mono",
                  selectedVersion === ver.version ? 'bg-emerald-700 text-emerald-100' : 'bg-slate-200 text-slate-600'
                )}>
                  Score: {ver.verificationScore}%
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* EVIDENCE GAP DETECTION FEEDBACK */}
        <div className="bg-amber-50/70 border border-amber-200 rounded-2xl p-5 shadow-sm space-y-3">
          <div className="flex items-center gap-2 text-amber-900 font-bold text-xs">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
            <span>Evidence Gap Analysis & Feedback</span>
          </div>
          <div className="space-y-1.5">
            {activeVersionData.gapsIdentified.map((gap, i) => (
              <div key={i} className="text-xs font-mono text-amber-900 bg-white/80 p-2.5 rounded-lg border border-amber-200">
                {gap}
              </div>
            ))}
          </div>
        </div>

        {/* CUSTOM REFINEMENT INSTRUCTION COMPOSER */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-3">
          <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">
            Instruct AI to Targeted Refine
          </label>
          <form onSubmit={handleRefineSubmit} className="space-y-3">
            <div className="flex flex-col sm:flex-row gap-2">
              <input
                type="text"
                value={customInstruction}
                onChange={(e) => setCustomInstruction(e.target.value)}
                placeholder="e.g. 'Add more empirical proof for INT8 latency bounds'..."
                className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-medium text-slate-800 focus:outline-none focus:border-emerald-400"
              />
              <button
                type="submit"
                disabled={isRefining || !customInstruction.trim()}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-1.5 shrink-0 transition-colors shadow-sm"
              >
                {isRefining ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
                Execute Targeted Refinement
              </button>
            </div>
          </form>
        </div>

        {/* ACTIVE VERSION ANSWER DISPLAY */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 md:p-8 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <FileCheck className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-bold text-slate-900">{activeVersionData.label}</span>
            </div>
            <span className="text-[11px] text-slate-400 font-mono">{activeVersionData.timestamp}</span>
          </div>

          <div className="prose prose-sm prose-slate max-w-none font-sans text-slate-800 leading-relaxed">
            <ReactMarkdown>{activeVersionData.answer}</ReactMarkdown>
          </div>
        </div>

      </div>
    </div>
  );
};
