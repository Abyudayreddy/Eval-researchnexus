import React from 'react';
import { cn } from '../../utils/cn';

interface WorkspaceLayoutProps {
  leftPanel?: React.ReactNode;
  mainContent: React.ReactNode;
  rightPanel?: React.ReactNode;
  className?: string;
  leftPanelClassName?: string;
  mainContentClassName?: string;
  rightPanelClassName?: string;
}

/**
 * A highly reusable 3-column workspace layout strictly designed to match the 
 * "Scientific Research OS" reference structure.
 * Features independent scrolling areas and no nested overflow traps.
 */
export default function WorkspaceLayout({
  leftPanel,
  mainContent,
  rightPanel,
  className,
  leftPanelClassName,
  mainContentClassName,
  rightPanelClassName
}: WorkspaceLayoutProps) {
  // We use CSS Grid.
  // Full 3 columns: 260px | 1fr | 340px
  // 2 columns (no right): 260px | 1fr
  // 2 columns (no left): 1fr | 340px
  
  let gridClass = "grid-cols-1";
  if (leftPanel && rightPanel) {
    gridClass = "lg:grid-cols-[240px_1fr_300px] xl:grid-cols-[260px_1fr_340px]";
  } else if (leftPanel && !rightPanel) {
    gridClass = "lg:grid-cols-[240px_1fr] xl:grid-cols-[260px_1fr]";
  } else if (!leftPanel && rightPanel) {
    gridClass = "lg:grid-cols-[1fr_300px] xl:grid-cols-[1fr_340px]";
  }

  return (
    <div className={cn("flex-1 min-h-0 max-w-[1400px] w-full mx-auto px-4 md:px-6 py-6 overflow-hidden", className)}>
      <div className={cn("grid gap-6 h-full", gridClass)}>
        
        {leftPanel && (
          <div className={cn(
            "flex flex-col h-full bg-white rounded-2xl border border-slate-200 shadow-sm p-5 overflow-y-auto scrollbar-hide", 
            leftPanelClassName
          )}>
            {leftPanel}
          </div>
        )}

        <div className={cn(
          "flex flex-col h-full bg-slate-50/50 rounded-2xl border border-slate-200 shadow-inner overflow-y-auto scrollbar-hide p-4 md:p-6", 
          mainContentClassName
        )}>
          {mainContent}
        </div>

        {rightPanel && (
          <div className={cn(
            "flex flex-col h-full bg-white rounded-2xl border border-slate-200 shadow-sm p-5 overflow-y-auto scrollbar-hide relative", 
            rightPanelClassName
          )}>
            {rightPanel}
          </div>
        )}

      </div>
    </div>
  );
}
