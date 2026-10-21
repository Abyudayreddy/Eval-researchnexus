import { useEffect, useState } from 'react';
import { 
  BarChart, Bar, 
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { 
  Clock, CheckCircle2, Download, BookOpen, 
  Map, Target, Filter, Briefcase, FileText, Trophy,
  Plus, Edit2, Trash2
} from 'lucide-react';
import { api } from '../utils/api';
import { useOverlayStore } from '../store/overlayStore';
import { CenteredSheet } from '../components/ui/Overlays';
import { toast } from 'sonner';

function ResearchGoals() {
  const [goals, setGoals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { openOverlay, closeOverlay } = useOverlayStore();
  
  const [formState, setFormState] = useState({ id: '', title: '', description: '', due_date: '', priority: 'medium', status: 'not_started' });

  const loadGoals = async () => {
    try {
      const data = await api.goals.getAll();
      setGoals(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGoals();
  }, []);

  const handleOpenSheet = (goal?: any) => {
    if (goal) {
      setFormState({ id: goal.id, title: goal.title, description: goal.description || '', due_date: goal.due_date || '', priority: goal.priority, status: goal.status });
    } else {
      setFormState({ id: '', title: '', description: '', due_date: '', priority: 'medium', status: 'not_started' });
    }
    openOverlay('centered_sheet', { id: 'goal_sheet' });
  };

  const handleSaveGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (formState.id) {
        await api.goals.update(formState.id, formState);
        toast.success("Goal updated");
      } else {
        await api.goals.create(formState);
        toast.success("Goal created");
      }
      closeOverlay();
      loadGoals();
    } catch (error) {
      toast.error("Failed to save goal");
    }
  };

  const handleDelete = async (id: string) => {
    openOverlay('confirmation_sheet', { 
      id: 'delete_goal',
      title: 'Delete this research goal?',
      onConfirm: async () => {
        try {
          await api.goals.delete(id);
          toast.success("Goal deleted");
          loadGoals();
        } catch (error) {
          toast.error("Failed to delete goal");
        }
      }
    });
  };

  const markCompleted = async (id: string) => {
    try {
      await api.goals.update(id, { status: 'completed' });
      toast.success("Goal completed");
      loadGoals();
    } catch (error) {
      toast.error("Failed to update goal");
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-500" /> Research Goals
          </h3>
          <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">Keep track of what you want to accomplish.</p>
        </div>
        <button 
          onClick={() => handleOpenSheet()}
          className="px-4 py-2 bg-emerald-600 text-white text-sm font-bold rounded-xl flex items-center gap-2 hover:bg-emerald-700 transition-colors shadow-sm"
        >
          <Plus className="w-4 h-4" /> New Research Goal
        </button>
      </div>

      {loading ? (
        <div className="flex-1 flex flex-col items-center justify-center text-center py-6">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
        </div>
      ) : goals.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center text-center py-12 border border-dashed border-slate-200 rounded-xl bg-slate-50">
          <Trophy className="w-10 h-10 text-slate-300 mb-4" />
          <h4 className="text-base font-bold text-slate-700 mb-1">No research goals yet.</h4>
          <p className="text-sm font-medium text-slate-500 mb-6 max-w-sm">Set a research goal to keep track of what you want to accomplish.</p>
          <button 
            onClick={() => handleOpenSheet()}
            className="px-5 py-2.5 bg-white border border-slate-200 text-slate-700 font-bold rounded-lg hover:border-emerald-400 hover:text-emerald-700 transition-colors shadow-sm"
          >
            + Create Research Goal
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {goals.map(goal => (
            <div key={goal.id} className="border border-slate-200 rounded-xl p-5 hover:shadow-md transition-all flex flex-col">
              <div className="flex justify-between items-start mb-2">
                <h4 className="text-base font-black text-slate-900 line-clamp-2 pr-4">{goal.title}</h4>
                {goal.status === 'completed' && (
                  <span className="shrink-0 flex items-center gap-1 text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full uppercase tracking-widest">
                    <CheckCircle2 className="w-3 h-3" /> Completed
                  </span>
                )}
              </div>
              
              {goal.description && <p className="text-sm text-slate-500 mb-4 line-clamp-3">{goal.description}</p>}
              
              <div className="mt-auto space-y-2 mb-4 pt-2 border-t border-slate-100">
                {goal.due_date && (
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-bold text-slate-400 uppercase tracking-widest">Due</span>
                    <span className="font-bold text-slate-700">{goal.due_date}</span>
                  </div>
                )}
                <div className="flex justify-between items-center text-xs">
                  <span className="font-bold text-slate-400 uppercase tracking-widest">Priority</span>
                  <span className={`font-bold capitalize ${goal.priority === 'high' ? 'text-rose-600' : goal.priority === 'medium' ? 'text-amber-600' : 'text-blue-600'}`}>
                    {goal.priority}
                  </span>
                </div>
                {goal.status !== 'completed' && (
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-bold text-slate-400 uppercase tracking-widest">Status</span>
                    <span className="font-bold text-slate-700 capitalize">{goal.status.replace('_', ' ')}</span>
                  </div>
                )}
              </div>
              
              <div className="flex items-center gap-2 pt-3 border-t border-slate-100">
                {goal.status !== 'completed' && (
                  <button onClick={() => markCompleted(goal.id)} className="flex-1 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-bold text-xs rounded-lg transition-colors border border-emerald-200">
                    Complete
                  </button>
                )}
                <button onClick={() => handleOpenSheet(goal)} className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                  <Edit2 className="w-4 h-4" />
                </button>
                <button onClick={() => handleDelete(goal.id)} className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <CenteredSheet id="goal_sheet" title={formState.id ? "Edit Goal" : "New Research Goal"}>
        <form onSubmit={handleSaveGoal} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Goal Title</label>
            <input 
              type="text" 
              required
              value={formState.title}
              onChange={e => setFormState({...formState, title: e.target.value})}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm font-medium focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 outline-none"
              placeholder="e.g., Complete healthcare AI review"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Description (Optional)</label>
            <textarea 
              value={formState.description}
              onChange={e => setFormState({...formState, description: e.target.value})}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm font-medium focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 outline-none h-24 resize-none"
              placeholder="Details about what you want to achieve..."
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Due Date (Optional)</label>
              <input 
                type="text" 
                value={formState.due_date}
                onChange={e => setFormState({...formState, due_date: e.target.value})}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm font-medium focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 outline-none"
                placeholder="e.g., This Friday"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Priority</label>
              <select 
                value={formState.priority}
                onChange={e => setFormState({...formState, priority: e.target.value})}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm font-medium focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 outline-none"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Status</label>
            <select 
              value={formState.status}
              onChange={e => setFormState({...formState, status: e.target.value})}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm font-medium focus:border-emerald-400 focus:ring-1 focus:ring-emerald-400 outline-none"
            >
              <option value="not_started">Not Started</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          
          <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-100">
            <button type="button" onClick={() => closeOverlay()} className="px-4 py-2 text-sm font-bold text-slate-500 hover:text-slate-800 transition-colors">
              Cancel
            </button>
            <button type="submit" className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-lg transition-colors shadow-sm">
              {formState.id ? 'Update Goal' : 'Create Goal'}
            </button>
          </div>
        </form>
      </CenteredSheet>

    </div>
  );
}

export default function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await api.analytics.getOverview();
        setAnalyticsData(data);
      } catch (error) {
        console.error("Failed to load analytics data", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  const hasData = analyticsData !== null;
  const stats = analyticsData?.stats || [];
  const activity = analyticsData?.activity || [];
  const timeline = analyticsData?.timeline || [];
  const insights = analyticsData?.insights || [];

  // Map icons for Timeline
  const getTimelineIcon = (action: string) => {
    if (action.includes("Project")) return { icon: CheckCircle2, color: "text-emerald-500 border-emerald-100" };
    if (action.includes("Paper Saved")) return { icon: Download, color: "text-blue-500 border-blue-100" };
    if (action.includes("Paper Opened")) return { icon: BookOpen, color: "text-indigo-500 border-indigo-100" };
    if (action.includes("Note")) return { icon: FileText, color: "text-purple-500 border-purple-100" };
    return { icon: Map, color: "text-amber-500 border-amber-100" }; // Search
  };

  // Map values for Top Cards
  const getStatTitleDesc = (label: string) => {
    if (label.includes("Sessions")) return { title: "RESEARCH SESSIONS", desc: "Total Searches", icon: Clock, color: "text-emerald-500" };
    if (label.includes("Papers Opened")) return { title: "PAPERS OPENED", desc: "Views", icon: BookOpen, color: "text-blue-500" };
    if (label.includes("Saved")) return { title: "PAPERS SAVED", desc: "Bookmarks", icon: Download, color: "text-indigo-500" };
    if (label.includes("Projects")) return { title: "ACTIVE PROJECTS", desc: "Workspaces", icon: Briefcase, color: "text-amber-500" };
    return { title: label.toUpperCase(), desc: "Count", icon: Target, color: "text-purple-500" };
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-[#FBFDFB]">
      
      {/* MAIN CONTENT AREA */}
      <div className="flex-1 overflow-y-auto p-4 md:p-8">
        <div className="max-w-[1400px] mx-auto space-y-8 animate-in fade-in duration-300">
          
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-black text-slate-900 tracking-tight">Research Analytics</h1>
              <p className="text-sm font-medium text-slate-500 mt-2">Track your research journey, productivity and knowledge growth.</p>
            </div>
            
            <div className="flex items-center gap-3">
              <button className="px-4 py-2 bg-white border border-slate-200 text-slate-600 text-sm font-bold rounded-xl flex items-center gap-2 hover:bg-slate-50 transition-colors">
                <Clock className="w-4 h-4" /> Last 7 Days
              </button>
              <button className="px-4 py-2 bg-white border border-slate-200 text-slate-600 text-sm font-bold rounded-xl flex items-center gap-2 hover:bg-slate-50 transition-colors">
                <Filter className="w-4 h-4" /> Filter
              </button>
              <div className="h-6 w-px bg-slate-200 mx-1"></div>
              <button className="px-4 py-2 bg-emerald-600 text-white text-sm font-bold rounded-xl flex items-center gap-2 hover:bg-emerald-700 transition-colors shadow-sm shadow-emerald-600/20">
                <Download className="w-4 h-4" /> Export Report
              </button>
            </div>
          </div>

          {!isLoading && hasData ? (
            <>
              {/* Stat Cards (Top Row) */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((stat: any, i: number) => {
                  const config = getStatTitleDesc(stat.label);
                  const Icon = config.icon;
                  return (
                    <div key={i} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-slate-300 transition-all group">
                      <div className="flex justify-between items-start mb-4">
                        <div className={`p-2 rounded-lg bg-slate-50 group-hover:scale-110 transition-transform ${config.color}`}>
                          <Icon className="w-5 h-5" />
                        </div>
                        <span className="text-[10px] font-bold text-slate-400 bg-slate-50 px-2 py-1 rounded-full">
                          {config.desc}
                        </span>
                      </div>
                      <h3 className="text-3xl font-black text-slate-900 mb-1">{stat.value}</h3>
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{config.title}</p>
                    </div>
                  );
                })}
              </div>

              {/* Top Row: Research Activity and Reading Insights */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Research Activity */}
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col min-h-[350px]">
                  <div className="flex justify-between items-start mb-8">
                    <div>
                      <h3 className="text-lg font-bold text-slate-900">Research Activity</h3>
                      <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">Last 7 Days (Searches & Opens)</p>
                    </div>
                  </div>
                  
                  {activity.length > 0 ? (
                    <div className="flex-1 w-full h-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={activity} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                          <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#64748b', fontWeight: 600 }} dy={10} />
                          <YAxis allowDecimals={false} axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#64748b' }} dx={-10} />
                          <Tooltip 
                            cursor={{ fill: '#f8fafc' }}
                            contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                            itemStyle={{ fontSize: '13px', fontWeight: 600 }}
                          />
                          <Bar dataKey="Searches" fill="#10b981" radius={[4, 4, 0, 0]} maxBarSize={40} />
                          <Bar dataKey="Papers Opened" fill="#3b82f6" radius={[4, 4, 0, 0]} maxBarSize={40} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col items-center justify-center text-center">
                      <Target className="w-8 h-8 text-slate-300 mb-3" />
                      <p className="text-sm font-medium text-slate-500">Your research activity will appear here as you search and explore.</p>
                    </div>
                  )}
                </div>

                {/* Reading Insights */}
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col min-h-[350px]">
                  <div className="mb-6">
                    <h3 className="text-lg font-bold text-slate-900">Reading Insights</h3>
                    <p className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">Top Research Topics</p>
                  </div>
                  
                  {insights.length > 0 ? (
                    <div className="flex-1 min-h-[200px] w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart 
                          data={insights.map((item: any) => ({
                            ...item,
                            displayName: item.name && item.name.length > 24 ? item.name.substring(0, 22) + '…' : item.name,
                            fullName: item.name
                          }))} 
                          layout="vertical" 
                          margin={{ top: 0, right: 20, left: 10, bottom: 0 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
                          <XAxis type="number" allowDecimals={false} axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#94a3b8', fontWeight: 600 }} />
                          <YAxis 
                            type="category" 
                            dataKey="displayName" 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fontSize: 11, fill: '#64748b', fontWeight: 600 }} 
                            width={140}
                          />
                          <Tooltip 
                            cursor={{ fill: 'rgba(16, 185, 129, 0.05)' }}
                            formatter={(val: any, _name: any, item: any) => [
                              `${val} searches`,
                              item?.payload?.fullName || 'Topic'
                            ]}
                            contentStyle={{ 
                              borderRadius: '12px', 
                              backgroundColor: 'var(--bg-card, #ffffff)', 
                              borderColor: 'var(--border-color, #e2e8f0)',
                              color: 'var(--text-main, #0f172a)',
                              boxShadow: '0 8px 16px -2px rgba(0, 0, 0, 0.15)' 
                            }}
                            itemStyle={{ fontSize: '12px', fontWeight: 600, color: '#10b981' }}
                          />
                          <Bar dataKey="value" fill="#10b981" radius={[0, 4, 4, 0]} barSize={20} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col items-center justify-center text-center py-6">
                      <BookOpen className="w-8 h-8 text-slate-300 mb-3" />
                      <p className="text-sm font-medium text-slate-500">Insights will appear as your research activity grows.</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Middle Row: Research Goals */}
              <ResearchGoals />

              {/* Bottom Row */}
              <div className="grid grid-cols-1 gap-6">
                
                {/* Research Timeline */}
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col max-h-[450px]">
                  <h3 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2"><Clock className="w-5 h-5 text-blue-500" /> Research Timeline</h3>
                  
                  {timeline.length > 0 ? (
                    <div className="flex-1 overflow-y-auto pr-2 space-y-6 relative before:absolute before:inset-0 before:ml-4 before:-translate-x-px before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
                      {timeline.map((item: any, i: number) => {
                        const config = getTimelineIcon(item.action);
                        const Icon = config.icon;
                        return (
                          <div key={i} className="relative flex items-start group is-active pl-12">
                            {/* Icon Marker */}
                            <div className={`absolute left-0 flex items-center justify-center w-8 h-8 rounded-full border-4 border-white bg-slate-100 shadow-sm z-10 ${config.color}`}>
                              <Icon className="w-3.5 h-3.5" />
                            </div>
                            
                            {/* Content Box */}
                            <div className="w-full p-4 rounded-xl border border-slate-100 bg-slate-50 hover:bg-white hover:border-slate-200 hover:shadow-sm transition-all">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-xs font-bold text-slate-800">{item.action}</span>
                                <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">{item.time}</span>
                              </div>
                              <p className="text-[11px] font-medium text-slate-500 line-clamp-2">{item.detail}</p>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col items-center justify-center text-center py-6">
                      <Clock className="w-8 h-8 text-slate-300 mb-3" />
                      <p className="text-sm font-medium text-slate-500">No research activity yet.</p>
                    </div>
                  )}
                </div>

              </div>
            </>
          ) : (
             <div className="flex flex-col items-center justify-center py-32">
              <p className="text-sm font-bold text-slate-400 animate-pulse">Loading analytics...</p>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
