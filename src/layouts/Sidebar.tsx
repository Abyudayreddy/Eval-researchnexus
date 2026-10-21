import { NavLink } from 'react-router-dom';
import { 
  Home, 
  Search, 
  Library, 
  Settings,
  BrainCircuit,
  BookOpen,
  BookMarked,
  Briefcase,
  Bot,
  Compass,
  ArrowRight,
  TrendingUp,
  ChevronRight,
  Bell
} from 'lucide-react';
import { cn } from '../utils/cn';
import { useAuthStore } from '../store/authStore';

const navigationGroups = [
  {
    name: 'Research',
    items: [
      { name: 'Dashboard', href: '/dashboard', icon: Home },
      { name: 'Domains', href: '/research-domains', icon: Compass },
      { name: 'Research Explorer', href: '/hybrid-search', icon: Search },
      { name: 'AI Assistant', href: '/assistant', icon: Bot },
    ]
  },
  {
    name: 'Workspace',
    items: [
      { name: 'Projects', href: '/research', icon: Briefcase },
      { name: 'Notebook', href: '/notebook', icon: BookOpen },
      { name: 'Paper Library', href: '/paper-library', icon: BookMarked },
      { name: 'Literature Review', href: '/literature-review', icon: Library },
    ]
  },
  {
    name: 'Intelligence',
    items: [
      { name: 'Explainable AI', href: '/xai', icon: BrainCircuit },
      { name: 'Analytics', href: '/analytics', icon: TrendingUp },
    ]
  },
  {
    name: 'Account',
    items: [
      { name: 'Notifications', href: '/notifications', icon: Bell },
      { name: 'Settings', href: '/settings', icon: Settings },
    ]
  }
];

interface SidebarProps {
  isCollapsed?: boolean;
  toggleCollapse?: () => void;
}

export default function Sidebar({ isCollapsed = false, toggleCollapse }: SidebarProps) {
  const { user } = useAuthStore();
  return (
    <div className={cn("border-r border-[var(--border-color)] bg-[var(--bg-card)] flex-col hidden md:flex h-screen fixed top-0 left-0 z-30 transition-all duration-300", isCollapsed ? "w-[72px]" : "w-64")}>
      
      {toggleCollapse && (
        <button 
          onClick={toggleCollapse}
          className="absolute -right-3 top-6 w-6 h-6 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-full flex items-center justify-center text-[var(--text-muted)] hover:text-[var(--accent-primary)] hover:border-[var(--accent-primary)] shadow-sm transition-colors z-50 hidden md:flex"
        >
          <ChevronRight className={cn("w-3.5 h-3.5 transition-transform duration-300", !isCollapsed && "rotate-180")} />
        </button>
      )}

      <div className={cn("h-16 flex items-center border-b border-[var(--border-subtle)] shrink-0", isCollapsed ? "justify-center px-0" : "gap-3 px-6")}>
        <div className="w-8 h-8 rounded-lg bg-[var(--accent-primary)] flex items-center justify-center text-white shadow-sm hover:scale-105 transition-transform duration-300 shrink-0">
          <BookOpen className="w-5 h-5 fill-current" />
        </div>
        {!isCollapsed && (
          <div className="overflow-hidden whitespace-nowrap opacity-100 transition-opacity duration-300">
            <span className="font-bold text-[var(--text-main)] tracking-tight text-[15px]">ResearchNexus AI</span>
            <span className="text-[9px] block text-[var(--text-muted)] font-semibold tracking-wider uppercase -mt-0.5">Scientific OS</span>
          </div>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        <nav className="space-y-6">
          {navigationGroups.map((group) => (
            <div key={group.name}>
              {!isCollapsed && <h4 className="px-3 mb-2 text-[10px] font-bold uppercase tracking-widest text-[var(--text-muted)]">{group.name}</h4>}
              <div className="space-y-0.5">
                {group.items.map((item) => (
                  <NavLink
                    key={item.name}
                    to={item.href}
                    title={isCollapsed ? item.name : undefined}
                    className={({ isActive }) =>
                      cn(
                        "w-full flex items-center rounded-xl transition-all duration-200 text-[13px]",
                        isCollapsed ? "justify-center p-3" : "gap-3 px-3 py-2.5 text-left",
                        isActive
                          ? "nav-active"
                          : "text-[var(--text-sub)] hover:bg-[var(--bg-card-hover)] hover:text-[var(--text-main)]"
                      )
                    }
                  >
                    <item.icon className="w-4 h-4 shrink-0" aria-hidden="true" />
                    {!isCollapsed && <span className="whitespace-nowrap overflow-hidden">{item.name}</span>}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>

        {!isCollapsed && (
          <div className="mt-6 p-4 rounded-2xl bg-[var(--accent-soft)] border border-[var(--border-color)] relative overflow-hidden">
            <div className="flex items-center justify-between">
              <span className="font-bold text-[var(--accent-primary)] text-[10px] uppercase tracking-wider">Research Assistant</span>
              <span className="w-2 h-2 rounded-full bg-[var(--accent-primary)] animate-pulse"></span>
            </div>
            <p className="text-[var(--text-muted)] text-[10px] mt-1 leading-relaxed">Your AI companion for every research step.</p>
            
            <NavLink to="/assistant" className="mt-3 w-full bg-[var(--bg-card)] hover:bg-[var(--bg-card-hover)] text-[var(--text-main)] font-bold py-1.5 px-3 rounded-xl border border-[var(--border-color)] text-xs flex items-center justify-between transition-colors shadow-xs">
              <span>Chat Now</span>
              <ArrowRight className="w-3.5 h-3.5 text-[var(--text-muted)]" />
            </NavLink>
          </div>
        )}
      </div>
      
      <div className={cn("p-4 border-t border-[var(--border-subtle)] flex items-center shrink-0", isCollapsed ? "justify-center" : "justify-between")}>
        <NavLink to="/settings" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-full bg-[var(--accent-primary)] text-white flex items-center justify-center font-bold text-sm shadow-inner shrink-0 group-hover:scale-105 transition-transform uppercase">
            {user?.name?.charAt(0) || 'U'}
          </div>
          {!isCollapsed && (
            <div className="overflow-hidden whitespace-nowrap group-hover:opacity-80 transition-opacity">
              <p className="font-bold text-[var(--text-main)] text-xs truncate">{user?.name || 'User'}</p>
              <p className="text-[10px] text-[var(--text-muted)] font-semibold truncate">{user?.title || 'Researcher'}</p>
            </div>
          )}
        </NavLink>
        {!isCollapsed && (
          <NavLink to="/settings" className="p-1.5 hover:bg-[var(--bg-card-hover)] rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] transition-colors shrink-0" title="Settings">
            <Settings className="w-4 h-4" />
          </NavLink>
        )}
      </div>
    </div>
  );
}
