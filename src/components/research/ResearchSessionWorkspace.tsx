import React, { useState, useEffect } from 'react';
import { ResearchSessionsPanel } from './ResearchSessionsPanel';
import { ResearchMemoryPanel } from './ResearchMemoryPanel';
import { ResearchTimeline } from './ResearchTimeline';
import { ResearchSessionSummary } from './ResearchSessionSummary';

interface ResearchSessionWorkspaceProps {
  currentSessionId?: string;
  onSelectSession?: (sessionId: string) => void;
  onOpenProof?: (text: string) => void;
}

export const ResearchSessionWorkspace: React.FC<ResearchSessionWorkspaceProps> = ({
  currentSessionId,
  onSelectSession,
  onOpenProof
}) => {
  const [activeSessionId, setActiveSessionId] = useState<string | undefined>(currentSessionId);
  const [sessionDetails, setSessionDetails] = useState<any>(null);

  const fetchSessionDetails = async (sid: string) => {
    try {
      const res = await fetch(`/api/research/sessions/${sid}`);
      if (res.ok) {
        const data = await res.json();
        setSessionDetails(data);
      }
    } catch (e) {
      console.error('Failed to fetch session details', e);
    }
  };

  useEffect(() => {
    if (activeSessionId) {
      fetchSessionDetails(activeSessionId);
    }
  }, [activeSessionId]);

  const handleCreateNewSession = async () => {
    try {
      const res = await fetch('/api/research/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New Research Investigation' })
      });
      if (res.ok) {
        const data = await res.json();
        setActiveSessionId(data.session_id);
        if (onSelectSession) onSelectSession(data.session_id);
      }
    } catch (e) {
      console.error('Failed to create session', e);
    }
  };

  const handleExport = async () => {
    if (!activeSessionId) return;
    try {
      const res = await fetch(`/api/research/sessions/${activeSessionId}/export`);
      if (res.ok) {
        const data = await res.json();
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `session_${activeSessionId}_export.json`;
        a.click();
      }
    } catch (e) {
      console.error('Failed to export session', e);
    }
  };

  return (
    <div className="w-full flex flex-col gap-6 p-6 bg-slate-50 min-h-screen">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <ResearchSessionsPanel
            activeSessionId={activeSessionId}
            onSelectSession={(sid) => {
              setActiveSessionId(sid);
              if (onSelectSession) onSelectSession(sid);
            }}
            onCreateNewSession={handleCreateNewSession}
          />
          {activeSessionId && <ResearchTimeline sessionId={activeSessionId} />}
        </div>

        <div className="lg:col-span-2 space-y-6">
          {sessionDetails ? (
            <>
              <ResearchSessionSummary sessionDetails={sessionDetails} onExport={handleExport} />
              <ResearchMemoryPanel sessionId={activeSessionId} onOpenProof={onOpenProof} />
            </>
          ) : (
            <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-500 font-medium">
              Select or create a Research Session to view investigation history, memories, and reproducible exports.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
