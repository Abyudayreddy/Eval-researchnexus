import React, { useState, useEffect } from 'react';
import { Plus, Archive, RotateCcw, Trash2, Folder } from 'lucide-react';

interface SessionItem {
  session_id: string;
  title: string;
  description?: string;
  status: string;
  paper_count: number;
  finding_count: number;
  last_activity_at?: string;
}

interface ResearchSessionsPanelProps {
  activeSessionId?: string;
  onSelectSession?: (sessionId: string) => void;
  onCreateNewSession?: () => void;
}

export const ResearchSessionsPanel: React.FC<ResearchSessionsPanelProps> = ({
  activeSessionId,
  onSelectSession,
  onCreateNewSession
}) => {
  const [sessions, setSessions] = useState<SessionItem[]>([]);
  const [showArchived] = useState<boolean>(true);

  const fetchSessions = async () => {
    try {
      const res = await fetch(`/api/research/sessions?include_archived=${showArchived}`);
      if (res.ok) {
        const data = await res.json();
        setSessions(data);
      }
    } catch (e) {
      console.error('Failed to fetch sessions', e);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, [showArchived]);

  const handleArchive = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await fetch(`/api/research/sessions/${sessionId}/archive`, { method: 'POST' });
      await fetchSessions();
    } catch (err) {
      console.error('Failed to archive session', err);
    }
  };

  const handleRestore = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await fetch(`/api/research/sessions/${sessionId}/restore`, { method: 'POST' });
      await fetchSessions();
    } catch (err) {
      console.error('Failed to restore session', err);
    }
  };

  const handleDelete = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await fetch(`/api/research/sessions/${sessionId}`, { method: 'DELETE' });
      await fetchSessions();
    } catch (err) {
      console.error('Failed to delete session', err);
    }
  };

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Folder className="w-4 h-4 text-emerald-600" />
          <h2 className="text-sm font-black text-slate-900 uppercase tracking-wider">Research Sessions</h2>
        </div>

        <button
          onClick={onCreateNewSession}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
        >
          <Plus className="w-3.5 h-3.5" /> New Research
        </button>
      </div>

      <div className="space-y-2">
        {sessions.map((s) => {
          const isActive = s.session_id === activeSessionId;
          const isArchived = s.status === 'ARCHIVED';

          return (
            <div
              key={s.session_id}
              onClick={() => onSelectSession && onSelectSession(s.session_id)}
              className={`p-3.5 rounded-xl border transition cursor-pointer flex items-center justify-between ${
                isActive ? 'bg-emerald-50/60 border-emerald-400 ring-2 ring-emerald-500/20' :
                isArchived ? 'bg-slate-50 border-slate-200 opacity-75' : 'bg-slate-50/40 border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h4 className="text-xs font-black text-slate-800">{s.title}</h4>
                  <span className={`text-[9px] font-extrabold uppercase px-2 py-0.2 rounded-full ${
                    isArchived ? 'bg-slate-200 text-slate-700' : 'bg-emerald-100 text-emerald-800'
                  }`}>
                    {s.status}
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 font-medium">
                  {s.paper_count} Papers · {s.finding_count} Findings
                </p>
              </div>

              <div className="flex items-center gap-1">
                {!isArchived ? (
                  <button
                    onClick={(e) => handleArchive(s.session_id, e)}
                    className="p-1 text-slate-400 hover:text-slate-700 rounded transition"
                    title="Archive Session"
                  >
                    <Archive className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    onClick={(e) => handleRestore(s.session_id, e)}
                    className="p-1 text-slate-400 hover:text-emerald-700 rounded transition"
                    title="Restore Session"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                  </button>
                )}

                <button
                  onClick={(e) => handleDelete(s.session_id, e)}
                  className="p-1 text-slate-400 hover:text-rose-600 rounded transition"
                  title="Soft Delete Session"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
