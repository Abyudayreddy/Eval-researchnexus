import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import { 
  Search, Brain, Stethoscope, 
  LineChart, Globe, Rocket, Zap,
  Database,
  ArrowRight,
  TrendingUp,
  BookOpen
} from 'lucide-react';

import { cn } from '../utils/cn';
import { useState, useEffect } from 'react';

const domains = [
  { id: 'artificial-intelligence', name: 'Artificial Intelligence', desc: 'LLMs, Neural Networks, Reinforcement Learning', trending: 'Agentic Architectures', update: 'Not yet opened', icon: Brain, color: 'text-purple-600', bg: 'bg-purple-50', hover: 'group-hover:bg-purple-50', source: 'Online + Offline' },
  { id: 'data-science', name: 'Data Science', desc: 'Analytics, Data Mining, Statistical Modeling', trending: 'Synthetic Data', update: 'Not yet opened', icon: LineChart, color: 'text-indigo-600', bg: 'bg-indigo-50', hover: 'group-hover:bg-indigo-50', source: 'Online' },
  { id: 'healthcare', name: 'Healthcare', desc: 'Medical Imaging, Genomics, Clinical Trials', trending: 'Predictive Diagnostics', update: 'Not yet opened', icon: Stethoscope, color: 'text-teal-600', bg: 'bg-teal-50', hover: 'group-hover:bg-teal-50', source: 'Online' },
  { id: 'materials-science', name: 'Materials Science', desc: 'Nanomaterials, Semiconductors, Polymers', trending: 'Nanotechnology', update: 'Not yet opened', icon: Database, color: 'text-blue-700', bg: 'bg-blue-700/10', hover: 'group-hover:bg-blue-700/10', source: 'Online' }, 
  { id: 'environmental-science', name: 'Environmental Science', desc: 'Climate Change, Ecology, Conservation', trending: 'Carbon Capture', update: 'Not yet opened', icon: Globe, color: 'text-green-800', bg: 'bg-green-50', hover: 'group-hover:bg-green-50', source: 'Online + Offline' }, 
  { id: 'energy', name: 'Energy', desc: 'Renewables, Grid Tech, Nuclear Sciences', trending: 'Solid State Batteries', update: 'Not yet opened', icon: Zap, color: 'text-amber-600', bg: 'bg-amber-50', hover: 'group-hover:bg-amber-50', source: 'Online' },
  { id: 'space-science', name: 'Space Science', desc: 'Astrophysics, Orbital Mechanics, Exoplanets', trending: 'Mars Colonization', update: 'Not yet opened', icon: Rocket, color: 'text-violet-900', bg: 'bg-violet-50', hover: 'group-hover:bg-violet-50', source: 'Online' }, 
  { id: 'interdisciplinary', name: 'Interdisciplinary Research', desc: 'Bioinformatics, Econophysics, Cybernetics', trending: 'Neuro-Symbolic AI', update: 'Not yet opened', icon: Database, color: 'text-slate-600', bg: 'bg-slate-100', hover: 'group-hover:bg-slate-100', source: 'Online + Offline' }, 
];

// Counts will be fetched from API
const popularTopics = [
  'Hybrid RAG', 'Vision Transformers', 'Climate Change', 'Medical Imaging', 
  'Nanotechnology', 'Renewable Energy', 'LLMs', 'Explainable AI'
];

