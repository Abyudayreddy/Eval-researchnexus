import { 
  Search, 
  Brain, 
  Stethoscope, 
  LineChart, 
  Globe, 
  Rocket, 
  Zap, 
  Database,
  BookOpen,
  Clock,
  Briefcase,
  Bookmark,
  MoreVertical,
  Plus,
  Play,
  Lightbulb,
  Bot,
  Edit3,
  Trash2
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { cn } from '../utils/cn';
import { formatDistanceToNow } from 'date-fns';
import { api } from '../utils/api';
import { useToastStore } from '../store/toastStore';
import { getDynamicResearchTopics, DynamicResearchTopic } from '../services/researchTopicService';

// Data definitions

const domains = [
  { id: 'artificial-intelligence', name: 'Artificial Intelligence', desc: 'LLMs, Neural Networks, Reinforcement Learning', trending: 'Agentic Architectures', icon: Brain, color: 'text-emerald-600', bg: 'bg-emerald-50', hover: 'group-hover:bg-emerald-50', source: 'Online + Offline' },
  { id: 'data-science', name: 'Data Science', desc: 'Analytics, Data Mining, Statistical Modeling', trending: 'Synthetic Data', icon: LineChart, color: 'text-blue-600', bg: 'bg-blue-50', hover: 'group-hover:bg-blue-50', source: 'Online' },
  { id: 'healthcare', name: 'Healthcare', desc: 'Medical Imaging, Genomics, Clinical Trials', trending: 'Predictive Diagnostics', icon: Stethoscope, color: 'text-rose-600', bg: 'bg-rose-50', hover: 'group-hover:bg-rose-50', source: 'Online' },
  { id: 'materials-science', name: 'Materials Science', desc: 'Nanomaterials, Semiconductors, Polymers', trending: 'Nanotechnology', icon: Database, color: 'text-blue-600', bg: 'bg-blue-50', hover: 'group-hover:bg-blue-50', source: 'Online' },
  { id: 'environmental-science', name: 'Environmental Science', desc: 'Climate Change, Ecology, Conservation', trending: 'Carbon Capture', icon: Globe, color: 'text-teal-600', bg: 'bg-teal-50', hover: 'group-hover:bg-teal-50', source: 'Online + Offline' },
  { id: 'energy', name: 'Energy', desc: 'Renewables, Grid Tech, Nuclear Sciences', trending: 'Solid State Batteries', icon: Zap, color: 'text-amber-600', bg: 'bg-amber-50', hover: 'group-hover:bg-amber-50', source: 'Online' },
  { id: 'space-science', name: 'Space Science', desc: 'Astrophysics, Orbital Mechanics, Exoplanets', trending: 'Mars Colonization', icon: Rocket, color: 'text-orange-600', bg: 'bg-orange-50', hover: 'group-hover:bg-orange-50', source: 'Online' },
  { id: 'interdisciplinary', name: 'Interdisciplinary', desc: 'Bioinformatics, Econophysics, Cybernetics', trending: 'Neuro-Symbolic AI', icon: Database, color: 'text-purple-600', bg: 'bg-purple-50', hover: 'group-hover:bg-purple-50', source: 'Online + Offline' },
];

export default function DashboardPage() {
  const navigate = useNavigate();
  const [isProjectModalOpen, setIsProjectModalOpen] = useState(false);
  const [dashboardData, setDashboardData] = useState<any>({
    activeProjects: [],
    recentPapers: [],
    continueResearch: [],
    recentTimeline: [],
    stats: []
  });
  const [isLoading, setIsLoading] = useState(true);
  
  // Project Creation/Edit State
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [editingProjectId, setEditingProjectId] = useState<string | null>(null);
  const [activeDropdownProjectId, setActiveDropdownProjectId] = useState<string | null>(null);
  const [dynamicExamples, setDynamicExamples] = useState<DynamicResearchTopic[]>([]);
  
  // Toast Popup State
  const { addToast } = useToastStore();

  useEffect(() => {
    getDynamicResearchTopics().then(res => {
      setDynamicExamples(res.tryExamples);
    }).catch(err => {
      console.warn('Failed to load dynamic examples for dashboard', err);
    });
  }, []);

  const fetchDashboard = async () => {
    try {
      const data = await api.dashboard.getStats();
      setDashboardData(data);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
      addToast("Failed to load dashboard data", 'error');
    } finally {
      setIsLoading(false);
    }
  };
  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleOpenCreateModal = () => {
    setEditingProjectId(null);
    setNewProjectName('');
    setNewProjectDesc('');
    setIsProjectModalOpen(true);
  };

  const handleOpenEditModal = (e: React.MouseEvent, project: any) => {
    e.stopPropagation();
    setEditingProjectId(project.id);
    setNewProjectName(project.name);
    setNewProjectDesc(project.description || '');
    setActiveDropdownProjectId(null);
    setIsProjectModalOpen(true);
  };

  const handleCreateOrEditProject = async () => {
    if (!newProjectName.trim()) {
      addToast("Project name is required", 'error');
      return;
    }
    setIsCreating(true);
    try {
      if (editingProjectId) {
        await api.projects.update(editingProjectId, { name: newProjectName, description: newProjectDesc });
        addToast("Project updated successfully!", 'success');
      } else {
        await api.projects.create({ name: newProjectName, description: newProjectDesc });
        addToast("Project created successfully!", 'success');
      }
      setIsProjectModalOpen(false);
      setNewProjectName('');
      setNewProjectDesc('');
      setEditingProjectId(null);
      await fetchDashboard(); // Refresh stats
    } catch (error) {
      console.error("Failed to save project:", error);
      addToast("Failed to save project", 'error');
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteProject = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    setActiveDropdownProjectId(null);
    if (!window.confirm("Are you sure you want to delete this project? This action cannot be undone.")) return;
    
    try {
      await api.projects.delete(id);
      addToast("Project deleted successfully!", 'success');
      await fetchDashboard();
    } catch (error) {
      console.error("Failed to delete project:", error);
      addToast("Failed to delete project", 'error');
    }
  };

  // Removed fake topicsByDomain logic

  const toggleBookmark = async (e: React.MouseEvent, paper: any) => {
    e.stopPropagation();
    const pid = paper.id || paper.paper_id;
    try {
      await api.bookmarks.remove(pid);
      addToast("Removed from saved papers", "success");
      await fetchDashboard();
    } catch (err) {
      addToast("Failed to update bookmark", "error");
    }
  };

  const fillSearchQuery = (text: string) => {
    navigate('/hybrid-search', { state: { query: text } });
  };

  if (isLoading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
      </div>
    );
  }

  return (
    <div className="h-full w-full overflow-y-auto overflow-x-hidden p-6 md:p-8 pb-16">
      <div className="space-y-16 animate-in fade-in duration-500 w-full text-slate-800">
      
      {/* Create Project Modal */}
      {isProjectModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={() => setIsProjectModalOpen(false)}></div>
          <div className="relative bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl animate-in zoom-in-95">
            <h3 className="text-xl font-bold text-slate-900 mb-4">{editingProjectId ? 'Edit Project' : 'Create New Project'}</h3>
            <input 
              type="text" 
              placeholder="Project Name" 
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-4 py-3 mb-4 focus:outline-none focus:border-emerald-400" 
            />
            <textarea 
              placeholder="Description" 
              rows={3} 
              value={newProjectDesc}
              onChange={(e) => setNewProjectDesc(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-4 py-3 mb-4 focus:outline-none focus:border-emerald-400"
            ></textarea>
            <div className="flex justify-end gap-2">
              <button onClick={() => setIsProjectModalOpen(false)} className="px-4 py-2 text-slate-500 font-bold hover:bg-slate-50 rounded-xl transition-colors">Cancel</button>
              <button 
                onClick={handleCreateOrEditProject} 
                disabled={isCreating}
                className="px-4 py-2 bg-emerald-600 text-white font-bold hover:bg-emerald-700 rounded-xl transition-colors disabled:opacity-50"
              >
                {isCreating ? 'Saving...' : (editingProjectId ? 'Save Changes' : 'Create Project')}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* 1. Universal Search (Hero) */}
      <section className="space-y-6">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">What would you like to do today?</h1>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button onClick={() => navigate('/hybrid-search')} className="p-4 bg-white border border-slate-200 rounded-2xl hover:border-emerald-400 hover:shadow-md transition-all flex flex-col items-center justify-center text-center group">
            <Search className="w-8 h-8 text-emerald-500 mb-3" />
            <span className="font-bold text-slate-800">Search Papers</span>
          </button>
          <button onClick={() => navigate('/assistant')} className="p-4 bg-white border border-slate-200 rounded-2xl hover:border-emerald-400 hover:shadow-md transition-all flex flex-col items-center justify-center text-center group">
            <Bot className="w-8 h-8 text-blue-500 mb-3" />
            <span className="font-bold text-slate-800">Ask AI Assistant</span>
          </button>
          <button onClick={() => navigate('/research')} className="p-4 bg-white border border-slate-200 rounded-2xl hover:border-emerald-400 hover:shadow-md transition-all flex flex-col items-center justify-center text-center group">
            <Briefcase className="w-8 h-8 text-indigo-500 mb-3" />
            <span className="font-bold text-slate-800">Continue Research</span>
          </button>
          <button onClick={() => navigate('/literature-review')} className="p-4 bg-white border border-slate-200 rounded-2xl hover:border-emerald-400 hover:shadow-md transition-all flex flex-col items-center justify-center text-center group">
            <BookOpen className="w-8 h-8 text-rose-500 mb-3" />
            <span className="font-bold text-slate-800">Generate Review</span>
          </button>
        </div>
      </section>

      {/* 2. Continue Research */}
      <section className="space-y-8">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Continue Research</h2>
          <button className="text-emerald-600 text-xs font-bold hover:underline">View All History</button>
        </div>
        
        {(!dashboardData.continueResearch || dashboardData.continueResearch.length === 0) ? (
           <div className="text-sm text-slate-500 text-center py-10 bg-white rounded-xl border border-slate-100">No active research topics. Start a search to begin.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {dashboardData.continueResearch.map((item: any) => (
              <div key={item.id} onClick={() => navigate(`/research`)} className="apple-card p-5 cursor-pointer group flex flex-col h-full hover:border-blue-300 transition-colors">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[10px] font-bold px-2.5 py-1 rounded-md uppercase tracking-wider text-blue-600 bg-blue-50">{item.type}</span>
                  <span className="text-[10px] font-semibold text-slate-400 flex items-center"><Clock className="w-3 h-3 mr-1" />{item.updatedAt ? formatDistanceToNow(new Date(item.updatedAt)) : "Recently"} ago</span>
                </div>
                <h4 className="font-bold text-slate-800 text-sm line-clamp-2 mb-4 group-hover:text-blue-600 transition-colors">{item.title}</h4>
                <div className="mt-auto pt-4 border-t border-slate-50">
                  <button className="text-xs font-bold text-slate-500 group-hover:text-blue-600 transition-colors flex items-center gap-1.5 w-full justify-center bg-slate-50 group-hover:bg-blue-50 py-2 rounded-lg">
                    <Play className="w-4 h-4" /> Continue
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* 3. Quick Actions */}
      <section className="space-y-6">
        <div className="flex items-center gap-2">
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Try Examples</h2>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
            Daily Grounded
          </span>
        </div>
        <div className="flex flex-wrap justify-start gap-3">
          {(dynamicExamples.length > 0 ? dynamicExamples : [
            { id: 'ex1', title: 'Explain Hybrid Retrieval', query: 'Explain Hybrid Retrieval with BM25 and Dense Vectors' },
            { id: 'ex2', title: 'Compare GraphRAG vs RAG', query: 'Compare GraphRAG vs traditional Vector RAG' },
            { id: 'ex3', title: 'Latest Medical AI Papers', query: 'Clinical diagnostics and medical imaging AI systems' }
          ]).map((item, i) => (
            <button 
              key={item.id || i} 
              onClick={() => fillSearchQuery(item.query || item.title)} 
              className="px-4 py-2.5 rounded-xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 text-xs font-bold transition-all shadow-sm flex items-center gap-2.5 hover:border-emerald-400 group cursor-pointer"
            >
              <Lightbulb className="w-3.5 h-3.5 text-emerald-500 group-hover:scale-110 transition-transform" /> 
              <span>{item.title}</span>
              {(item as any).sourceBadge && (
                <span className="text-[9px] font-mono font-bold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                  {(item as any).sourceBadge}
                </span>
              )}
            </button>
          ))}
        </div>
      </section>

      {/* 4. Research Domains */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Domains</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {domains.map((domain, i) => (
            <div key={i} onClick={() => navigate(`/research-domains/${domain.id}`)} className={cn("group apple-card p-6 flex flex-col h-full cursor-pointer")}>
              <div className="flex items-start justify-between mb-4">
                <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center transition-colors shadow-inner", domain.bg, domain.color, domain.hover)}>
                  <domain.icon className="w-6 h-6" />
                </div>
                <div className="text-right flex flex-col items-end">
                  <div className="flex items-center gap-1 bg-slate-50 px-1.5 py-0.5 rounded-full border border-slate-100">
                    <div className={cn("w-1.5 h-1.5 rounded-full", domain.source === 'Online + Offline' ? 'bg-emerald-500' : 'bg-blue-500')} />
                    <span className="text-[8px] font-bold text-slate-500 uppercase tracking-wider">{domain.source}</span>
                  </div>
                </div>
              </div>
              
              <h3 className="text-lg font-bold text-slate-800 mb-2 group-hover:text-emerald-600 transition-colors">{domain.name}</h3>
              <p className="text-slate-500 text-xs flex-grow mb-4 leading-relaxed font-medium">{domain.desc}</p>
              
              <div className="bg-slate-50 rounded-xl p-3 mb-4 border border-slate-100">
                <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-widest block mb-1">Trending Topic</span>
                <span className="text-xs font-bold text-slate-700">{domain.trending}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 5. Recent Papers */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Recent Papers</h2>
        {dashboardData.recentPapers.length === 0 ? (
          <div className="text-sm text-slate-500 py-6 text-center border border-dashed border-slate-200 rounded-xl bg-slate-50">
            You haven't interacted with any papers yet. Search for a paper to begin.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {dashboardData.recentPapers.map((paper: any, i: number) => (
              <div key={i} onClick={() => navigate('/paper-library')} className="apple-card p-6 cursor-pointer hover:border-emerald-300">
                <div className="flex justify-between items-start mb-3">
                  <span className="text-[10px] font-bold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md uppercase tracking-wider">{paper.domain || 'Uncategorized'}</span>
                  <button 
                    onClick={(e) => toggleBookmark(e, paper)}
                    className="p-1.5 rounded-lg transition-colors text-amber-500 bg-amber-50 hover:bg-amber-100"
                    title="Remove from saved papers"
                  >
                    <Bookmark className="w-5 h-5" fill="currentColor" />
                  </button>
                </div>
                <h3 className="text-lg font-bold text-slate-800 mb-2 leading-tight hover:text-emerald-600 transition-colors">{paper.title}</h3>
                <div className="flex items-center gap-2 text-xs font-medium text-slate-500 mb-4">
                  <span className="text-slate-600">{paper.authors}</span>
                  <span>•</span>
                  <span>{paper.publication}</span>
                </div>
                <p className="text-slate-500 text-xs leading-relaxed mb-5 line-clamp-3">
                  {paper.abstract}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-12">
          {/* 6. Active Projects */}
          <section className="space-y-6">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Projects</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {dashboardData.activeProjects.map((project: any, i: number) => (
                <div key={i} onClick={() => navigate('/research')} className="apple-card p-5 cursor-pointer hover:border-emerald-300 relative">
                  <div className="flex justify-between items-start mb-4">
                    <h4 className="font-bold text-slate-800 text-sm leading-tight pr-6">{project.name}</h4>
                    <div className="relative">
                      <button 
                        onClick={(e) => { e.stopPropagation(); setActiveDropdownProjectId(activeDropdownProjectId === project.id ? null : project.id); }} 
                        className="text-slate-400 hover:text-slate-600 p-1"
                      >
                        <MoreVertical className="w-4 h-4" />
                      </button>
                      {activeDropdownProjectId === project.id && (
                        <div className="absolute right-0 mt-1 w-36 bg-white border border-slate-200 rounded-xl shadow-xl z-10 py-1 animate-in fade-in zoom-in-95">
                          <button onClick={(e) => handleOpenEditModal(e, project)} className="w-full text-left px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 flex items-center gap-2">
                            <Edit3 className="w-3.5 h-3.5" /> Edit
                          </button>
                          <button onClick={(e) => handleDeleteProject(e, project.id)} className="w-full text-left px-4 py-2 text-sm font-semibold text-rose-600 hover:bg-rose-50 flex items-center gap-2">
                            <Trash2 className="w-3.5 h-3.5" /> Delete
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="mb-4">
                    <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1.5">
                      <span>Progress</span>
                      <span className="text-emerald-600">{project.progress}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${project.progress}%` }} />
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-auto">
                    <div className="text-[10px] font-semibold text-slate-400">
                      <span className="text-slate-600">{project.notes || 0}</span> Notes • {project.lastActivity}
                    </div>
                    <button className="text-[11px] font-bold text-emerald-600 hover:underline">Continue</button>
                  </div>
                </div>
              ))}
              
              {/* Create Project Card */}
              <div onClick={handleOpenCreateModal} className="bg-slate-50 border-2 border-dashed border-slate-200 rounded-2xl p-5 flex flex-col items-center justify-center text-slate-500 hover:text-slate-800 hover:border-emerald-400 hover:bg-emerald-50/50 transition-all cursor-pointer min-h-[160px] group">
                <div className="w-10 h-10 rounded-full bg-white border border-slate-200 shadow-sm flex items-center justify-center mb-3 group-hover:bg-emerald-500 group-hover:text-white group-hover:border-emerald-500 transition-colors">
                  <Plus className="w-5 h-5" />
                </div>
                <span className="font-bold text-sm">Create New Project</span>
              </div>
            </div>
          </section>
        </div>

        <div className="space-y-12">
          {/* 7. Recent Activity Timeline */}
          <section className="space-y-6">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Recent Activity</h2>
            <div className="apple-card p-6">
              {(!dashboardData.recentTimeline || dashboardData.recentTimeline.length === 0) ? (
                <div className="text-sm text-slate-500 text-center py-4 bg-slate-50 rounded-xl border border-dashed border-slate-200">
                  No recent activity recorded yet.
                </div>
              ) : (
                <div className="relative border-l-2 border-slate-100 ml-3 space-y-6 pb-2">
                  {dashboardData.recentTimeline.map((item: any, i: number) => (
                    <div key={i} className="relative pl-6">
                      <div className="absolute w-3 h-3 bg-white border-2 border-emerald-500 rounded-full -left-[7px] top-1.5 shadow-sm" />
                      <div className="flex flex-col">
                        <span className="text-xs font-bold text-slate-800">{item.action}</span>
                        <span className="text-[11px] font-medium text-slate-500 truncate mt-0.5" title={item.detail}>{item.detail}</span>
                        <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider mt-1.5">{item.time}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>

          {/* 8. Research Statistics (Analytics) */}
          <section className="space-y-6">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Analytics</h2>
            <div className="grid grid-cols-2 gap-4">
              {dashboardData.stats.map((stat: any, i: number) => (
                <div key={i} className="apple-card p-4 text-center">
                  <span className="block text-2xl font-black text-slate-800 mb-1">{stat.value}</span>
                  <span className="block text-[10px] font-bold text-slate-400 uppercase tracking-widest">{stat.label}</span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>

      {/* 10. Footer */}
      <footer className="mt-20 pt-8 border-t border-slate-100 flex flex-col md:flex-row items-center justify-between gap-4 text-xs font-semibold text-slate-500">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-emerald-500" />
          <span className="font-bold text-slate-800">ResearchNexus AI</span>
          <span>© 2026</span>
        </div>
        <div className="flex gap-6">
          <button className="hover:text-slate-800 transition-colors">Documentation</button>
          <button className="hover:text-slate-800 transition-colors">API</button>
          <button className="hover:text-slate-800 transition-colors">Privacy</button>
          <button className="hover:text-slate-800 transition-colors">Terms</button>
        </div>
      </footer>
      </div>
    </div>
  );
}
