import { CheckCircle2, AlertCircle, Info, AlertTriangle, X } from 'lucide-react';
import { useToastStore, Toast } from '../store/toastStore';
import { cn } from '../utils/cn';

export default function ToastContainer() {
  const toasts = useToastStore((state) => state.toasts);
  const removeToast = useToastStore((state) => state.removeToast);

  if (toasts.length === 0) return null;
  
  const getIcon = (type: Toast['type']) => {
    switch (type) {
      case 'success': return <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" />;
      case 'error': return <AlertCircle className="w-5 h-5 text-rose-500 shrink-0" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />;
      case 'info':
      default: return <Info className="w-5 h-5 text-blue-500 shrink-0" />;
    }
  };

  const getStyles = (type: Toast['type']) => {
    switch (type) {
      case 'success': return "bg-emerald-50/90 border-emerald-200 text-emerald-800";
      case 'error': return "bg-rose-50/90 border-rose-200 text-rose-800";
      case 'warning': return "bg-amber-50/90 border-amber-200 text-amber-800";
      case 'info':
      default: return "bg-blue-50/90 border-blue-200 text-blue-800";
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-[100] flex flex-col gap-3 pointer-events-none">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            "pointer-events-auto px-5 py-4 rounded-2xl shadow-2xl flex items-center gap-3 animate-in slide-in-from-bottom-5 fade-in duration-300 min-w-[300px] max-w-sm border backdrop-blur-md",
            getStyles(toast.type)
          )}
        >
          {getIcon(toast.type)}
          <p className="text-sm font-bold flex-1">{toast.message}</p>
          <button 
            onClick={() => removeToast(toast.id)}
            className="p-1 rounded-full transition-colors opacity-70 hover:opacity-100 hover:bg-slate-900/10"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
}
