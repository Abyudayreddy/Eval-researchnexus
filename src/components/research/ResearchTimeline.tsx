import React, { useState, useEffect } from 'react';
import { Clock } from 'lucide-react';

interface ActivityEvent {
  artifact_id: string;
  artifact_type: string;
  artifact_ref: string;
  title: string;
  created_at: string;
}

interface ResearchTimelineProps {
  sessionId?: string;
}

export const ResearchTimeline: React.FC<ResearchTimelineProps> = ({ sessionId }) => {
  const [timeline, setTimeline] = useState<ActivityEvent[]>([]);

  useEffect(() => {
    if (!sessionId) return;
    fetch(`/api/research/sessions/${sessionId}/activity`)
      .then(res => res.json())
      .then(data => setTimeline(data))
      .catch(err => console.error('Failed to fetch activity timeline', err));
  }, [sessionId]);

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
      <div className="flex items-center gap-2">
        <Clock className="w-4 h-4 text-blue-600" />
        <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Research Activity Chronology ({timeline.length})</h3>
      </div>

      <div className="space-y-2 border-l-2 border-slate-200 pl-4">
        {timeline.map((evt) => (
          <div key={evt.artifact_id} className="relative space-y-0.5">
            <div className="w-2.5 h-2.5 rounded-full bg-blue-500 absolute -left-[21px] top-1 border-2 border-white"></div>
            <div className="flex items-center justify-between text-xs">
              <span className="font-extrabold text-slate-800 uppercase text-[10px] px-2 py-0.5 bg-slate-100 rounded">
                {evt.artifact_type}
              </span>
              <span className="text-[10px] text-slate-400 font-medium">{evt.created_at ? new Date(evt.created_at).toLocaleTimeString() : ''}</span>
            </div>
            <p className="text-xs text-slate-700 font-medium">{evt.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
