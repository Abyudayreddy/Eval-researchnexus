import React, { useState } from 'react';
import { Check } from 'lucide-react';

interface HumanEvalPanelProps {
  experimentId: string;
  itemId: string;
}

export const HumanEvalPanel: React.FC<HumanEvalPanelProps> = ({ experimentId, itemId }) => {
  const [ratings, setRatings] = useState<{ [key: string]: number }>({
    Correctness: 4,
    Relevance: 5,
    Groundedness: 4,
    'Citation Quality': 5,
    Completeness: 4,
    Usefulness: 4,
    Clarity: 5
  });
  const [comments, setComments] = useState<string>('');
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const dimensions = [
    'Correctness',
    'Relevance',
    'Groundedness',
    'Citation Quality',
    'Completeness',
    'Usefulness',
    'Clarity'
  ];

  const handleRatingChange = (dim: string, val: number) => {
    setRatings(prev => ({ ...prev, [dim]: val }));
  };

  const handleSubmit = async () => {
    try {
      const res = await fetch('/api/evaluation/human-eval', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          experiment_id: experimentId,
          item_id: itemId,
          evaluator_id: 'evaluator_user',
          system_label: 'System A',  // Blinded system identity
          ratings,
          comments
        })
      });
      if (res.ok) setIsSubmitted(true);
    } catch (e) {
      console.error('Failed to submit human evaluation', e);
    }
  };

  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 bg-slate-100 font-extrabold text-[10px] text-slate-700 rounded uppercase">
              Blinded Evaluation: System A
            </span>
          </div>
          <h2 className="text-base font-black text-slate-900 mt-1">Blinded Human Evaluation Rubric</h2>
          <p className="text-xs text-slate-500 font-medium">Rate response across 7 independent dimensions (1–5 scale)</p>
        </div>
      </div>

      <div className="space-y-4">
        {dimensions.map((dim) => (
          <div key={dim} className="flex items-center justify-between bg-slate-50 p-3 rounded-xl border border-slate-200">
            <span className="text-xs font-bold text-slate-800">{dim}</span>
            <div className="flex items-center gap-1">
              {[1, 2, 3, 4, 5].map((val) => (
                <button
                  key={val}
                  onClick={() => handleRatingChange(dim, val)}
                  className={`w-7 h-7 rounded-lg text-xs font-black transition ${
                    ratings[dim] === val ? 'bg-purple-600 text-white shadow-sm' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                  }`}
                >
                  {val}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <label className="text-xs font-bold text-slate-700">Evaluator Comments / Feedback</label>
        <textarea
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          placeholder="Enter detailed qualitative observations..."
          className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 font-medium focus:outline-none focus:border-purple-500"
        />
      </div>

      <div className="flex items-center justify-between">
        <button
          onClick={handleSubmit}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
        >
          Submit Evaluation Ratings
        </button>

        {isSubmitted && <span className="text-xs font-bold text-emerald-600 flex items-center gap-1"><Check className="w-4 h-4" /> Ratings Recorded</span>}
      </div>
    </div>
  );
};
