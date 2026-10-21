import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, PenTool, FolderPlus, MessageSquare, Maximize, ExternalLink, HelpCircle, FileText } from 'lucide-react';
import { cn } from '../../utils/cn';

interface PaperCardProps {
  paper: any;
  searchId: string;
  isSelectedForAi: boolean;
  isBookmarked: boolean;
  onToggleSelection: (e: React.MouseEvent, paperId: string) => void;
  onBookmark: (e: React.MouseEvent, paper: any) => void;
  onNote: (e: React.MouseEvent, paperId: string) => void;
  onProject: (e: React.MouseEvent, paperId: string) => void;
  onAskAi: (e: React.MouseEvent, paperId: string) => void;
  onExplain: (e: React.MouseEvent, paperId: string) => void;
}

export default function PaperCard({
  paper,
  searchId,
  isSelectedForAi,
  isBookmarked,
  onToggleSelection,
  onBookmark,
  onNote,
  onProject,
  onAskAi,
  onExplain
}: PaperCardProps) {
  const navigate = useNavigate();
  const isLocal = paper.retrieval_source === 'local';
  const isOnline = paper.retrieval_source === 'online';
  const isMixed = paper.retrieval_source === 'mixed';

  const badgeClass = cn(
    "text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-widest",
    isLocal && "bg-emerald-100 text-emerald-800",
    isOnline && "bg-blue-100 text-blue-800",
    isMixed && "bg-violet-100 text-violet-800"
  );

  const badgeText = isLocal ? "LOCAL" : isOnline ? "ONLINE" : "MIXED";
  
  const authors = Array.isArray(paper.authors) 
    ? paper.authors.join(', ') 
    : (paper.authors || "Authors unavailable");

  const publicationInfo = [
    paper.publication_year || (paper.publication_date && paper.publication_date.substring(0,4)) || paper.year,
    paper.journal || paper.conference || paper.source_repository || paper.venue,
    paper.doi
  ].filter(Boolean).join(' • ');

  // Evidence preview for local results
  const evidenceSnippet = paper.evidence_text;

  // Handle open paper action based on source
  const handleOpenPaper = (e: React.MouseEvent) => {
    e.stopPropagation();
    const pid = paper.id || paper.paper_id;
    
    // MIXED logic: Prefer local if it has a local PDF representation, else online URL
    if (isMixed) {
      if (paper.read_source === 'local_pdf' || paper.pdf_path) {
        navigate(`/read?paper_id=${pid}&search_id=${searchId}`);
      } else if (paper.url || paper.paper_url) {
        window.open(paper.paper_url || paper.url, '_blank');
      }
    } else if (isLocal) {
      navigate(`/read?paper_id=${pid}&search_id=${searchId}`);
    } else if (isOnline) {
      if (paper.url || paper.paper_url) {
        window.open(paper.paper_url || paper.url, '_blank');
      }
    }
  };

  const hasLocal = paper.read_source === 'local_pdf' || paper.pdf_path || isLocal;
  const hasOnline = paper.url || paper.paper_url;
  const canOpen = (isMixed && (hasLocal || hasOnline)) || (isLocal && hasLocal) || (isOnline && hasOnline);

  return (
    <div 
      className={cn(
        "group relative bg-[var(--bg-card)] rounded-xl p-5 mb-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg cursor-pointer overflow-hidden border-y border-r border-[var(--border-color)]",
        isLocal ? "border-l-4 border-l-emerald-500" : isOnline ? "border-l-4 border-l-blue-500" : "border-l-4 border-l-violet-500",
        isSelectedForAi ? "border-[var(--accent-primary)] ring-2 ring-[var(--accent-soft)] shadow-md" : "hover:border-[var(--accent-primary)]"
      )}
      onClick={(e) => onToggleSelection(e, paper.id || paper.paper_id)}
    >
      {/* Header / Provenance */}
      <div className="flex items-center justify-between mb-2">
        <span className={badgeClass}>{badgeText}</span>
        
        {/* Quick action icons visible on hover for desktop, always for mobile accessibility */}
        <div className="flex items-center gap-1 opacity-100 md:opacity-0 group-hover:opacity-100 transition-opacity">
           <button onClick={(e) => { e.stopPropagation(); onBookmark(e, paper); }} className="p-1.5 text-[var(--text-muted)] hover:text-amber-500 rounded">
             <Bookmark className="w-4 h-4" fill={isBookmarked ? "currentColor" : "none"} />
           </button>
        </div>
      </div>

      <h3 className="text-lg font-bold text-[var(--text-main)] leading-snug mb-1">{paper.title}</h3>
      <p className="text-sm font-medium text-[var(--text-muted)] mb-2">{authors}</p>
      
      {publicationInfo && (
        <p className="text-xs font-bold text-[var(--text-muted)] mb-4">{publicationInfo}</p>
      )}

      {/* Abstract preview if no evidence snippet */}
      {!evidenceSnippet && (
        <p className="text-sm text-[var(--text-sub)] line-clamp-3 mb-4 leading-relaxed font-serif">
          {paper.abstract || "No abstract available."}
        </p>
      )}

      {/* Evidence snippet */}
      {evidenceSnippet && (
        <div className="mb-4 bg-[var(--evidence-bg,#151A17)] border border-[var(--evidence-border,rgba(139,226,139,0.28))] p-3 rounded-lg relative shadow-xs">
          <div className="text-[10px] font-bold text-[var(--evidence-label,#8BE28B)] uppercase tracking-widest mb-1 flex items-center gap-1">
            <FileText className="w-3 h-3 text-[var(--evidence-label,#8BE28B)]" /> Retrieved Evidence
          </div>
          <p className="text-sm text-[var(--evidence-text,#D7DED9)] italic font-serif leading-relaxed line-clamp-4">
            "...{evidenceSnippet}..."
          </p>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-wrap items-center gap-2 mt-4 pt-4 border-t border-[var(--border-subtle)]">
        <button 
          onClick={handleOpenPaper}
          disabled={!canOpen}
          className={cn("px-3 py-1.5 text-xs font-bold rounded-lg flex items-center gap-1.5 transition-colors shadow-xs cursor-pointer",
            canOpen 
              ? "bg-[var(--bg-surface)] hover:bg-[var(--bg-card-hover)] text-[var(--text-main)] border border-[var(--border-color)] hover:border-[var(--accent-primary)]" 
              : "bg-[var(--bg-surface)] text-[var(--text-muted)] cursor-not-allowed border border-[var(--border-subtle)]"
          )}
        >
          {canOpen ? <Maximize className="w-3.5 h-3.5 text-[var(--accent-primary)]" /> : <ExternalLink className="w-3.5 h-3.5" />}
          Open Paper
        </button>
        
        <button 
          onClick={(e) => onAskAi(e, paper.id || paper.paper_id)}
          className="px-3 py-1.5 text-xs font-bold bg-[var(--ask-ai-bg,rgba(139,121,168,0.14))] text-[var(--ask-ai-text,#D9CCEA)] hover:bg-[var(--ask-ai-hover,rgba(139,121,168,0.22))] border border-[var(--ask-ai-border,rgba(169,151,194,0.35))] rounded-lg flex items-center gap-1.5 transition-colors shadow-xs cursor-pointer"
        >
          <MessageSquare className="w-3.5 h-3.5 text-[var(--ask-ai-icon,#B9A6D4)]" /> Ask AI
        </button>

        <button 
          onClick={(e) => onExplain(e, paper.id || paper.paper_id)}
          className="px-3 py-1.5 text-xs font-bold bg-[var(--bg-card)] text-[var(--text-sub)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card-hover)] border border-[var(--border-color)] rounded-lg flex items-center gap-1.5 transition-colors shadow-xs cursor-pointer"
        >
          <HelpCircle className="w-3.5 h-3.5 text-[var(--accent-primary)]" /> Explain
        </button>

        <div className="flex-1" />

        <button onClick={(e) => onNote(e, paper.id || paper.paper_id)} className="px-2.5 py-1.5 text-xs font-bold text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card-hover)] border border-transparent hover:border-[var(--border-color)] rounded-lg transition-colors flex items-center gap-1.5 cursor-pointer">
          <PenTool className="w-3.5 h-3.5 text-[var(--accent-secondary)]" /> <span className="hidden sm:inline">Note</span>
        </button>
        <button onClick={(e) => onProject(e, paper.id || paper.paper_id)} className="px-2.5 py-1.5 text-xs font-bold text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card-hover)] border border-transparent hover:border-[var(--border-color)] rounded-lg transition-colors flex items-center gap-1.5 cursor-pointer">
          <FolderPlus className="w-3.5 h-3.5 text-[var(--info)]" /> <span className="hidden sm:inline">Project</span>
        </button>
      </div>
    </div>
  );
}
