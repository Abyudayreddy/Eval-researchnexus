import React from 'react';

interface PaperInfo {
  id: string;
  title: string;
  authors: string;
}

interface CompareTableProps {
  papers: PaperInfo[];
}

export const CompareTable: React.FC<CompareTableProps> = ({ papers }) => {
  const dimensions = [
    { key: 'method', label: 'Method / Approach' },
    { key: 'dataset', label: 'Dataset Used' },
    { key: 'model', label: 'Model Architecture' },
    { key: 'evaluation', label: 'Evaluation Metrics' },
    { key: 'results', label: 'Reported Results' },
    { key: 'limitations', label: 'Limitations' },
  ];

  return (
    <div className="w-full overflow-x-auto border border-slate-200 rounded-xl bg-white shadow-sm">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-200">
            <th className="p-4 text-xs font-black text-slate-700 uppercase tracking-wider w-1/4">Dimension</th>
            {papers.map((p, idx) => (
              <th key={p.id} className="p-4 text-xs font-black text-slate-700 uppercase tracking-wider">
                Paper [{idx + 1}]: {p.title.substring(0, 30)}...
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 text-xs">
          {dimensions.map((dim) => (
            <tr key={dim.key} className="hover:bg-slate-50/50">
              <td className="p-4 font-bold text-slate-500 bg-slate-50/20">{dim.label}</td>
              {papers.map((p) => (
                <td key={p.id} className="p-4 text-slate-600 font-medium">
                  <span className="text-slate-400 italic">No verified data resolved for this dimension yet.</span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
