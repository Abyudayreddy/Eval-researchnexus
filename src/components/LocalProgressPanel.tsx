import { ExperimentStage } from '../utils/apiAdapter';
export default function LocalProgressPanel({ local }: { local: ExperimentStage & { status: string } }) {
  return (
    <div className="flex flex-col gap-2 p-4 bg-emerald-50 border border-emerald-100 rounded-lg w-full">
      <div className="flex justify-between items-center">
        <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider">LOCAL RESEARCH</span>
        <span className="text-xs font-medium text-emerald-600">{local.status === 'failed' ? 'Failed' : local.progress !== null ? `${Math.round(local.progress * 100)}%` : '...'}</span>
      </div>
      <div className="text-sm font-medium text-emerald-700">{local.stage}</div>
      {local.progress !== null ? (
        <div className="w-full bg-emerald-200 rounded-full h-1.5">
          <div className="bg-emerald-600 h-1.5 rounded-full" style={{ width: `${local.progress * 100}%` }}></div>
        </div>
      ) : (
        <div className="w-full bg-emerald-200 rounded-full h-1.5 overflow-hidden">
          <div className="bg-emerald-600 h-1.5 rounded-full w-1/3 animate-[pulse_1s_ease-in-out_infinite]"></div>
        </div>
      )}
    </div>
  );
}
