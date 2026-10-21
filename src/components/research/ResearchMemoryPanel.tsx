import React, { useState, useEffect } from 'react';
import { BrainCircuit, Check, X, Edit2, Trash2 } from 'lucide-react';

interface ResearchMemoryItem {
  memory_id: string;
  memory_type: string;
  content: string;
  status: string;  // SUGGESTED | ACCEPTED | REJECTED | EDITED
  memory_origin: string;  // USER_RECORDED | EVIDENCE_DERIVED | AI_SUGGESTED
  paper_ids?: string[];
  evidence_ids?: string[];
  created_at?: string;
}

interface ResearchMemoryPanelProps {
  sessionId?: string;
  onOpenProof?: (text: string) => void;
}

export const ResearchMemoryPanel: React.FC<ResearchMemoryPanelProps> = ({
  sessionId,
  onOpenProof
}) => {
  const [memories, setMemories] = useState<ResearchMemoryItem[]>([]);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState<string>('');

  const fetchMemories = async () => {
    if (!sessionId) return;
    try {
      const res = await fetch(`/api/research/sessions/${sessionId}/memories`);
      if (res.ok) {
        const data = await res.json();
        setMemories(data);
      }
    } catch (e) {
      console.error('Failed to fetch memories', e);
    }
  };

  useEffect(() => {
    fetchMemories();
  }, [sessionId]);

  const handleAccept = async (memoryId: string) => {
    try {
      await fetch(`/api/research/memories/${memoryId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'ACCEPTED' })
      });
      await fetchMemories();
    } catch (e) {
      console.error('Failed to accept memory', e);
    }
  };

  const handleReject = async (memoryId: string) => {
    try {
      await fetch(`/api/research/memories/${memoryId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'REJECTED' })
      });
      await fetchMemories();
    } catch (e) {
      console.error('Failed to reject memory', e);
    }
  };

  const handleDelete = async (memoryId: string) => {
    try {
      await fetch(`/api/research/memories/${memoryId}`, { method: 'DELETE' });
      await fetchMemories();
    } catch (e) {
      console.error('Failed to delete memory', e);
    }
  };

  const handleSaveEdit = async (memoryId: string) => {
    try {
      await fetch(`/api/research/memories/${memoryId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: editContent })
      });
      setEditingId(null);
      await fetchMemories();
    } catch (e) {
      console.error('Failed to edit memory', e);
    }
  };

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BrainCircuit className="w-4 h-4 text-purple-600" />
          <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Research Memory ({memories.length})</h3>
        </div>
        <span className="text-[11px] font-bold text-slate-500 bg-purple-50 px-2.5 py-0.5 rounded-full border border-purple-200">
          Provenanced Facts & Decisions
        </span>
      </div>

      <div className="space-y-3">
        {memories.map((m) => {
          const isSuggested = m.status === 'SUGGESTED';
          const isEditing = editingId === m.memory_id;

          return (
            <div key={m.memory_id} className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 bg-purple-100 text-purple-800 rounded-full">
                    {m.memory_type.replace('_', ' ')}
                  </span>
                  <span className="text-[10px] font-semibold text-slate-400">
                    Origin: {m.memory_origin}
                  </span>
                </div>

                {isSuggested && (
                  <span className="text-[10px] font-bold px-2 py-0.5 bg-amber-100 text-amber-800 rounded-full">
                    SUGGESTED (Requires Approval)
                  </span>
                )}
              </div>

              {isEditing ? (
                <div className="space-y-2">
                  <textarea
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded-lg text-xs"
                  />
                  <div className="flex gap-2">
                    <button onClick={() => handleSaveEdit(m.memory_id)} className="px-2.5 py-1 bg-emerald-600 text-white rounded text-xs font-bold">Save</button>
                    <button onClick={() => setEditingId(null)} className="px-2.5 py-1 bg-slate-200 text-slate-700 rounded text-xs">Cancel</button>
                  </div>
                </div>
              ) : (
                <p className="text-slate-800 font-medium leading-relaxed">{m.content}</p>
              )}

              <div className="flex items-center justify-between pt-1">
                <div className="flex items-center gap-2">
                  {onOpenProof && m.memory_type === 'KEY_FINDING' && (
                    <button
                      onClick={() => onOpenProof(m.content)}
                      className="text-[10px] font-bold text-purple-700 bg-white border border-purple-200 px-2 py-0.5 rounded hover:bg-purple-50"
                    >
                      Show Proof
                    </button>
                  )}
                </div>

                <div className="flex items-center gap-1">
                  {isSuggested && (
                    <>
                      <button onClick={() => handleAccept(m.memory_id)} className="p-1 text-emerald-600 hover:bg-emerald-50 rounded" title="Accept Memory">
                        <Check className="w-3.5 h-3.5" />
                      </button>
                      <button onClick={() => handleReject(m.memory_id)} className="p-1 text-rose-600 hover:bg-rose-50 rounded" title="Reject Memory">
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </>
                  )}

                  <button
                    onClick={() => { setEditingId(m.memory_id); setEditContent(m.content); }}
                    className="p-1 text-slate-400 hover:text-slate-700 rounded"
                    title="Edit Memory"
                  >
                    <Edit2 className="w-3.5 h-3.5" />
                  </button>

                  <button onClick={() => handleDelete(m.memory_id)} className="p-1 text-slate-400 hover:text-rose-600 rounded" title="Delete Memory">
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