export default function ResearchDomainsPage() {
  const navigate = useNavigate();
  const [lastOpenedMap, setLastOpenedMap] = useState<Record<string, string>>({});

  useEffect(() => {
    try {
      const stored = localStorage.getItem('domainLastOpened');
      if (stored) {
        setLastOpenedMap(JSON.parse(stored));
      }
    } catch (e) {
      console.error('Failed to parse domainLastOpened from localStorage', e);
    }
  }, []);

  return (
    <div className="h-full w-full overflow-y-auto overflow-x-hidden p-6 md:p-8 pb-16">
      <div className="space-y-10 animate-in fade-in duration-500 w-full text-main">
      
      {/* Hero Section */}
      <section className="relative rounded-[24px] overflow-hidden p-8 md:p-14 text-white shadow-lg flex flex-col items-center text-center space-y-6 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 border border-slate-800">
        <div className="absolute inset-0 opacity-15 pointer-events-none mix-blend-overlay">
          <svg className="w-full h-full" viewBox="0 0 1000 300" preserveAspectRatio="none">
            <path d="M0 150 C 200 100, 400 200, 600 120 C 800 50, 900 130, 1000 80 L 1000 300 L 0 300 Z" fill="#FFFFFF"/>
          </svg>
        </div>
        
        {/* Subtle glow orb */}
        <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-96 bg-emerald-500/15 rounded-full blur-[100px] pointer-events-none" />

        <div className="relative z-10 max-w-2xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold tracking-wide uppercase">
            <span>Verified Scientific Knowledge Base</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight text-white drop-shadow-sm">
            Research Domains
          </h1>
          <p className="text-slate-200 text-base md:text-lg font-normal max-w-xl mx-auto leading-relaxed">
            Explore curated scientific literature across multiple research disciplines powered by Explainable AI.
          </p>
        </div>

        <div className="relative z-10 w-full max-w-2xl group mt-2">
          <div className="flex items-center gap-3 px-4 py-3.5 rounded-2xl bg-white/10 backdrop-blur-md hover:bg-white/15 border border-white/20 transition-all focus-within:border-emerald-400 focus-within:bg-white/20 w-full shadow-xl">
            <Search className="w-5 h-5 text-slate-300 shrink-0 ml-1 group-focus-within:text-emerald-400 transition-colors" />
            <input
              type="text"
              className="bg-transparent text-white text-base md:text-lg w-full focus:outline-none placeholder:text-slate-400 py-0.5"
              placeholder="Search or filter scientific domains..."
            />
          </div>
        </div>
      </section>

      {/* Domain Statistics */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Domains', value: '8' },
          { label: 'Research Sessions', value: '142' },
          { label: 'Trending Topics', value: '24' },
          { label: 'Recent Publications', value: '56' },
        ].map((stat, i) => (
          <div key={i} className="apple-card p-5 text-center transition-all hover:border-emerald-500/40">
            <span className="block text-3xl font-black text-main mb-1 tracking-tight">{stat.value}</span>
            <span className="block text-[11px] font-bold text-muted uppercase tracking-wider">{stat.label}</span>
          </div>
        ))}
      </section>

      {/* Popular Topics */}
      <section className="space-y-3">
        <h2 className="text-lg font-bold text-main tracking-tight flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-emerald-500" /> Popular Research Topics
        </h2>
        <div className="flex flex-wrap gap-2.5">
          {popularTopics.map((topic, i) => (
            <button 
              key={i} 
              className="px-3.5 py-1.5 rounded-xl bg-card border border-theme hover:border-emerald-500/50 hover:bg-emerald-50/20 text-sub hover:text-main text-xs font-semibold shadow-sm transition-all"
            >
              {topic}
            </button>
          ))}
        </div>
      </section>

      {/* Domain Grid */}
      <section className="space-y-5">
        <div className="flex items-center justify-between">
          <h2 className="text-xl md:text-2xl font-bold text-main tracking-tight">Scientific Disciplines</h2>
          <span className="text-xs text-muted font-medium">{domains.length} Specialized Corpora Available</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
          {domains.map((domain, i) => (
            <div 
              key={i} 
              onClick={() => navigate(`/research-domains/${domain.id}`)}
              className={cn(
                "group apple-card p-5 flex flex-col h-full cursor-pointer hover:border-emerald-500/50 hover:shadow-lg transition-all"
              )}
            >
              <div className="flex items-start justify-between mb-3.5">
                <div className={cn("w-11 h-11 rounded-xl flex items-center justify-center transition-all duration-300 shadow-sm group-hover:scale-105", domain.bg, domain.color)}>
                  <domain.icon className="w-5 h-5" />
                </div>
                <div className="text-right flex flex-col items-end">
                  <div className="flex items-center gap-1.5 bg-surface px-2 py-0.5 rounded-full border border-theme">
                    <div className={cn("w-1.5 h-1.5 rounded-full", domain.source === 'Online + Offline' ? 'bg-emerald-500' : 'bg-blue-500')} />
                    <span className="text-[9px] font-bold text-muted uppercase tracking-wider">{domain.source}</span>
                  </div>
                </div>
              </div>
              
              <h3 className={cn("text-base font-bold text-main mb-1.5 transition-colors group-hover:text-emerald-500")}>
                {domain.name}
              </h3>
              <p className="text-muted text-xs flex-grow mb-3.5 leading-relaxed font-normal">
                {domain.desc}
              </p>
              
              <div className="bg-surface rounded-xl p-2.5 mb-3.5 border border-theme">
                <span className="text-[9px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-widest block mb-0.5">
                  Trending Focus
                </span>
                <span className="text-xs font-semibold text-main truncate block">
                  {domain.trending}
                </span>
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t border-theme">
                <span className="text-[10px] font-medium text-muted uppercase tracking-wider flex items-center gap-1">
                  <BookOpen className="w-3 h-3" /> {lastOpenedMap[domain.id] ? `${formatDistanceToNow(new Date(lastOpenedMap[domain.id]))} ago` : domain.update}
                </span>
                <button className="font-bold text-xs flex items-center gap-1 text-emerald-600 dark:text-emerald-400 group-hover:translate-x-0.5 transition-all">
                  Explore <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Research (Cross-domain) */}
      <section className="space-y-4">
        <h2 className="text-xl md:text-2xl font-bold text-main tracking-tight">Featured Cross-Domain Research</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div className="apple-card p-5 hover:border-emerald-500/40 transition-all cursor-pointer group">
            <div className="flex items-center gap-2 mb-2.5">
              <span className="text-[10px] font-black text-blue-700 dark:text-blue-300 bg-blue-100/80 dark:bg-blue-950/60 border border-blue-300 dark:border-blue-700/60 px-2 py-0.5 rounded-md uppercase tracking-wider">Data Science</span>
              <span className="text-[10px] font-black text-emerald-700 dark:text-emerald-300 bg-emerald-100/80 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-700/60 px-2 py-0.5 rounded-md uppercase tracking-wider">Healthcare</span>
            </div>
            <h3 className="text-base font-bold text-main mb-1.5 group-hover:text-emerald-500 transition-colors">Predicting Patient Outcomes via Federated Learning Models</h3>
            <p className="text-xs text-muted font-medium">Chen et al. • Nature Medicine 2024</p>
          </div>
          <div className="apple-card p-5 hover:border-emerald-500/40 transition-all cursor-pointer group">
            <div className="flex items-center gap-2 mb-2.5">
              <span className="text-[10px] font-black text-indigo-700 dark:text-indigo-300 bg-indigo-100/80 dark:bg-indigo-950/60 border border-indigo-300 dark:border-indigo-700/60 px-2 py-0.5 rounded-md uppercase tracking-wider">Materials Science</span>
              <span className="text-[10px] font-black text-purple-700 dark:text-purple-300 bg-purple-100/80 dark:bg-purple-950/60 border border-purple-300 dark:border-purple-700/60 px-2 py-0.5 rounded-md uppercase tracking-wider">Artificial Intelligence</span>
            </div>
            <h3 className="text-base font-bold text-main mb-1.5 group-hover:text-emerald-500 transition-colors">AI-Driven Crop Yield Optimization using Satellite Imagery</h3>
            <p className="text-xs text-muted font-medium">Rodriguez et al. • Agricultural Systems 2025</p>
          </div>
        </div>
      </section>
      </div>
    </div>
  );
}
