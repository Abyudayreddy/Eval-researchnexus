import { ExternalLink, RefreshCw, Bot, Bookmark } from 'lucide-react';

interface PaperInspectorProps {
  title: string;
  source: string;
  rank?: number;
  evidenceCount?: number;
  onOpen?: () => void;
  onExplain?: () => void;
  onAskAi?: () => void;
  onSave?: () => void;
}

export const PaperInspector: React.FC<PaperInspectorProps> = ({
  title,
  source,
  rank,
  evidenceCount = 0,
  onOpen,
  onExplain,
  onAskAi,
  onSave
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-3">
      <div>
        <h4 className="text-xs font-black text-slate-800 line-clamp-2">{title}</h4>
        <div className="flex flex-wrap items-center gap-2 mt-1.5 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
          <span>Source: {source}</span>
          {rank !== undefined && (
            <>
              <span>•</span>
              <span>RRF Rank: #{rank}</span>
            </>
          )}
          <span>•</span>
          <span>Evidence: {evidenceCount} blocks</span>
        </div>
      </div>

      <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
        {onOpen && (
          <button 
            onClick={onOpen}
            className="flex-1 px-2.5 py-1.5 text-[10px] font-bold bg-slate-900 text-white hover:bg-slate-800 rounded-lg flex items-center justify-center gap-1 transition-all"
          >
            <ExternalLink className="w-3 h-3" /> Open
          </button>
        )}
        {onExplain && (
          <button 
            onClick={onExplain}
            className="flex-1 px-2.5 py-1.5 text-[10px] font-bold bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 rounded-lg flex items-center justify-center gap-1 transition-all"
          >
            <RefreshCw className="w-3 h-3" /> Explain
          </button>
        )}
        {onAskAi && (
          <button 
            onClick={onAskAi}
            className="flex-1 px-2.5 py-1.5 text-[10px] font-bold bg-emerald-600 text-white hover:bg-emerald-700 rounded-lg flex items-center justify-center gap-1 transition-all"
          >
            <Bot className="w-3 h-3" /> Ask AI
          </button>
        )}
        {onSave && (
          <button 
            onClick={onSave}
            className="p-1.5 bg-white border border-slate-200 text-slate-500 hover:text-emerald-600 rounded-lg transition-colors"
            title="Save Paper"
          >
            <Bookmark className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
    </div>
  );
};
