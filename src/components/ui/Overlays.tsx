import { X } from 'lucide-react';
import { cn } from '../../utils/cn';
import { useOverlayStore } from '../../store/overlayStore';

// Common backdrop
const Backdrop = ({ onClick }: { onClick: () => void }) => (
  <div 
    className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-50 animate-in fade-in duration-200" 
    onClick={onClick} 
  />
);

export function CenteredSheet({ 
  id, 
  title, 
  children, 
  className 
}: { 
  id: string; 
  title?: string; 
  children: React.ReactNode; 
  className?: string; 
}) {
  const { activeOverlay, overlayData, closeOverlay } = useOverlayStore();
  const isOpen = activeOverlay === 'centered_sheet' && overlayData?.id === id;

  if (!isOpen) return null;

  return (
    <>
      <Backdrop onClick={closeOverlay} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-6 pointer-events-none">
        <div className={cn("relative bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden animate-in zoom-in-95 duration-200 pointer-events-auto", className)}>
          {title && (
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 shrink-0">
              <h2 className="text-lg font-black text-slate-800">{title}</h2>
              <button onClick={closeOverlay} className="p-2 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-50 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
          )}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
            {children}
          </div>
        </div>
      </div>
    </>
  );
}

export function SideDrawer({ 
  id, 
  title, 
  children, 
  position = 'right' 
}: { 
  id: string; 
  title?: string; 
  children: React.ReactNode; 
  position?: 'left' | 'right'; 
}) {
  const { activeOverlay, overlayData, closeOverlay } = useOverlayStore();
  const isOpen = activeOverlay === 'side_drawer' && overlayData?.id === id;

  if (!isOpen) return null;

  return (
    <>
      <Backdrop onClick={closeOverlay} />
      <div className={cn(
        "fixed top-0 bottom-0 z-50 w-full max-w-sm bg-white shadow-2xl flex flex-col animate-in duration-300",
        position === 'right' ? "right-0 slide-in-from-right" : "left-0 slide-in-from-left"
      )}>
        {title && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 shrink-0">
            <h2 className="text-lg font-black text-slate-800">{title}</h2>
            <button onClick={closeOverlay} className="p-2 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-50 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
        )}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-hide">
          {children}
        </div>
      </div>
    </>
  );
}

export function ActionSheet({ 
  id, 
  title, 
  children 
}: { 
  id: string; 
  title: string; 
  children: React.ReactNode; 
}) {
  const { activeOverlay, overlayData, closeOverlay } = useOverlayStore();
  const isOpen = activeOverlay === 'action_sheet' && overlayData?.id === id;

  if (!isOpen) return null;

  return (
    <>
      <Backdrop onClick={closeOverlay} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="relative bg-white rounded-xl shadow-xl w-full max-w-sm flex flex-col overflow-hidden animate-in zoom-in-95 duration-200 pointer-events-auto">
          <div className="flex items-center justify-between px-5 py-3 border-b border-slate-100 bg-slate-50/50 shrink-0">
            <h3 className="text-sm font-bold text-slate-800">{title}</h3>
            <button onClick={closeOverlay} className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200/50 transition-colors">
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="p-5">
            {children}
          </div>
        </div>
      </div>
    </>
  );
}

export function ConfirmationSheet({ 
  id, 
  title, 
  description, 
  confirmText = "Confirm", 
  cancelText = "Cancel", 
  onConfirm,
  destructive = true
}: { 
  id: string; 
  title: string; 
  description: string; 
  confirmText?: string; 
  cancelText?: string; 
  onConfirm: () => void;
  destructive?: boolean;
}) {
  const { activeOverlay, overlayData, closeOverlay } = useOverlayStore();
  const isOpen = activeOverlay === 'confirmation_sheet' && overlayData?.id === id;

  if (!isOpen) return null;

  return (
    <>
      <Backdrop onClick={closeOverlay} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="relative bg-white rounded-xl shadow-xl w-full max-w-sm overflow-hidden animate-in zoom-in-95 duration-200 pointer-events-auto p-6 text-center">
          <h3 className="text-lg font-black text-slate-900 mb-2">{title}</h3>
          <p className="text-sm text-slate-500 mb-6 font-medium">{description}</p>
          <div className="flex flex-col gap-2">
            <button 
              onClick={() => {
                onConfirm();
                closeOverlay();
              }}
              className={cn("w-full py-2.5 rounded-lg text-sm font-bold text-white transition-colors", destructive ? "bg-rose-600 hover:bg-rose-700" : "bg-emerald-600 hover:bg-emerald-700")}
            >
              {confirmText}
            </button>
            <button 
              onClick={closeOverlay}
              className="w-full py-2.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-sm font-bold transition-colors"
            >
              {cancelText}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
