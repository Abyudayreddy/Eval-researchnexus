import { Terminal } from 'lucide-react';

interface ContextInspectorProps {
  sessionId: string;
  searchId: string | null;
  contextSnapshotId?: string;
  snapshotVersion?: number;
  contextHash?: string;
  mode: string;
  scope: string;
  papers: Array<{ paper_id: string; title: string }>;
  evidence: Array<{ chunk_id: string }>;
  uploadedDocuments: Array<{ document_id: string; filename: string }>;
}

export const ContextInspector: React.FC<ContextInspectorProps> = ({
  sessionId,
  searchId,
  contextSnapshotId = 'pending-resolution',
  snapshotVersion = 1,
  contextHash = 'pending-generation',
  mode,
  scope,
  papers,
  evidence,
  uploadedDocuments,
}) => {
  return (
    <div className="space-y-6 pb-12">
      <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
        <Terminal className="w-4 h-4 text-emerald-600" />
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
          Resolution Trace Panel
        </span>
      </div>

      <div className="space-y-4">
        {/* Core Identifiers */}
        <div className="bg-slate-900 rounded-xl p-4 font-mono text-[10px] text-slate-350 space-y-3 leading-relaxed border border-slate-800 shadow-inner">
          <div>
            <span className="text-emerald-500 font-bold block">context_hash</span>
            <span className="break-all">{contextHash}</span>
          </div>
          <div>
            <span className="text-emerald-500 font-bold block">context_snapshot_id</span>
            <span className="break-all">{contextSnapshotId}</span>
          </div>
          <div>
            <span className="text-emerald-500 font-bold block">session_id</span>
            <span className="break-all">{sessionId || 'none-allocated'}</span>
          </div>
          <div>
            <span className="text-emerald-500 font-bold block">search_id</span>
            <span className="break-all">{searchId || 'none'}</span>
          </div>
          <div className="flex justify-between">
            <div>
              <span className="text-emerald-500 font-bold block">snapshot_version</span>
              <span>v{snapshotVersion}</span>
            </div>
            <div>
              <span className="text-emerald-500 font-bold block">scope</span>
              <span>{scope}</span>
            </div>
            <div>
              <span className="text-emerald-500 font-bold block">mode</span>
              <span>{mode}</span>
            </div>
          </div>
        </div>

        {/* Papers, Evidence, Upload lists */}
        <div className="space-y-3">
          <div>
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Permitted Papers ({papers.length})</span>
            <div className="max-h-24 overflow-y-auto border border-slate-200 rounded-lg p-2 bg-slate-50 space-y-1 text-xs">
              {papers.length === 0 ? (
                <span className="text-slate-400 italic">None resolving</span>
              ) : (
                papers.map(p => (
                  <div key={p.paper_id} className="text-slate-700 truncate font-semibold" title={p.title}>
                    [{p.paper_id.substring(0, 8)}] {p.title}
                  </div>
                ))
              )}
            </div>
          </div>

          <div>
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Permitted Chunks ({evidence.length})</span>
            <div className="max-h-24 overflow-y-auto border border-slate-200 rounded-lg p-2 bg-slate-50 space-y-1 text-xs">
              {evidence.length === 0 ? (
                <span className="text-slate-400 italic">None resolving</span>
              ) : (
                evidence.map(e => (
                  <div key={e.chunk_id} className="text-slate-700 truncate font-mono">
                    {e.chunk_id}
                  </div>
                ))
              )}
            </div>
          </div>

          <div>
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Ingested Documents ({uploadedDocuments.length})</span>
            <div className="max-h-24 overflow-y-auto border border-slate-200 rounded-lg p-2 bg-slate-50 space-y-1 text-xs">
              {uploadedDocuments.length === 0 ? (
                <span className="text-slate-400 italic">None resolving</span>
              ) : (
                uploadedDocuments.map(d => (
                  <div key={d.document_id} className="text-slate-700 truncate font-semibold">
                    [{d.document_id}] {d.filename}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
