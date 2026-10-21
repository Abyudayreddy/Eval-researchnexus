import { Lightbulb, X } from 'lucide-react';
import { useTipStore } from '../store/tipStore';

interface ContextualTipProps {
  id: string;
  text: string;
}

export default function ContextualTip({ id, text }: ContextualTipProps) {
  const { hasSeenTip, dismissTip } = useTipStore();

  if (hasSeenTip(id)) {
    return null;
  }

  return (
    <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start gap-3 shadow-sm relative animate-in fade-in slide-in-from-bottom-2 mb-6">
      <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center shrink-0">
        <Lightbulb className="w-4 h-4 text-amber-600" />
      </div>
      <div className="flex-1 pr-6">
        <h4 className="text-[11px] font-bold text-amber-800 uppercase tracking-widest mb-1 flex items-center gap-1.5">
          <Lightbulb className="w-3.5 h-3.5" /> Tip
        </h4>
        <p className="text-sm text-amber-900 font-medium leading-relaxed">{text}</p>
        <button 
          onClick={() => dismissTip(id)}
          className="mt-3 text-xs font-bold text-amber-800 bg-white hover:bg-amber-100 border border-amber-200 px-3 py-1.5 rounded-lg transition-colors shadow-sm"
        >
          Got it
        </button>
      </div>
      <button 
        onClick={() => dismissTip(id)}
        className="absolute top-3 right-3 text-amber-400 hover:text-amber-600 p-1"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
