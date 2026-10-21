import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Brain, 
  Stethoscope, 
  Leaf, 
  LineChart, 
  Globe, 
  Rocket, 
  Zap, 
  Database,
  TrendingUp,
  HardDrive,
  Network,
  Map,
  BookOpen,
  Play,
  FileText,
  Bookmark,
  Search,
  FolderOpen,
  Monitor
} from 'lucide-react';
import { cn } from '../utils/cn';
import { researchDomains } from '../config/researchDomains';
import DomainHeroBackground from '../components/DomainHeroBackgrounds';
import { api } from '../utils/api';
import { useState, useEffect } from 'react';

const IconMap: Record<string, React.ElementType> = {
  Brain, Stethoscope, Leaf, Database, Globe, Rocket, Zap, LineChart
};

type Theme = {
  light: string;
  text: string;
  border: string;
  hover: string;
  gradient: string;
};

const getTheme = (color: string): Theme => {
  const themes: Record<string, Theme> = {
    purple: { light: 'bg-purple-50', text: 'text-purple-600', border: 'border-purple-200', hover: 'hover:border-purple-300 hover:shadow-purple-100', gradient: 'from-purple-600 via-purple-500 to-indigo-600' },
    rose: { light: 'bg-rose-50', text: 'text-rose-600', border: 'border-rose-200', hover: 'hover:border-rose-300 hover:shadow-rose-100', gradient: 'from-rose-600 via-rose-500 to-pink-600' },
    green: { light: 'bg-lime-50', text: 'text-lime-700', border: 'border-lime-200', hover: 'hover:border-lime-300 hover:shadow-lime-100', gradient: 'from-[#808000] via-lime-700 to-green-700' },
    blue: { light: 'bg-blue-50', text: 'text-blue-600', border: 'border-blue-200', hover: 'hover:border-blue-300 hover:shadow-blue-100', gradient: 'from-blue-600 via-blue-500 to-cyan-600' },
    emerald: { light: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', hover: 'hover:border-emerald-300 hover:shadow-emerald-100', gradient: 'from-emerald-700 via-emerald-600 to-teal-700' },
    indigo: { light: 'bg-indigo-50', text: 'text-indigo-600', border: 'border-indigo-200', hover: 'hover:border-indigo-300 hover:shadow-indigo-100', gradient: 'from-indigo-800 via-indigo-600 to-blue-700' },
    amber: { light: 'bg-amber-50', text: 'text-amber-600', border: 'border-amber-200', hover: 'hover:border-amber-300 hover:shadow-amber-100', gradient: 'from-amber-600 via-amber-500 to-orange-500' },
    teal: { light: 'bg-teal-50', text: 'text-teal-700', border: 'border-teal-200', hover: 'hover:border-teal-300 hover:shadow-teal-100', gradient: 'from-teal-700 via-teal-600 to-emerald-800' }
  };
  return themes[color] || themes.purple;
};

const domainCache: Record<string, any> = {};

export default function DomainWorkspacePage() {
  const { domainId } = useParams();
  const navigate = useNavigate();
  const [domainData, setDomainData] = useState<any>(() => (domainId ? domainCache[domainId] || null : null));
  const [isLoading, setIsLoading] = useState(!domainCache[domainId as string]);
  const [error, setError] = useState<string | null>(null);
  const [bookmarkedPapers, setBookmarkedPapers] = useState<string[]>([]);

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    try {
      const data = await api.bookmarks.getAll();
      if (Array.isArray(data)) {
        setBookmarkedPapers(data.map((b: any) => b.paper_id));
      }
    } catch (e) {
      console.error("Failed to load bookmarks", e);
    }
  };

  const handleBookmark = async (e: React.MouseEvent, paper: any) => {
    e.stopPropagation();
    const pid = paper.id || paper.paper_id || paper.doi || paper.title;
    if (bookmarkedPapers.includes(pid)) {
      try {
        await api.bookmarks.remove(pid);
        setBookmarkedPapers(prev => prev.filter(id => id !== pid));
      } catch (err) {
        console.error("Failed to remove bookmark", err);
      }
    } else {
      try {
        await api.bookmarks.add({
          id: pid,
          title: paper.title || "Untitled Paper",
          authors: typeof paper.authors === 'string' ? paper.authors : (Array.isArray(paper.authors) ? paper.authors.join(', ') : "Unknown Authors"),
          abstract: paper.abstract || "",
          url: paper.url || "",
          published: paper.publication_date || null,
          domain: domainId
        });
        setBookmarkedPapers(prev => [...prev, pid]);
      } catch (err) {
        console.error("Failed to save bookmark", err);
      }
    }
  };

  useEffect(() => {
    if (!domainId) return;

    // Use cached data immediately if available, while refreshing asynchronously
    if (domainCache[domainId]) {
      setDomainData(domainCache[domainId]);
      setIsLoading(false);
    } else {
      setIsLoading(true);
    }

    const fetchDomainInfo = async () => {
      try {
        const data = await api.papers.getDomainPapers(domainId);
        domainCache[domainId] = data;
        setDomainData(data);
      } catch (err) {
        console.error("Failed to load domain papers", err);
        setError("Failed to load papers from the online repository. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchDomainInfo();

    // Track last opened timestamp for this domain
    const lastOpenedMap = JSON.parse(localStorage.getItem('domainLastOpened') || '{}');
    lastOpenedMap[domainId] = new Date().toISOString();
    localStorage.setItem('domainLastOpened', JSON.stringify(lastOpenedMap));
  }, [domainId]);

  const domain = researchDomains[domainId as string];
  
  if (!domain) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500">
        <h2 className="text-xl font-bold mb-2">Domain Not Found</h2>
        <button onClick={() => navigate('/research-domains')} className="text-emerald-600 hover:underline">Return to Domains</button>
      </div>
    );
  }

  const Icon = IconMap[domain.icon] || Brain;
  const theme = getTheme(domain.color);
  const realPapers = domainData?.papers || [];

  return (
    <div className="h-full w-full overflow-y-auto overflow-x-hidden pr-2">
      <div className="space-y-12 animate-in fade-in duration-500 pb-16 w-full max-w-[1400px] mx-auto text-slate-800">
      
      {/* Navigation */}
      <button 
        onClick={() => navigate('/research-domains')}
        className="flex items-center gap-2 text-slate-500 hover:text-slate-900 font-bold text-xs transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Research Domains
      </button>

      {/* 1. Hero Section & Domain Overview */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className={cn("relative rounded-[32px] overflow-hidden p-8 md:p-12 lg:p-16 text-white shadow-xl bg-gradient-to-br", domain.heroGradient || theme.gradient)}
      >
        
        {/* Animated Background Layers */}
        <DomainHeroBackground domainId={domain.id} />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-start justify-between gap-8 h-full">
          <div className="max-w-2xl space-y-6 flex-1">
            <div className="flex items-center gap-3">
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-full border border-white/30 text-xs font-bold uppercase tracking-widest shadow-sm"
              >
                <Icon className="w-4 h-4" /> Domain Workspace
              </motion.div>
              <div className="inline-flex items-center gap-1.5 bg-black/30 backdrop-blur-md px-3 py-1.5 rounded-full border border-white/20 text-xs font-bold text-white shadow-sm">
                <div className={cn("w-2 h-2 rounded-full", domain.sourceBadge === 'Online + Offline' ? 'bg-emerald-400' : 'bg-blue-400')} />
                <span>{domain.sourceBadge}</span>
              </div>
            </div>
            
            <motion.h1 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-4xl md:text-5xl lg:text-6xl font-black tracking-tight leading-tight"
            >
              {domain.title}
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-white/90 text-base md:text-lg font-medium max-w-xl leading-relaxed"
            >
              {domain.description}
            </motion.p>

            {/* Metrics */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="flex flex-wrap gap-4 pt-2"
            >
              {domain.heroMetrics?.filter((metric: any) => metric.label !== 'Papers').map((metric: { label: string; value: string }, i: number) => (
                <div key={i} className="flex flex-col">
                  <span className="text-[10px] font-bold text-white/60 uppercase tracking-widest">{metric.label}</span>
                  <span className="text-sm font-bold text-white">{metric.value}</span>
                </div>
              ))}
            </motion.div>
            
            {/* Quick Actions (Search Within Domain) */}
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="pt-6 w-full"
            >
              <div className="relative max-w-xl group">
                <Search className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-white/70 group-focus-within:text-white transition-colors" />
                <input 
                  type="text" 
                  autoFocus
                  placeholder={domain.searchPlaceholder || `Search within ${domain.title}...`}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      navigate('/hybrid-search', { state: { query: e.currentTarget.value, domain: domain.id } });
                    }
                  }}
                  className="w-full bg-white/10 hover:bg-white/15 border border-white/20 text-white placeholder:text-white/60 rounded-2xl px-12 py-4 focus:outline-none focus:ring-2 focus:ring-white/50 backdrop-blur-md transition-all shadow-lg"
                />
              </div>
              
              {/* Suggested Searches */}
              <div className="flex flex-wrap gap-2 mt-4">
                {domain.suggestedSearches?.map((suggestion: string, i: number) => (
                  <button 
                    key={i}
                    onClick={() => navigate('/hybrid-search', { state: { query: suggestion, domain: domain.id } })}
                    className="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 border border-white/10 text-white text-[11px] font-bold shadow-sm transition-all backdrop-blur-sm"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* 9. Quick Actions */}
      <section className="flex flex-wrap gap-4">
        <button onClick={() => navigate('/research')} className="px-6 py-3 bg-slate-900 text-white rounded-xl font-bold text-sm shadow-md hover:bg-slate-800 transition-colors flex items-center gap-2">
          <Play className="w-4 h-4 fill-current" /> Start Research
        </button>
        <button className="px-6 py-3 bg-white text-slate-700 border border-slate-200 rounded-xl font-bold text-sm shadow-sm hover:bg-slate-50 transition-colors flex items-center gap-2">
          <BookOpen className="w-4 h-4" /> Browse Papers
        </button>
        <button className="px-6 py-3 bg-white text-slate-700 border border-slate-200 rounded-xl font-bold text-sm shadow-sm hover:bg-slate-50 transition-colors flex items-center gap-2">
          <FolderOpen className="w-4 h-4" /> View Projects
        </button>
        <button onClick={() => navigate('/research')} className="px-6 py-3 bg-white text-slate-700 border border-slate-200 rounded-xl font-bold text-sm shadow-sm hover:bg-slate-50 transition-colors flex items-center gap-2">
          <Monitor className="w-4 h-4" /> Open Workspace
        </button>
      </section>

      {/* 8. Statistics */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {domain.statistics && domain.statistics.filter((stat: any) => stat.label !== 'Total Papers').length > 0 ? (
          domain.statistics.filter((stat: any) => stat.label !== 'Total Papers').map((stat, i) => (
            <div key={i} className={cn("apple-card p-5 text-center transition-all", theme.hover)}>
              <span className={cn("block text-2xl font-black mb-1", theme.text)}>{stat.value}</span>
              <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-widest">{stat.label}</span>
            </div>
          ))
        ) : (
          <div className="col-span-full apple-card p-8 flex flex-col items-center justify-center text-slate-400">
            <LineChart className="w-8 h-8 mb-3 opacity-50" />
            <p className="text-sm font-bold uppercase tracking-widest">No statistics configured.</p>
          </div>
        )}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Main Column */}
        <div className="lg:col-span-8 space-y-10">
          
          {/* 3. Research Subdomains */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <Network className={cn("w-5 h-5", theme.text)} />
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Research Subdomains</h2>
            </div>
            
            {domain.subdomains && domain.subdomains.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {domain.subdomains.map((sub: any, i: number) => (
                  <button 
                    key={i} 
                    onClick={() => navigate('/hybrid-search', { state: { query: sub.name, domain: domain.id } })}
                    className={cn("apple-card p-5 transition-all border-l-4 text-left hover:shadow-md", theme.hover)} 
                    style={{ borderLeftColor: `var(--color-${domain.color}-500, currentColor)` }}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-slate-800 text-sm">{sub.name}</h3>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <div className="apple-card p-12 flex flex-col items-center justify-center text-slate-400">
                <Network className="w-8 h-8 mb-3 opacity-50" />
                <p className="text-sm font-bold uppercase tracking-widest">No subdomains configured.</p>
              </div>
            )}
          </section>

          {/* 4. Featured Papers */}
          <section className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileText className={cn("w-5 h-5", theme.text)} />
                <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Featured Papers</h2>
              </div>
            </div>
            
            {isLoading && realPapers.length === 0 ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="apple-card p-6 flex flex-col gap-3 animate-pulse">
                    <div className="h-4 bg-slate-200 rounded w-1/4"></div>
                    <div className="h-6 bg-slate-200 rounded w-3/4"></div>
                    <div className="h-4 bg-slate-100 rounded w-1/2"></div>
                    <div className="h-10 bg-slate-50 rounded w-full"></div>
                  </div>
                ))}
              </div>
            ) : realPapers.length > 0 ? (
              <div className="space-y-4">
                {error && (
                  <div className="bg-rose-50 text-rose-600 border border-rose-200 p-4 rounded-xl text-sm font-bold text-center">
                    {error}
                  </div>
                )}
                {realPapers.map((paper: any, i: number) => (
                  <div key={i} className={cn("apple-card p-6 flex flex-col sm:flex-row justify-between gap-4 transition-all", theme.hover)}>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                         <span className="text-[10px] font-bold bg-slate-100 text-slate-500 px-2 py-0.5 rounded-md uppercase tracking-widest">{paper.source || 'Repository'}</span>
                      </div>
                      <a href={paper.url} target="_blank" rel="noreferrer" className={cn("block text-lg font-bold text-slate-800 mb-2 leading-tight transition-colors line-clamp-2", `hover:${theme.text}`)}>
                        {paper.title}
                      </a>
                      <div className="flex flex-wrap items-center gap-2 text-xs font-medium text-slate-500 mb-2">
                        <span className="truncate max-w-[200px] sm:max-w-xs">{paper.authors || "Unknown Authors"}</span>
                        <span>•</span>
                        <span>{paper.publication_date || "Unknown Date"}</span>
                      </div>
                      <p className="text-slate-500 text-xs line-clamp-2 leading-relaxed">
                        {paper.abstract || "No abstract available."}
                      </p>
                    </div>
                    <div className="flex sm:flex-col items-center sm:items-end justify-between gap-2 shrink-0">
                      <button 
                        onClick={(e) => handleBookmark(e, paper)}
                        className={cn("p-2 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors", bookmarkedPapers.includes(paper.id || paper.paper_id || paper.doi || paper.title) ? "text-amber-500 bg-amber-50" : "text-slate-400", `hover:${theme.text}`)}
                        title="Bookmark paper"
                      >
                        <Bookmark className="w-4 h-4" fill={bookmarkedPapers.includes(paper.id || paper.paper_id || paper.doi || paper.title) ? "currentColor" : "none"} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="apple-card p-12 flex flex-col items-center justify-center text-slate-400">
                <FileText className="w-8 h-8 mb-3 opacity-50" />
                <p className="text-sm font-bold uppercase tracking-widest">No papers found for this domain.</p>
              </div>
            )}
          </section>

          {/* 7. Recommended Learning Path */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <Map className={cn("w-5 h-5", theme.text)} />
              <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Recommended Learning Path</h2>
            </div>
            
            {domain.learningPath && domain.learningPath.length > 0 ? (
              <div className="apple-card p-6">
                <div className="relative border-l-2 border-slate-100 ml-3 space-y-8 py-2">
                  {domain.learningPath.map((item: any, i: number) => (
                    <div key={i} className="relative pl-8">
                      <div className={cn("absolute w-6 h-6 rounded-full -left-[13px] top-0 shadow-sm flex items-center justify-center text-[10px] font-bold text-white", theme.gradient)}>
                        {i + 1}
                      </div>
                      <div className="flex flex-col">
                        <span className={cn("text-[10px] font-bold uppercase tracking-widest mb-1", theme.text)}>{item.step ?? i + 1}</span>
                        <span className="text-base font-bold text-slate-800">{item.title}</span>
                        <span className="text-xs font-medium text-slate-500 mt-1">{item.desc}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="apple-card p-12 flex flex-col items-center justify-center text-slate-400">
                <Map className="w-8 h-8 mb-3 opacity-50" />
                <p className="text-sm font-bold uppercase tracking-widest">No learning path configured.</p>
              </div>
            )}
          </section>

        </div>

        {/* Side Column */}
        <div className="lg:col-span-4 space-y-10">
          
          {/* 5. Research Topics */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <TrendingUp className={cn("w-5 h-5", theme.text)} />
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Research Topics</h2>
            </div>
            
            {domain.topics && domain.topics.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {domain.topics.map((topic: any, i: number) => {
                  const topicName = typeof topic === 'string' ? topic : topic?.name;
                  return (
                    <button 
                      key={i} 
                      onClick={() => navigate('/hybrid-search', { state: { query: topicName, domain: domain.id } })}
                      className={cn("px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-600 text-xs font-bold shadow-sm transition-all apple-shadow", theme.hover, `hover:${theme.text}`)}
                    >
                      {topicName}
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="apple-card p-8 flex flex-col items-center justify-center text-slate-400">
                <TrendingUp className="w-6 h-6 mb-2 opacity-50" />
                <p className="text-[10px] font-bold uppercase tracking-widest">No topics configured.</p>
              </div>
            )}
          </section>

          {/* 6. Datasets */}
          <section className="space-y-6">
            <div className="flex items-center gap-2">
              <HardDrive className={cn("w-5 h-5", theme.text)} />
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Datasets</h2>
            </div>
            
            {domain.datasets && domain.datasets.length > 0 ? (
              <div className="apple-card p-2 divide-y divide-slate-50">
                {domain.datasets.map((dataset: any, i: number) => (
                  <div key={i} className={cn("p-4 transition-colors rounded-xl cursor-pointer flex justify-between items-center group", theme.light)}>
                    <h4 className="font-bold text-slate-800 text-sm group-hover:text-slate-900">{typeof dataset === 'string' ? dataset : dataset?.name}</h4>
                  </div>
                ))}
              </div>
            ) : (
              <div className="apple-card p-8 flex flex-col items-center justify-center text-slate-400">
                <HardDrive className="w-6 h-6 mb-2 opacity-50" />
                <p className="text-[10px] font-bold uppercase tracking-widest">No datasets configured.</p>
              </div>
            )}
          </section>

        </div>
        </div>
      </div>
    </div>
  );
}
