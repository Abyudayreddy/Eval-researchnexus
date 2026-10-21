import React from 'react';
import { CheckCircle2, AlertTriangle, HelpCircle, XCircle, FileText, Activity } from 'lucide-react';

export interface ClaimProofDrawerProps {
  claim: {
    claim_id: string;
    text: string;
    claim_type: string;
    citation_ids: string[];
    evidence_ids: string[];
    claim_support_status: string;
    verification_method: string;
    verification_reason: string;
    citation_repaired?: boolean;
  };
  evidenceList: Array<{
    id?: string;
    paper_id?: string;
    chunk_id?: string;
    title?: string;
    authors?: string;
    evidence_text?: string;
    resolved_evidence_text?: string;
    section?: string;
    page?: string;
    source_type?: string;
    retrieval_source?: string;
  }>;
  searchId: string | null;
  onClose: () => void;
}

export const ClaimProofDrawer: React.FC<ClaimProofDrawerProps> = ({
  claim,
  evidenceList,
  searchId,
  onClose,
}) => {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'SUPPORTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <CheckCircle2 className="w-3.5 h-3.5" /> ✓ Supported
          </span>
        );
      case 'PARTIALLY_SUPPORTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            <AlertTriangle className="w-3.5 h-3.5" /> △ Partially Supported
          </span>
        );
      case 'INSUFFICIENT_EVIDENCE':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
            <HelpCircle className="w-3.5 h-3.5" /> ? Insufficient Evidence
          </span>
        );
      case 'UNSUPPORTED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            <XCircle className="w-3.5 h-3.5" /> × Unsupported
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-50 text-slate-700 border border-slate-200">
            <AlertTriangle className="w-3.5 h-3.5" /> ! Verification Unavailable
          </span>
        );
    }
  };

  // Find evidence objects matching claim evidence_ids
  const matchingEvidence = evidenceList.filter((ev) => {
    const eid = ev.chunk_id || ev.id || ev.paper_id;
    return claim.evidence_ids.includes(eid || '');
  });

  return (
    <div className="fixed inset-y-0 right-0 w-[480px] bg-white border-l border-slate-200 shadow-2xl z-50 flex flex-col">
      {/* Drawer Header */}
      <div className="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div>
          <h3 className="text-sm font-bold text-slate-800">Claim Proof & Grounding</h3>
          <p className="text-xs text-slate-500">Claim ID: {claim.claim_id} • Type: {claim.claim_type}</p>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition"
        >
          ✕
        </button>
      </div>

      {/* Drawer Body */}
      <div className="p-6 space-y-6 overflow-y-auto flex-1 text-xs">
        {/* Claim Text Box */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-slate-700">Claim Text</span>
            {getStatusBadge(claim.claim_support_status)}
          </div>
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 text-slate-800 font-medium leading-relaxed">
            "{claim.text}"
          </div>
        </div>

        {/* Verification Explanation */}
        <div className="space-y-2">
          <span className="font-semibold text-slate-700">Verification Verdict</span>
          <div className="p-3 bg-slate-900 rounded-xl text-slate-200 font-mono text-[11px] leading-relaxed border border-slate-800">
            <div className="text-emerald-400 font-bold mb-1">
              Method: {claim.verification_method} {claim.citation_repaired && '(Repaired Citation)'}
            </div>
            <div>{claim.verification_reason}</div>
          </div>
        </div>

        {/* Evidence Snippets */}
        <div className="space-y-3">
          <span className="font-semibold text-slate-700">
            Cited Evidence Objects ({matchingEvidence.length})
          </span>

          {matchingEvidence.length === 0 ? (
            <div className="p-4 rounded-xl bg-slate-50 border border-dashed border-slate-200 text-slate-400 text-center">
              No matching evidence objects bound to this claim in the current context.
            </div>
          ) : (
            matchingEvidence.map((ev, idx) => (
              <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-white space-y-2 shadow-sm">
                <div className="flex items-center justify-between text-slate-600 font-semibold">
                  <span className="truncate max-w-[280px] font-bold text-slate-800">
                    {ev.title || 'Untitled Paper'}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-600 uppercase font-mono">
                    {ev.source_type || ev.retrieval_source || 'local'}
                  </span>
                </div>
                {ev.authors && <p className="text-[11px] text-slate-500 truncate">{ev.authors}</p>}
                
                <div className="p-2.5 bg-slate-50 rounded-lg text-slate-700 leading-relaxed font-mono text-[11px]">
                  "{ev.evidence_text || ev.resolved_evidence_text || 'No text snippet available.'}"
                </div>

                <div className="flex items-center justify-between pt-1 text-[10px] text-slate-400 font-mono">
                  <span>Chunk: {ev.chunk_id || 'n/a'}</span>
                  {ev.section && <span>Section: {ev.section}</span>}
                  {ev.page && <span>Page: {ev.page}</span>}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Drawer Footer Actions */}
      <div className="p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between gap-3">
        <button
          onClick={() => {
            if (searchId) {
              window.location.href = `/xai?search_id=${searchId}`;
            } else {
              window.location.href = '/xai';
            }
          }}
          className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-lg bg-white border border-slate-300 text-slate-700 hover:bg-slate-100 transition shadow-sm"
        >
          <Activity className="w-3.5 h-3.5 text-emerald-600" />
          Show Retrieval Explanation
        </button>

        {matchingEvidence.length > 0 && matchingEvidence[0].paper_id && (
          <button
            onClick={() => {
              window.location.href = `/reader/${matchingEvidence[0].paper_id}`;
            }}
            className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition shadow-sm"
          >
            <FileText className="w-3.5 h-3.5" />
            Open Paper
          </button>
        )}
      </div>
    </div>
  );
};
