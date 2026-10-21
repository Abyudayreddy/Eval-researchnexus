import { Bell, CheckSquare } from 'lucide-react';

export default function NotificationsPage() {
  return (
    <div className="flex-1 flex flex-col h-full bg-[#FBFDFB]">
      {/* HEADER */}
      <header className="px-6 py-8 md:px-10 md:py-10 bg-white border-b border-slate-100 flex items-end justify-between shrink-0">
        <div>
          <h1 className="text-2xl md:text-3xl font-black text-slate-900 tracking-tight flex items-center gap-3">
            <Bell className="w-8 h-8 text-emerald-600" />
            Notifications
          </h1>
          <p className="text-sm font-medium text-slate-500 mt-2">
            Activity and alerts across your workspace
          </p>
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 overflow-y-auto bg-slate-50 p-6 md:p-10 flex flex-col items-center justify-center text-center">
        <div className="max-w-md mx-auto space-y-4 animate-in fade-in zoom-in-95 duration-500">
          <div className="w-20 h-20 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm border border-emerald-100">
            <CheckSquare className="w-10 h-10 text-emerald-500" />
          </div>
          <h2 className="text-xl font-black text-slate-900">You're all caught up.</h2>
          <p className="text-sm font-medium text-slate-500 leading-relaxed">
            New research and workspace activity will appear here. As you collaborate on projects, save papers, and run AI tasks, your notifications will be organized in a timeline.
          </p>
        </div>
      </div>
    </div>
  );
}
