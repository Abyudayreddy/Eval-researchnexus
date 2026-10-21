const fs = require('fs');
const path = require('path');

const dir = 'c:/Users/Abyureddy/OneDrive/Desktop/SDC2/src/components/xai';
if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

fs.writeFileSync(path.join(dir, 'XaiHeader.tsx'), `
import React from 'react';

interface XaiHeaderProps {
  query: string;
  localCount: number;
  onlineCount: number;
}

export function XaiHeader({ query, localCount, onlineCount }: XaiHeaderProps) {
  return (
    <div className="bg-white border-b border-slate-200 px-6 py-4">
      <h1 className="text-xl font-bold text-slate-900">Explainable Research</h1>
      <p className="text-sm text-slate-500 mt-1">
        Query: <span className="font-medium text-slate-700">"{query}"</span>
      </p>
      <div className="flex gap-4 mt-3 text-xs">
        <div className="bg-slate-100 px-2 py-1 rounded">Local: <span className="font-bold">{localCount}</span></div>
        <div className="bg-slate-100 px-2 py-1 rounded">Online: <span className="font-bold">{onlineCount}</span></div>
        <div className="bg-slate-100 px-2 py-1 rounded">Unique: <span className="font-bold">{localCount + onlineCount}</span></div>
      </div>
    </div>
  );
}
`);

fs.writeFileSync(path.join(dir, 'XaiSourceToggle.tsx'), `
import React from 'react';

interface XaiSourceToggleProps {
  source: 'LOCAL' | 'ONLINE';
  onChange: (source: 'LOCAL' | 'ONLINE') => void;
}

export function XaiSourceToggle({ source, onChange }: XaiSourceToggleProps) {
  return (
    <div className="flex gap-2 mb-6">
      <button
        onClick={() => onChange('LOCAL')}
        className={\`px-4 py-2 text-sm font-bold rounded-lg transition-colors \${
          source === 'LOCAL' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
        }\`}
      >
        [ LOCAL RETRIEVAL ]
      </button>
      <button
        onClick={() => onChange('ONLINE')}
        className={\`px-4 py-2 text-sm font-bold rounded-lg transition-colors \${
          source === 'ONLINE' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
        }\`}
      >
        [ ONLINE RETRIEVAL ]
      </button>
    </div>
  );
}
`);

fs.writeFileSync(path.join(dir, 'XaiOverview.tsx'), `
import React from 'react';

interface XaiOverviewProps {
  metrics: {
    candidateCount?: number;
    filteredCount?: number;
    finalCount?: number;
    latency?: string;
  };
}

export function XaiOverview({ metrics }: XaiOverviewProps) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 flex gap-6 mb-6">
      {metrics.candidateCount !== undefined && (
        <div>
          <div className="text-xs text-slate-500 uppercase tracking-wider">Candidates</div>
          <div className="text-lg font-bold text-slate-900">{metrics.candidateCount}</div>
        </div>
      )}
      {metrics.filteredCount !== undefined && (
        <div>
          <div className="text-xs text-slate-500 uppercase tracking-wider">Filtered</div>
          <div className="text-lg font-bold text-slate-900">{metrics.filteredCount}</div>
        </div>
      )}
      {metrics.finalCount !== undefined && (
        <div>
          <div className="text-xs text-slate-500 uppercase tracking-wider">Final</div>
          <div className="text-lg font-bold text-slate-900">{metrics.finalCount}</div>
        </div>
      )}
      {metrics.latency && (
        <div>
          <div className="text-xs text-slate-500 uppercase tracking-wider">Latency</div>
          <div className="text-lg font-bold text-slate-900">{metrics.latency}</div>
        </div>
      )}
    </div>
  );
}
`);

fs.writeFileSync(path.join(dir, 'XaiRetrievalFlow.tsx'), `
import React from 'react';

interface XaiRetrievalFlowProps {
  stages: { name: string; count: number; active?: boolean }[];
}

export function XaiRetrievalFlow({ stages }: XaiRetrievalFlowProps) {
  return (
    <div className="flex items-center gap-4 py-4 overflow-x-auto">
      {stages.map((stage, i) => (
        <React.Fragment key={stage.name}>
          <div className={\`flex flex-col items-center p-3 rounded-lg border \${stage.active ? 'border-indigo-500 bg-indigo-50' : 'border-slate-200 bg-white'}\`}>
            <span className="text-xs font-bold text-slate-600">{stage.name}</span>
            <span className="text-lg font-black text-indigo-700">{stage.count}</span>
          </div>
          {i < stages.length - 1 && (
            <div className="h-px w-8 bg-slate-300"></div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
`);

fs.writeFileSync(path.join(dir, 'XaiEvidenceGraph.tsx'), `
import React from 'react';

export function XaiEvidenceGraph() {
  return (
    <div className="absolute inset-0 pointer-events-none opacity-5 z-0" style={{
      backgroundImage: 'radial-gradient(circle at 2px 2px, #4f46e5 1px, transparent 0)',
      backgroundSize: '24px 24px'
    }}>
      {/* Visual metaphor placeholder */}
    </div>
  );
}
`);

fs.writeFileSync(path.join(dir, 'XaiEvidencePanel.tsx'), `
import React from 'react';

interface XaiEvidencePanelProps {
  evidence: string;
}

export function XaiEvidencePanel({ evidence }: XaiEvidencePanelProps) {
  return (
    <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-xl mt-4 relative z-10">
      <h3 className="text-xs font-bold text-emerald-800 uppercase tracking-widest mb-2">Evidence</h3>
      <p className="text-sm text-emerald-900 italic">"{evidence}"</p>
    </div>
  );
}
`);
console.log('Done writing files.');
