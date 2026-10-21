import { ExperimentStage } from '../utils/apiAdapter';
export default function OnlineProgressPanel({ online }: { online: ExperimentStage & { status: string } }) {
  return (
    <div className="flex flex-col gap-2 p-4 bg-blue-50 border border-blue-100 rounded-lg w-full">
      <div className="flex justify-between items-center">
        <span className="text-xs font-bold text-blue-800 uppercase tracking-wider">ONLINE RESEARCH</span>
        <span className="text-xs font-medium text-blue-600">{online.status === 'failed' ? 'Failed' : online.progress !== null ? `${Math.round(online.progress * 100)}%` : '...'}</span>
      </div>
      <div className="text-sm font-medium text-blue-700">{online.stage}</div>
      {online.progress !== null ? (
        <div className="w-full bg-blue-200 rounded-full h-1.5">
          <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: `${online.progress * 100}%` }}></div>
        </div>
      ) : (
        <div className="w-full bg-blue-200 rounded-full h-1.5 overflow-hidden">
          <div className="bg-blue-600 h-1.5 rounded-full w-1/3 animate-[pulse_1s_ease-in-out_infinite]"></div>
        </div>
      )}
    </div>
  );
}
