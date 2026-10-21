import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Folder, Plus, FileText, ArrowLeft, Trash2, 
  Edit, PlusCircle, Calendar, BarChart2, BookOpen, Briefcase
} from 'lucide-react';
import { cn } from '../utils/cn';
import { useOverlayStore } from '../store/overlayStore';
import { useToastStore } from '../store/toastStore';
import { ConfirmationSheet, ActionSheet } from '../components/ui/Overlays';

interface Project {
  id: string;
  name: string;
  description: string;
  created_at?: string;
  updated_at?: string;
}

export default function ResearchPage() {
  const [viewState, setViewState] = useState<'grid' | 'detail'>('grid');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'papers' | 'notes' | 'review'>('overview');
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [projectPapers, setProjectPapers] = useState<any[]>([]);
  const [projectNotes, setProjectNotes] = useState<any[]>([]);
  const [loadingTab, setLoadingTab] = useState(false);
  const { openOverlay, closeOverlay } = useOverlayStore();
  const { addToast } = useToastStore();
  
  // Form State
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  
  // Edit Form State
  const [editProjectName, setEditProjectName] = useState('');
  const [editProjectDesc, setEditProjectDesc] = useState('');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setIsLoading(true);
    try {
      const { api } = await import('../utils/api');
      const data = await api.projects.getAll();
      setProjects(data);
    } catch (err) {
      addToast('Failed to load projects', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateProject = async () => {
    if (!newProjectName.trim()) return;
    try {
      const { api } = await import('../utils/api');
      const data = await api.projects.create({ name: newProjectName, description: newProjectDesc });
      setProjects([...projects, data]);
      setNewProjectName('');
      setNewProjectDesc('');
      closeOverlay();
      addToast('Project created successfully', 'success');
    } catch (err) {
      addToast('Failed to create project', 'error');
    }
  };
  
  const handleEditProject = async () => {
    if (!selectedProject || !editProjectName.trim()) return;
    try {
      const { api } = await import('../utils/api');
      const data = await api.projects.update(selectedProject.id, { 
        name: editProjectName, 
        description: editProjectDesc 
      });
      setProjects(projects.map(p => p.id === selectedProject.id ? data : p));
      setSelectedProject(data);
      closeOverlay();
      addToast('Project updated successfully', 'success');
    } catch (err) {
      addToast('Failed to update project', 'error');
    }
  };

  const handleDeleteProject = async () => {
    if (selectedProject) {
      try {
        const { api } = await import('../utils/api');
        await api.projects.delete(selectedProject.id);
        setProjects(projects.filter(p => p.id !== selectedProject.id));
        closeProject();
        closeOverlay();
        addToast('Project deleted successfully', 'success');
      } catch (err) {
        addToast('Failed to delete project', 'error');
      }
    }
  };

  const navigate = useNavigate();

  const openProject = async (project: Project) => {
    setSelectedProject(project);
    setViewState('detail');
    setActiveTab('overview');
    setLoadingTab(true);
    try {
      const { api } = await import('../utils/api');
      const papers = await api.projects.getPapers(project.id);
      const notes = await api.projects.getNotes(project.id);
      setProjectPapers(papers);
      setProjectNotes(notes);
    } catch (err) {
      addToast('Failed to load project details', 'error');
    } finally {
      setLoadingTab(false);
    }
  };

  const removePaper = async (paperId: string) => {
    if (!selectedProject) return;
    try {
      const { api } = await import('../utils/api');
      await api.projects.removePaper(selectedProject.id, paperId);
      setProjectPapers(prev => prev.filter(p => p.paper_id !== paperId));
      addToast('Paper removed from project', 'success');
    } catch (err) {
      addToast('Failed to remove paper', 'error');
    }
  };

  const closeProject = () => {
    setViewState('grid');
    setSelectedProject(null);
  };
  
  const openEditOverlay = () => {
    if (selectedProject) {
      setEditProjectName(selectedProject.name);
      setEditProjectDesc(selectedProject.description || '');
      openOverlay('action_sheet', { id: 'edit_project' });
    }
  };

  const formatDate = (isoString?: string) => {
    if (!isoString) return '';
    return isoString.split('T')[0];
  };

  return (
    <div className="h-full flex flex-col bg-[#FBFDFB] font-sans overflow-hidden relative rounded-xl border border-slate-200">
      {/* HEADER */}
      <header className="px-6 py-4 border-b border-slate-200 flex items-center justify-between shrink-0 bg-white z-10">
        <div className="flex items-center gap-4">
          {viewState === 'detail' && (
            <button onClick={closeProject} className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-400 hover:text-slate-700 transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </button>
          )}
          <div>
            <h1 className="text-xl font-black text-slate-900 flex items-center gap-2">
              <Folder className="w-5 h-5 text-emerald-600" /> 
              {viewState === 'grid' ? 'Research Projects' : selectedProject?.name}
            </h1>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {viewState === 'grid' ? (
            <button 
              onClick={() => openOverlay('action_sheet', { id: 'create_project' })}
              className="px-4 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
            >
              <Plus className="w-3.5 h-3.5" /> New Project
            </button>
          ) : (
            <>
              <button 
                onClick={openEditOverlay}
                className="px-3 py-1.5 text-xs font-bold text-slate-600 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
              >
                <Edit className="w-3.5 h-3.5" /> Edit
              </button>
              <button 
                onClick={() => openOverlay('confirmation_sheet', { id: 'delete_project' })}
                className="px-3 py-1.5 text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-100 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
              >
                <Trash2 className="w-3.5 h-3.5" /> Delete
              </button>
            </>
          )}
        </div>
      </header>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto scrollbar-hide min-h-0">
        {viewState === 'grid' ? (
          <div className="w-full max-w-7xl mx-auto p-6 md:p-8">
            {isLoading ? (
               <div className="flex justify-center p-12">
                 <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
               </div>
            ) : projects.length === 0 ? (
              <div className="flex flex-col items-center justify-center pt-20 animate-in fade-in duration-500 text-center">
                <Briefcase className="w-16 h-16 text-slate-200 mb-6" />
                <h2 className="text-xl font-bold text-slate-700 mb-2">No projects yet</h2>
                <p className="text-sm text-slate-500 max-w-md mb-8">
                  Create a project to organize your research.
                </p>
                <button 
                  onClick={() => openOverlay('action_sheet', { id: 'create_project' })}
                  className="px-6 py-2.5 text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg flex items-center gap-2 transition-colors shadow-sm"
                >
                  <Plus className="w-4 h-4" /> Create First Project
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map(project => (
                  <div 
                    key={project.id}
                    onClick={() => openProject(project)}
                    className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all cursor-pointer group flex flex-col h-[200px]"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-transform">
                        <Folder className="w-5 h-5" />
                      </div>
                    </div>
                    <h3 className="text-lg font-black text-slate-900 mb-1 group-hover:text-emerald-700 transition-colors line-clamp-1">{project.name}</h3>
                    <p className="text-sm font-medium text-slate-500 line-clamp-2 mb-4 flex-1">{project.description || "No description"}</p>
                    <div className="flex items-center justify-between text-[11px] font-bold text-slate-400 mt-auto pt-4 border-t border-slate-100">
                      <span className="flex items-center gap-1">{project.updated_at ? <><Calendar className="w-3.5 h-3.5" /> {formatDate(project.updated_at)}</> : ''}</span>
                    </div>
                  </div>
                ))}
                
                <div 
                  onClick={() => openOverlay('action_sheet', { id: 'create_project' })}
                  className="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-emerald-400 hover:bg-emerald-50 transition-all cursor-pointer flex flex-col items-center justify-center text-center h-[200px]"
                >
                  <PlusCircle className="w-8 h-8 text-slate-400 mb-3" />
                  <h3 className="text-sm font-bold text-slate-600">Create New Project</h3>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col h-full relative">
            <div className="px-6 md:px-8 pt-6 border-b border-slate-200 bg-white">
              <div className="max-w-4xl mx-auto">
                <div className="flex gap-6">
                  {[
                    { id: 'overview', label: 'OVERVIEW' },
                    { id: 'papers', label: 'PAPERS' },
                    { id: 'notes', label: 'NOTES' },
                    { id: 'review', label: 'LITERATURE REVIEW' }
                  ].map(tab => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={cn(
                        "pb-3 text-xs font-bold tracking-widest transition-colors",
                        activeTab === tab.id
                          ? "text-emerald-600 border-b-2 border-emerald-600"
                          : "text-slate-400 hover:text-slate-700"
                      )}
                      style={{ marginBottom: activeTab === tab.id ? '-2px' : '0' }}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 md:p-8">
              <div className="max-w-4xl mx-auto">
                {activeTab === 'overview' && (
                  <div className="space-y-8 animate-in fade-in">
                    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                      <h2 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Project Summary</h2>
                      <p className="text-slate-700 leading-relaxed font-medium">
                        {selectedProject?.description || "No description provided."}
                      </p>
                    </div>
                  </div>
                )}

                {activeTab === 'papers' && (
                  <div className="animate-in fade-in">
                    {loadingTab ? (
                      <div className="text-center py-20 text-slate-500 font-medium">Loading papers...</div>
                    ) : projectPapers.length === 0 ? (
                      <div className="text-center py-20">
                        <FileText className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                        <h3 className="text-lg font-bold text-slate-700 mb-2">No Papers Attached</h3>
                        <p className="text-slate-500">Search and add papers to this project to build your library.</p>
                      </div>
                    ) : (
                      <div className="grid gap-4">
                        {projectPapers.map(pp => (
                          <div key={pp.id} className="bg-white border border-slate-200 rounded-xl p-5 hover:border-slate-300 transition-colors">
                            <h3 className="font-bold text-slate-800 mb-1">{pp.paper.title}</h3>
                            <p className="text-sm text-slate-500 mb-3">{pp.paper.authors}</p>
                            <div className="flex gap-3">
                              <a href={pp.paper.url || '#'} target="_blank" rel="noreferrer" className="text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-lg hover:bg-emerald-100 transition-colors">Open Paper</a>
                              <button onClick={() => navigate(`/notebook?create=true&paperId=${pp.paper_id}&projectId=${selectedProject?.id}`)} className="text-xs font-bold text-amber-600 bg-amber-50 px-3 py-1.5 rounded-lg hover:bg-amber-100 transition-colors">Add Note</button>
                              <button onClick={() => removePaper(pp.paper_id)} className="text-xs font-bold text-rose-600 bg-rose-50 px-3 py-1.5 rounded-lg hover:bg-rose-100 transition-colors">Remove</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'notes' && (
                  <div className="animate-in fade-in">
                    {loadingTab ? (
                      <div className="text-center py-20 text-slate-500 font-medium">Loading notes...</div>
                    ) : projectNotes.length === 0 ? (
                      <div className="text-center py-20">
                        <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                        <h3 className="text-lg font-bold text-slate-700 mb-2">No Notes Yet</h3>
                        <p className="text-slate-500">Add notes from papers or the Notebook.</p>
                      </div>
                    ) : (
                      <div className="grid gap-4">
                        {projectNotes.map(n => (
                          <div key={n.id} onClick={() => navigate(`/notebook/${n.id}`)} className="bg-amber-50 border border-amber-100 rounded-xl p-5 cursor-pointer hover:border-amber-300 transition-colors">
                            <p className="text-sm text-slate-700 whitespace-pre-wrap line-clamp-3">{n.content}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'review' && (
                  <div className="text-center py-20 animate-in fade-in">
                    <BarChart2 className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                    <h3 className="text-lg font-bold text-slate-700 mb-2">Literature Review</h3>
                    <p className="text-sm text-slate-500 max-w-sm mx-auto mb-6">Use the AI Assistant to synthesize your collected papers into a full literature review.</p>
                    <button onClick={() => navigate('/literature-review', { state: { projectId: selectedProject?.id } })} className="px-4 py-2 bg-slate-900 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold transition-colors">
                      Start Workflow
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* OVERLAYS */}
      <ConfirmationSheet 
        id="delete_project"
        title="Delete Project?"
        description="This will permanently delete the project and all associated notes. Papers will remain in your library. This action cannot be undone."
        onConfirm={handleDeleteProject}
      />
      <ActionSheet id="create_project" title="New Project">
        <div className="space-y-4">
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-2">Project Name</label>
            <input 
              type="text" 
              value={newProjectName}
              onChange={e => setNewProjectName(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-400" 
            />
          </div>
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-2">Description</label>
            <textarea 
              value={newProjectDesc}
              onChange={e => setNewProjectDesc(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-400 min-h-[80px]" 
            />
          </div>
          <button 
            onClick={handleCreateProject}
            disabled={!newProjectName.trim()}
            className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold rounded-lg text-sm transition-colors"
          >
            Create Project
          </button>
        </div>
      </ActionSheet>
      <ActionSheet id="edit_project" title="Edit Project">
         <div className="space-y-4">
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-2">Project Name</label>
            <input 
              type="text" 
              value={editProjectName}
              onChange={e => setEditProjectName(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-400" 
            />
          </div>
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-2">Description</label>
            <textarea 
              value={editProjectDesc}
              onChange={e => setEditProjectDesc(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-400 min-h-[80px]" 
            />
          </div>
          <button 
            onClick={handleEditProject}
            disabled={!editProjectName.trim()}
            className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold rounded-lg text-sm transition-colors"
          >
            Save Changes
          </button>
        </div>
      </ActionSheet>
    </div>
  );
}
