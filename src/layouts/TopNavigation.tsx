import { useState, useRef, useEffect } from 'react';
import { Search, Menu, Bell, Library, Bot, Briefcase } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { ThemeToggle } from '../components/ThemeToggle';

export default function TopNavigation({ openCommandPalette }: { openCommandPalette?: () => void }) {
  const [showNotifDropdown, setShowNotifDropdown] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const userDropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowNotifDropdown(false);
      }
      if (userDropdownRef.current && !userDropdownRef.current.contains(event.target as Node)) {
        setShowUserDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="h-16 border-b border-[var(--border-subtle)] bg-[var(--bg-card)]/95 backdrop-blur-md sticky top-0 z-20 px-8 flex items-center justify-between shrink-0">
      
      <div className="flex flex-1 items-center md:hidden">
        <button type="button" className="-ml-2 p-2 text-[var(--text-muted)] hover:bg-[var(--bg-card-hover)] rounded-md">
          <span className="sr-only">Open sidebar</span>
          <Menu className="h-6 w-6" aria-hidden="true" />
        </button>
      </div>

      {/* Compact Quick Search */}
      <div className="hidden md:flex flex-1 justify-center relative">
        <button 
          onClick={openCommandPalette}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[var(--bg-surface)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-color)] text-[var(--text-muted)] hover:text-[var(--text-main)] transition-colors cursor-pointer group shadow-xs"
        >
          <Search className="w-3.5 h-3.5" />
          <span className="text-[11px] font-bold">Quick Search...</span>
          <span className="text-[9px] bg-[var(--bg-card)] border border-[var(--border-color)] text-[var(--text-muted)] font-mono px-1.5 py-0.5 rounded ml-2">Ctrl K</span>
        </button>
      </div>

      {/* Quick stats indicators */}
      <div className="flex items-center gap-3 justify-end flex-1 md:flex-none">
        {/* Visual Environment / Theme Switcher */}
        <ThemeToggle compact={false} />

        <div className="relative" ref={dropdownRef}>
          <button 
            onClick={() => setShowNotifDropdown(!showNotifDropdown)}
            className="p-2 hover:bg-[var(--bg-card-hover)] rounded-full text-[var(--text-muted)] hover:text-[var(--text-main)] transition-colors relative"
            title="Notifications"
          >
            <Bell className="w-4.5 h-4.5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500 animate-pulse border-2 border-[var(--bg-card)]"></span>
          </button>

          {showNotifDropdown && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                <h3 className="text-[13px] font-bold text-slate-800">Notifications</h3>
                <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">2 Unread</span>
              </div>
              <div className="max-h-[320px] overflow-y-auto">
                {[
                  { id: 1, title: 'New paper added to your library', time: '2 mins ago', icon: Library, bg: 'bg-indigo-100 text-indigo-600', unread: true },
                  { id: 2, title: 'AI Summary Generated Successfully', time: '1 hour ago', icon: Bot, bg: 'bg-emerald-100 text-emerald-600', unread: true },
                  { id: 3, title: 'Project Update: BioResearch Beta', time: '3 hours ago', icon: Briefcase, bg: 'bg-blue-100 text-blue-600', unread: false },
                ].map((notif) => (
                  <div key={notif.id} className="p-4 border-b border-slate-50 hover:bg-slate-50 cursor-pointer transition-colors flex gap-3 group relative">
                    {notif.unread && <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500"></div>}
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${notif.bg}`}>
                      <notif.icon className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className={`text-xs ${notif.unread ? 'font-bold text-slate-900' : 'font-semibold text-slate-700'}`}>{notif.title}</h4>
                      <p className="text-[10px] text-slate-400 font-medium mt-1">{notif.time}</p>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-3 bg-slate-50 text-center">
                <button 
                  onClick={() => {
                    setShowNotifDropdown(false);
                    navigate('/notifications');
                  }}
                  className="text-xs font-bold text-emerald-600 hover:text-emerald-700 transition-colors w-full p-2"
                >
                  View All Notifications
                </button>
              </div>
            </div>
          )}
        </div>

        <span className="h-5 w-px bg-slate-200 hidden sm:block"></span>

        <div className="relative" ref={userDropdownRef}>
          <div 
            onClick={() => setShowUserDropdown(!showUserDropdown)}
            className="w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-xs shadow-sm cursor-pointer hidden sm:flex"
          >
            {user?.name?.charAt(0) || 'U'}
          </div>
          
          {showUserDropdown && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-slate-100 overflow-hidden z-50">
              <div className="px-4 py-3 border-b border-slate-50">
                <p className="text-[13px] font-bold text-slate-800 truncate">{user?.name}</p>
                <p className="text-[11px] font-medium text-slate-500 truncate">{user?.email}</p>
              </div>
              <div className="p-1">
                <button 
                  onClick={() => {
                    logout();
                    navigate('/login');
                  }}
                  className="w-full text-left px-3 py-2 text-xs font-semibold text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                >
                  Sign out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
