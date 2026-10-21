import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopNavigation from './TopNavigation';
import CommandPalette from '../components/CommandPalette';
import ToastContainer from '../components/ToastContainer';
import { useState, useEffect } from 'react';
import { cn } from '../utils/cn';

export default function AppLayout() {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="flex h-screen w-full bg-[var(--bg-main)] overflow-hidden text-[var(--text-main)] font-sans antialiased text-[13px] leading-relaxed transition-colors duration-200">
      <Sidebar isCollapsed={isSidebarCollapsed} toggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)} />
      <div className={cn("flex flex-col flex-1 min-w-0 h-full relative transition-all duration-300", isSidebarCollapsed ? "md:pl-[72px]" : "md:pl-64")}>
        <TopNavigation openCommandPalette={() => setIsCommandPaletteOpen(true)} />
        <main className="flex-1 flex flex-col w-full h-full min-w-0 overflow-hidden relative bg-[var(--bg-surface)] transition-colors duration-200">
          <Outlet />
        </main>
      </div>
      <CommandPalette isOpen={isCommandPaletteOpen} onClose={() => setIsCommandPaletteOpen(false)} />
      <ToastContainer />
    </div>
  );
}
