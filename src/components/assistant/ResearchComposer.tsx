import React from 'react';
import { Send, Paperclip } from 'lucide-react';

interface ResearchComposerProps {
  value: string;
  onChange: (val: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  scopeLabel: string;
  sourceLabel: string;
  evidenceCount: number;
  isTyping: boolean;
  onAttachClick?: () => void;
}

export const ResearchComposer: React.FC<ResearchComposerProps> = ({
  value,
  onChange,
  onSubmit,
  scopeLabel,
  sourceLabel,
  evidenceCount,
  isTyping,
  onAttachClick
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-3.5 shadow-sm focus-within:border-emerald-400 focus-within:shadow-md transition-all flex flex-col gap-2">
      <div className="flex items-center justify-between text-[9px] font-bold text-slate-400 uppercase tracking-widest border-b border-slate-100 pb-2 mb-1">
        <div className="flex items-center gap-4">
          <span>Scope: <strong className="text-slate-600">{scopeLabel}</strong></span>
          <span>Sources: <strong className="text-slate-600">{sourceLabel}</strong></span>
          <span>Evidence: <strong className="text-slate-600">{evidenceCount} blocks</strong></span>
        </div>
      </div>
      
      <form onSubmit={onSubmit} className="flex flex-col gap-2">
        <textarea 
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Ask a research question..."
          className="w-full bg-transparent text-sm font-medium text-slate-800 placeholder:text-slate-400 resize-none outline-none min-h-[50px] p-1.5"
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              onSubmit(e);
            }
          }}
        />
        
        <div className="flex items-center justify-between pt-2 border-t border-slate-100">
          <button 
            type="button" 
            onClick={onAttachClick}
            className="p-1.5 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
            title="Attach Context File"
          >
            <Paperclip className="w-4 h-4" />
          </button>
          
          <button 
            type="submit" 
            disabled={isTyping || !value.trim()}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-40 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all hover:scale-[1.02] active:scale-95"
          >
            Send <Send className="w-3.5 h-3.5" />
          </button>
        </div>
      </form>
    </div>
  );
};
