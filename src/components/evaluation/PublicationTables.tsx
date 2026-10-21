import React, { useState, useEffect } from 'react';
import { Download } from 'lucide-react';

interface PublicationTablesProps {
  claims: any[];
}

export const PublicationTables: React.FC<PublicationTablesProps> = ({ claims }) => {
  const [exportPackage, setExportPackage] = useState<any>(null);

  useEffect(() => {
    fetch('/api/evaluation/export/tables')
      .then(res => res.json())
      .then(data => setExportPackage(data))
      .catch(err => console.error('Failed to fetch export tables', err));
  }, []);

  const handleDownloadPackage = () => {
    if (!exportPackage) return;
    const jsonStr = JSON.stringify(exportPackage, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'publication_reproducibility_package.json';
    a.click();
  };

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-black text-slate-900">Publication Tables & Claim Audit</h2>
          <p className="text-xs text-slate-500 font-medium mt-0.5">
            Automatic Markdown/CSV publication tables & claim audit engine (Zero manual number editing)
          </p>
        </div>

        <button
          onClick={handleDownloadPackage}
          className="flex items-center gap-1.5 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
        >
          <Download className="w-3.5 h-3.5" /> Download Reproducibility Package
        </button>
      </div>

      {/* Publication Claims Audit Table */}
      <div className="space-y-3">
        <h3 className="text-xs font-black text-slate-800 uppercase tracking-wider">Publication Claim Fact-Check Audit ({claims.length})</h3>
        <div className="overflow-x-auto border border-slate-200 rounded-xl">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-100 font-extrabold text-slate-700 uppercase border-b border-slate-200">
              <tr>
                <th className="p-3">Publication Claim Text</th>
                <th className="p-3">Evidence Source</th>
                <th className="p-3">Audit Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 font-medium text-slate-800">
              {claims.map((c) => {
                const isSupported = c.status === 'SUPPORTED';
                const isNotMeasured = c.status === 'NOT_MEASURED';

                return (
                  <tr key={c.claim_id} className="bg-white">
                    <td className="p-3 font-bold text-slate-900">{c.text}</td>
                    <td className="p-3 text-slate-500 font-mono text-[11px]">{c.evidence_source}</td>
                    <td className="p-3">
                      <span className={`text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full ${
                        isSupported ? 'bg-emerald-100 text-emerald-800' :
                        isNotMeasured ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'
                      }`}>
                        {c.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Markdown Tables Output */}
      {exportPackage && (
        <div className="space-y-4 pt-4 border-t border-slate-200">
          <h3 className="text-xs font-black text-slate-800 uppercase tracking-wider">Generated IEEE Paper Markdown Tables</h3>
          <div className="bg-slate-900 text-slate-100 font-mono p-4 rounded-xl text-xs overflow-x-auto whitespace-pre-wrap space-y-4">
            <div>{exportPackage.tables?.table1_datasets}</div>
            <div>{exportPackage.tables?.table2_retrieval}</div>
            <div>{exportPackage.tables?.table3_ablation}</div>
          </div>
        </div>
      )}
    </div>
  );
};
