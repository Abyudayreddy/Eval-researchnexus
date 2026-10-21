import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { 
  Plus, Search, FileText,
  ChevronLeft, BookOpen, Clock, Trash2, Save
} from 'lucide-react';
import { useToastStore } from '../store/toastStore';
import { SideDrawer } from '../components/ui/Overlays';

interface Note {
  id: string;
  content: string;
  updated_at?: string;
}

export default function NotebookPage() {
  const { noteId } = useParams();
  const [searchParams] = useSearchParams();
  const { addToast } = useToastStore();
  
  const [viewState, setViewState] = useState<'list' | 'editor'>(noteId ? 'editor' : 'list');
  const [notes, setNotes] = useState<Note[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Context state
  const [paperId] = useState<string | null>(searchParams.get('paperId'));
  const [projectId] = useState<string | null>(searchParams.get('projectId'));
  
  // Editor state
  const [selectedNoteId, setSelectedNoteId] = useState<string | null>(null);
  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');

  useEffect(() => {
    if (searchParams.get('create') === 'true') {
      setViewState('editor');
    }
  }, [searchParams]);

  useEffect(() => {
    if (noteId && notes.length > 0) {
      const noteToOpen = notes.find(n => n.id === noteId);
      if (noteToOpen && noteToOpen.id !== selectedNoteId) {
        openNote(noteToOpen);
      }
    }
  }, [noteId, notes]);

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    setIsLoading(true);
    try {
      const { api } = await import('../utils/api');
      const data = await api.notes.getAll();
      setNotes(data);
    } catch (err) {
      addToast('Failed to load notes', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const openNote = (note: Note) => {
    setSelectedNoteId(note.id);
    const parts = note.content.split('\n\n');
    if (parts.length > 1) {
      setNoteTitle(parts[0]);
      setNoteContent(parts.slice(1).join('\n\n'));
    } else {
      setNoteTitle('');
      setNoteContent(note.content);
    }
    setViewState('editor');
  };

  const createNewNote = () => {
    setSelectedNoteId(null);
    setNoteTitle('');
    setNoteContent('');
    setViewState('editor');
  };

  const closeNote = () => {
    setViewState('list');
    setSelectedNoteId(null);
  };

  const handleSaveNote = async () => {
    const fullContent = noteTitle.trim() ? `${noteTitle}\n\n${noteContent}` : noteContent;
    if (!fullContent.trim()) {
      addToast('Cannot save an empty note', 'error');
      return;
    }
    
    try {
      const { api } = await import('../utils/api');
      if (selectedNoteId) {
        const data = await api.notes.update(selectedNoteId, { content: fullContent });
        setNotes(notes.map(n => n.id === selectedNoteId ? data : n));
        addToast('Note updated successfully', 'success');
      } else {
        const data = await api.notes.create({ 
          content: fullContent,
          paper_id: paperId || undefined,
          project_id: projectId || undefined
        });
        setNotes([data, ...notes]);
        setSelectedNoteId(data.id);
        addToast('Note created successfully', 'success');
      }
    } catch (err) {
      addToast('Failed to save note', 'error');
    }
  };

  const handleDeleteNote = async () => {
    if (!selectedNoteId) {
      closeNote();
      return;
    }
    try {
      const { api } = await import('../utils/api');
      await api.notes.delete(selectedNoteId);
      setNotes(notes.filter(n => n.id !== selectedNoteId));
      addToast('Note deleted successfully', 'success');
      closeNote();
    } catch (err) {
      addToast('Failed to delete note', 'error');
    }
  };

  const getNotePreview = (content: string) => {
    const parts = content.split('\n\n');
    return {
      title: parts.length > 1 ? parts[0] : (content.substring(0, 30) || 'Untitled Note'),
      preview: parts.length > 1 ? parts.slice(1).join('\n\n') : content
    };
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
          {viewState === 'editor' && (
            <button onClick={closeNote} className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-400 hover:text-slate-700 transition-colors">
              <ChevronLeft className="w-5 h-5" />
            </button>
          )}
          <h1 className="text-xl font-black text-slate-900 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-600" /> Notebook
          </h1>
        </div>
        <div className="flex items-center gap-2">
          {viewState === 'list' ? (
            <>
              <div className="relative hidden md:block">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input 
                  type="text" 
                  placeholder="Search notes..."
                  className="w-48 bg-slate-50 border border-slate-200 text-xs text-slate-800 rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:border-emerald-400 transition-colors shadow-sm"
                />
              </div>
              <button 
                onClick={createNewNote}
                className="px-4 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
              >
                <Plus className="w-3.5 h-3.5" /> New Note
              </button>
            </>
          ) : (
            <>
              <button 
                onClick={handleDeleteNote}
                className="px-3 py-1.5 text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-100 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
              <button 
                onClick={handleSaveNote}
                className="px-4 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
              >
                <Save className="w-3.5 h-3.5" /> Save Note
              </button>
            </>
          )}
        </div>
      </header>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto bg-slate-50 min-h-0">
        {viewState === 'list' ? (
          <div className="max-w-5xl mx-auto p-6 md:p-10 space-y-8">
            {isLoading ? (
               <div className="flex justify-center p-12">
                 <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
               </div>
            ) : notes.length === 0 ? (
              <div className="flex flex-col items-center justify-center pt-20 animate-in fade-in duration-500 text-center">
                <BookOpen className="w-16 h-16 text-slate-200 mb-6" />
                <h2 className="text-xl font-bold text-slate-700 mb-2">No notes yet</h2>
                <p className="text-sm text-slate-500 max-w-md mb-8">
                  Add a note while working on your research.
                </p>
                <button 
                  onClick={createNewNote}
                  className="px-6 py-2.5 text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg flex items-center gap-2 transition-colors shadow-sm"
                >
                  <Plus className="w-4 h-4" /> Create First Note
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {notes.map(note => {
                  const { title, preview } = getNotePreview(note.content);
                  return (
                    <div 
                      key={note.id}
                      onClick={() => openNote(note)}
                      className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-emerald-300 transition-all cursor-pointer group flex flex-col h-[200px]"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:scale-110 transition-transform">
                          <FileText className="w-5 h-5" />
                        </div>
                      </div>
                      <h3 className="text-lg font-black text-slate-900 mb-1 group-hover:text-emerald-700 transition-colors truncate">{title}</h3>
                      <p className="text-sm font-medium text-slate-500 line-clamp-2 mb-4 flex-1">{preview}</p>
                      <div className="flex items-center justify-between text-[11px] font-bold text-slate-400 mt-auto pt-4 border-t border-slate-100">
                        <span className="flex items-center gap-1">{note.updated_at ? <><Clock className="w-3.5 h-3.5" /> {formatDate(note.updated_at)}</> : ''}</span>
                      </div>
                    </div>
                  );
                })}
                
                <div 
                  onClick={createNewNote}
                  className="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-emerald-400 hover:bg-emerald-50 transition-all cursor-pointer flex flex-col items-center justify-center text-center h-[200px]"
                >
                  <Plus className="w-8 h-8 text-slate-400 mb-3" />
                  <h3 className="text-sm font-bold text-slate-600">Create New Note</h3>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="max-w-3xl mx-auto my-8 bg-white border border-slate-200 shadow-sm rounded-2xl min-h-[80vh] flex flex-col overflow-hidden">
            <header className="px-8 py-5 flex flex-col gap-3 shrink-0 border-b border-slate-100 bg-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-slate-400">
                  <span>Research Note</span>
                </div>
              </div>
            </header>

            <div className="flex-1 p-8 text-slate-800 flex flex-col">
              <input 
                type="text" 
                value={noteTitle}
                onChange={(e) => setNoteTitle(e.target.value)}
                placeholder="Note Title" 
                className="text-3xl font-black text-slate-900 border-none outline-none mb-6 placeholder:text-slate-300"
              />
              <textarea 
                value={noteContent}
                onChange={(e) => setNoteContent(e.target.value)}
                placeholder="Start typing your research notes... Use [[ to link to papers."
                className="flex-1 w-full resize-none outline-none text-base font-medium leading-relaxed text-slate-700 placeholder:text-slate-300"
              />
            </div>
          </div>
        )}
      </div>

      {/* OVERLAYS */}
      <SideDrawer id="note_context" title="Note Context" position="right">
        <div className="space-y-6">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-3">Linked Papers</span>
            <div className="text-center p-6 border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
              <p className="text-xs font-semibold text-slate-500 mb-3">No papers linked to this note.</p>
              <button className="px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-600 hover:text-emerald-600 transition-colors shadow-sm">
                Attach Paper
              </button>
            </div>
          </div>
        </div>
      </SideDrawer>
    </div>
  );
}
