import { ExperimentStatus } from '../utils/apiAdapter';
export default function ExperimentOverallStatus({ status }: { status: ExperimentStatus }) {
  const getMsg = () => {
    if (status.local.status === 'failed' && status.online.status === 'failed') return 'Both retrieval pipelines failed';
    if (status.local.status === 'failed') return 'Local retrieval failed — Online results available';
    if (status.online.status === 'failed') return 'Online retrieval failed — Local results available';
    if (status.overall_status === 'complete') return 'Retrieval Complete';
    return `Local ${status.local.status} / Online ${status.online.status}`;
  };
  return (
    <div className="w-full text-center py-2 text-sm font-medium text-slate-600 bg-slate-50 rounded-lg border border-slate-100">
      {getMsg()}
    </div>
  );
}
