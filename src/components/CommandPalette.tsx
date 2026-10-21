import { useState, useEffect, useRef } from 'react';
import { 
  Search, FileText, Briefcase, Bot, BookOpen, Library,
  Settings, Activity, Layout,
  X, CornerDownLeft
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { cn } from '../utils/cn';

const COMMANDS = [
  // Pages
  { id: 'p1', title: 'Dashboard', category: 'Research Pages', icon: Layout, route: '/dashboard', type: 'page' },
  { id: 'p2', title: 'Hybrid Search', category: 'Research Pages', icon: Search, route: '/hybrid-search', type: 'page' },
  { id: 'p3', title: 'AI Assistant', category: 'Research Pages', icon: Bot, route: '/assistant', type: 'page' },
  { id: 'p4', title: 'Notebook', category: 'Research Pages', icon: BookOpen, route: '/notebook', type: 'page' },
  { id: 'p5', title: 'Projects', category: 'Research Pages', icon: Briefcase, route: '/projects', type: 'page' },
  { id: 'p6', title: 'Paper Library', category: 'Research Pages', icon: Library, route: '/paper-library', type: 'page' },
  { id: 'p7', title: 'Settings', category: 'Research Pages', icon: Settings, route: '/settings', type: 'page' },
  { id: 'p8', title: 'Profile', category: 'Research Pages', icon: Activity, route: '/profile', type: 'page' },

  // Commands
  { id: 'c1', title: 'Create New Project', category: 'Commands', icon: Briefcase, type: 'command' },
  { id: 'c2', title: 'Create New Note', category: 'Commands', icon: BookOpen, type: 'command' },
  { id: 'c3', title: 'Generate Literature Review', category: 'Commands', icon: Library, type: 'command' },
  { id: 'c4', title: 'Compare Papers', category: 'Commands', icon: FileText, type: 'command' },
  
  // Papers
  { id: 'r1', title: 'Retrieval-Augmented Generation', subtitle: 'Lewis et al. • 2024', category: 'Research Papers', icon: FileText, route: '/paper-library', type: 'paper' },
  { id: 'r2', title: 'Attention Is All You Need', subtitle: 'Vaswani et al. • 2017', category: 'Research Papers', icon: FileText, route: '/paper-library', type: 'paper' },

  // Projects
  { id: 'pr1', title: 'BioResearch Beta', subtitle: 'Active • 4 Members', category: 'Projects', icon: Briefcase, route: '/projects', type: 'project' },
];

export default function CommandPalette({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const filteredResults = COMMANDS.filter(cmd => 
    cmd.title.toLowerCase().includes(query.toLowerCase()) || 
    (cmd.subtitle && cmd.subtitle.toLowerCase().includes(query.toLowerCase())) ||
    cmd.category.toLowerCase().includes(query.toLowerCase())
  );

  // Group results
  const groupedResults = filteredResults.reduce((acc, curr) => {
    if (!acc[curr.category]) acc[curr.category] = [];
    acc[curr.category].push(curr);
    return acc;
  }, {} as Record<string, typeof COMMANDS>);

  const flattenedList = Object.values(groupedResults).flat();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % Math.max(flattenedList.length, 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + flattenedList.length) % Math.max(flattenedList.length, 1));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const selected = flattenedList[selectedIndex];
        if (selected && selected.route) {
          navigate(selected.route);
          onClose();
        } else if (selected) {
          // Handle command
          onClose();
        }
      } else if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, flattenedList, navigate, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-start justify-center pt-[10vh] px-4 animate-in fade-in duration-200">
      
      {/* Overlay */}
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose}></div>
      
      {/* Modal */}
      <div className="relative w-full max-w-[900px] bg-[#FBFDFB] rounded-2xl shadow-2xl overflow-hidden flex flex-col border border-slate-200 animate-in zoom-in-95 duration-200">
        
        {/* Header / Input */}
        <div className="flex items-center px-4 py-3 border-b border-slate-100 bg-white">
          <Search className="w-5 h-5 text-emerald-500 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="Search papers, projects, notes, commands, or ask anything..."
            className="flex-1 bg-transparent border-none outline-none text-slate-800 text-sm md:text-base px-4 py-2 placeholder:text-slate-400 font-medium"
          />
          <div className="flex items-center gap-2 shrink-0">
            <kbd className="hidden md:inline-flex items-center gap-1 px-2 py-1 bg-slate-50 border border-slate-200 rounded text-[10px] font-mono font-bold text-slate-500 shadow-sm">
              ESC <span className="font-sans">to close</span>
            </kbd>
            <button onClick={onClose} className="p-2 text-slate-400 hover:bg-slate-100 rounded-lg transition-colors md:hidden">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-2 px-4 py-2 border-b border-slate-100 bg-slate-50 overflow-x-auto scrollbar-hide">
          {['All', 'Pages', 'Papers', 'Projects', 'Commands'].map((tab, i) => (
            <button key={tab} className={cn("px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-widest whitespace-nowrap transition-colors", i === 0 ? "bg-white border border-slate-200 text-slate-800 shadow-sm" : "text-slate-500 hover:bg-slate-200")}>
              {tab}
            </button>
          ))}
        </div>

        {/* Results */}
        <div className="max-h-[60vh] overflow-y-auto p-2 scrollbar-hide">
          {flattenedList.length === 0 ? (
            <div className="py-14 text-center">
              <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-5 h-5 text-slate-400" />
              </div>
              <p className="text-sm font-bold text-slate-700">No results found.</p>
              <p className="text-xs text-slate-500 font-medium mt-1 mb-6">Try searching for papers, projects, or commands.</p>
              <div className="flex items-center justify-center gap-2">
                <button className="px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-lg text-xs font-bold transition-colors hover:bg-emerald-100">Search Papers</button>
                <button className="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-lg text-xs font-bold transition-colors hover:bg-slate-200">Search Projects</button>
              </div>
            </div>
          ) : (
            <div className="space-y-4 p-2">
              {Object.entries(groupedResults).map(([category, items]) => (
                <div key={category}>
                  <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 mb-2">{category}</h4>
                  <div className="space-y-1">
                    {items.map((item) => {
                      const globalIndex = flattenedList.indexOf(item);
                      const isSelected = globalIndex === selectedIndex;
                      
                      return (
                        <div 
                          key={item.id}
                          className={cn(
                            "flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-colors group",
                            isSelected ? "bg-emerald-50" : "hover:bg-slate-50"
                          )}
                          onMouseEnter={() => setSelectedIndex(globalIndex)}
                          onClick={() => {
                            if (item.route) {
                              navigate(item.route);
                              onClose();
                            } else {
                              onClose();
                            }
                          }}
                        >
                          <div className={cn("w-8 h-8 rounded-lg flex items-center justify-center shrink-0 shadow-sm transition-colors", isSelected ? "bg-emerald-500 text-white" : "bg-white border border-slate-200 text-slate-500 group-hover:text-emerald-600 group-hover:border-emerald-300")}>
                            <item.icon className="w-4 h-4" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <h5 className={cn("text-xs font-bold truncate transition-colors", isSelected ? "text-emerald-900" : "text-slate-800")}>{item.title}</h5>
                            {item.subtitle && <p className={cn("text-[10px] font-semibold truncate mt-0.5", isSelected ? "text-emerald-600" : "text-slate-400")}>{item.subtitle}</p>}
                          </div>
                          
                          <div className="hidden sm:flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button className="text-[10px] font-bold text-emerald-600 bg-emerald-100 hover:bg-emerald-200 px-2 py-1 rounded transition-colors">
                              Open
                            </button>
                          </div>
                          {isSelected && (
                            <div className="hidden md:flex items-center gap-1 text-[10px] font-bold text-emerald-600 shrink-0 ml-4">
                              <CornerDownLeft className="w-3.5 h-3.5" /> Enter
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-slate-100 bg-slate-50 flex items-center justify-between text-[10px] font-bold text-slate-500 uppercase tracking-widest hidden md:flex">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5"><kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded shadow-sm">↑↓</kbd> to navigate</span>
            <span className="flex items-center gap-1.5"><kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded shadow-sm">Enter</kbd> to select</span>
            <span className="flex items-center gap-1.5"><kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded shadow-sm">Esc</kbd> to close</span>
          </div>
          <div>ResearchNexus AI Command Palette</div>
        </div>
      </div>
    </div>
  );
}
