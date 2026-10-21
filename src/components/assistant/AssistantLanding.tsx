import React from 'react';
import { 
  Sparkles, CheckCircle2, RefreshCw, ArrowRight, Upload, BrainCircuit
} from 'lucide-react';

interface AssistantLandingProps {
  onSelectWorkspace: (workspace: 'ask' | 'explore' | 'prove' | 'refine') => void;
  paperCount: number;
  sourcesCount: number;
}

export const AssistantLanding: React.FC<AssistantLandingProps> = ({
  onSelectWorkspace,
  paperCount,
  sourcesCount,
}) => {
  return (
    <div className="flex-1 overflow-y-auto bg-[#FBFDFB] p-6 md:p-12 font-sans">
      <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-300">
        
        {/* HERO TITLE SECTION */}
        <div className="text-center space-y-3 max-w-2xl mx-auto pt-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" /> Grounded Research Reasoning Workspace
          </div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">
            Deep Literature & Evidence Analysis
          </h1>
          <p className="text-sm font-medium text-slate-500 leading-relaxed">
            ResearchNexus provides a calm, transparent research environment. Select a primary objective below to begin your analysis.
          </p>

          {/* ACTIVE CONTEXT STATUS BADGE */}
          <div className="pt-2">
            <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 border border-slate-200 text-xs font-mono font-bold text-slate-700">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              Synchronized Research Context: {paperCount} Papers • {sourcesCount} Sources
            </span>
          </div>
        </div>

        {/* 4 CALM FEATURE CARDS GRID */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          
          {/* CARD 1: ASK */}
          <div 
            onClick={() => onSelectWorkspace('ask')}
            className="bg-white border border-slate-200 hover:border-emerald-500 hover:shadow-md rounded-2xl p-6 transition-all cursor-pointer group flex flex-col justify-between space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center font-black">
                  01
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-100">
                  Step 1
                </span>
              </div>
              <div>
                <h3 className="text-base font-black text-slate-900 group-hover:text-emerald-700 transition-colors flex items-center gap-2">
                  ASK <BrainCircuit className="w-4 h-4 text-emerald-600" />
                </h3>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  Generate a grounded research answer from retrieved literature. Includes 6-stage beginner loading progress and full RAG technical disclosure.
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs font-bold text-slate-700 group-hover:text-emerald-700">
              <span>Open Research Answer</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* CARD 2: EXPLORE PAPERS */}
          <div 
            onClick={() => onSelectWorkspace('explore')}
            className="bg-white border border-slate-200 hover:border-blue-500 hover:shadow-md rounded-2xl p-6 transition-all cursor-pointer group flex flex-col justify-between space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center font-black">
                  02
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest text-blue-700 bg-blue-50 px-2.5 py-1 rounded-md border border-blue-100">
                  Step 2
                </span>
              </div>
              <div>
                <h3 className="text-base font-black text-slate-900 group-hover:text-blue-700 transition-colors flex items-center gap-2">
                  EXPLORE PAPERS <Upload className="w-4 h-4 text-blue-600" />
                </h3>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  Upload PDF research papers with a 10-stage transparent pipeline, or synthesize a multi-paper comparison matrix across 10 key dimensions.
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs font-bold text-slate-700 group-hover:text-blue-700">
              <span>Upload & Compare</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* CARD 3: PROVE */}
          <div 
            onClick={() => onSelectWorkspace('prove')}
            className="bg-white border border-slate-200 hover:border-violet-500 hover:shadow-md rounded-2xl p-6 transition-all cursor-pointer group flex flex-col justify-between space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-violet-50 text-violet-700 flex items-center justify-center font-black">
                  03
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest text-violet-700 bg-violet-50 px-2.5 py-1 rounded-md border border-violet-100">
                  Step 3
                </span>
              </div>
              <div>
                <h3 className="text-base font-black text-slate-900 group-hover:text-violet-700 transition-colors flex items-center gap-2">
                  PROVE <CheckCircle2 className="w-4 h-4 text-violet-600" />
                </h3>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  Inspect claim-level attribution proof cards with status badges (Supported, Partial, Insufficient Evidence), exact passages, and source links.
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs font-bold text-slate-700 group-hover:text-violet-700">
              <span>Verify Evidence</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          {/* CARD 4: REFINE */}
          <div 
            onClick={() => onSelectWorkspace('refine')}
            className="bg-white border border-slate-200 hover:border-amber-500 hover:shadow-md rounded-2xl p-6 transition-all cursor-pointer group flex flex-col justify-between space-y-4"
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center font-black">
                  04
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest text-amber-700 bg-amber-50 px-2.5 py-1 rounded-md border border-amber-100">
                  Step 4
                </span>
              </div>
              <div>
                <h3 className="text-base font-black text-slate-900 group-hover:text-amber-700 transition-colors flex items-center gap-2">
                  REFINE <RefreshCw className="w-4 h-4 text-amber-600" />
                </h3>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  Detect evidence gaps, compare answer versions across iteration cycles (max 2 cycles), and produce a final publication-ready synthesis.
                </p>
              </div>
            </div>
            <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs font-bold text-slate-700 group-hover:text-amber-700">
              <span>Iterate & Gap Fill</span>
              <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
