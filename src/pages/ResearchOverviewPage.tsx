import { useParams, useNavigate } from 'react-router-dom';
import { useResearchSessionStore } from '../store/researchSessionStore';
import { formatDistanceToNow } from 'date-fns';
import { Search, MessageSquare, BookOpen, Bookmark, FileText, Activity } from 'lucide-react';
import { useEffect } from 'react';

export default function ResearchOverviewPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { topics, setActiveTopic } = useResearchSessionStore();
  
  const topic = id ? topics[id] : null;

  useEffect(() => {
    if (id && topic) {
      setActiveTopic(id);
    }
  }, [id, topic, setActiveTopic]);

  if (!topic) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500">
        <p>Research Topic not found.</p>
        <button onClick={() => navigate('/')} className="mt-4 text-blue-500 hover:underline">Return to Dashboard</button>
      </div>
    );
  }

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  return (
    <div className="flex-1 flex flex-col h-full max-w-5xl mx-auto w-full pb-10">
      <div className="mb-8 mt-4">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">{topic.title} in {topic.domain}</h1>
        <p className="text-slate-500">Started {formatDistanceToNow(new Date(topic.timeline[0]?.timestamp || topic.lastOpenedAt), { addSuffix: true })}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Left Column: Stats and Quick Links */}
        <div className="flex flex-col gap-6">
          
          {/* Progress Tracker */}
          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-600" /> Research Progress
            </h2>
            <div className="space-y-5">
              <div>
                <div className="flex justify-between text-xs mb-1.5 uppercase tracking-widest font-bold">
                  <span className="text-slate-500">1. Exploration</span>
                  <span className="text-emerald-600">100%</span>
                </div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full w-full"></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5 uppercase tracking-widest font-bold">
                  <span className="text-slate-500">2. Synthesis</span>
                  <span className="text-emerald-600">65%</span>
                </div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full w-[65%]"></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1.5 uppercase tracking-widest font-bold">
                  <span className="text-slate-500">3. Review Generation</span>
                  <span className="text-emerald-600">15%</span>
                </div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full w-[15%]"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Overview</h2>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-100 flex flex-col items-center justify-center text-center">
                <span className="text-2xl font-bold text-slate-700">{topic.selectedPapers?.length || 0}</span>
                <span className="text-sm text-slate-500">Papers</span>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-100 flex flex-col items-center justify-center text-center">
                <span className="text-2xl font-bold text-slate-700">{topic.notes?.length || 0}</span>
                <span className="text-sm text-slate-500">Notes</span>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-100 flex flex-col items-center justify-center text-center">
                <span className="text-2xl font-bold text-slate-700">{topic.aiConversations?.length || 0}</span>
                <span className="text-sm text-slate-500">AI Chats</span>
              </div>
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-100 flex flex-col items-center justify-center text-center">
                <span className="text-2xl font-bold text-slate-700">{topic.bookmarks?.length || 0}</span>
                <span className="text-sm text-slate-500">Bookmarks</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Continue with</h2>
            
            <div className="flex flex-col gap-2">
              <button onClick={() => handleNavigate('/search')} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors text-left border border-transparent hover:border-slate-200 group">
                <div className="p-2 bg-blue-100 text-blue-600 rounded-md group-hover:bg-blue-600 group-hover:text-white transition-colors">
                  <Search className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-medium text-slate-900">Search Papers</div>
                  <div className="text-xs text-slate-500">Find new literature</div>
                </div>
              </button>
              
              <button onClick={() => handleNavigate('/assistant')} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors text-left border border-transparent hover:border-slate-200 group">
                <div className="p-2 bg-purple-100 text-purple-600 rounded-md group-hover:bg-purple-600 group-hover:text-white transition-colors">
                  <MessageSquare className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-medium text-slate-900">Ask AI</div>
                  <div className="text-xs text-slate-500">Discuss papers and concepts</div>
                </div>
              </button>
              
              <button onClick={() => handleNavigate('/notebook')} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors text-left border border-transparent hover:border-slate-200 group">
                <div className="p-2 bg-amber-100 text-amber-600 rounded-md group-hover:bg-amber-600 group-hover:text-white transition-colors">
                  <BookOpen className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-medium text-slate-900">Open Notes</div>
                  <div className="text-xs text-slate-500">Review and organize your thoughts</div>
                </div>
              </button>
              
              <button onClick={() => handleNavigate('/library')} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors text-left border border-transparent hover:border-slate-200 group">
                <div className="p-2 bg-green-100 text-green-600 rounded-md group-hover:bg-green-600 group-hover:text-white transition-colors">
                  <Bookmark className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-medium text-slate-900">View Library</div>
                  <div className="text-xs text-slate-500">Manage saved papers</div>
                </div>
              </button>
              
              <button onClick={() => handleNavigate('/literature-review')} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors text-left border border-transparent hover:border-slate-200 group">
                <div className="p-2 bg-rose-100 text-rose-600 rounded-md group-hover:bg-rose-600 group-hover:text-white transition-colors">
                  <FileText className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-medium text-slate-900">Generate Review</div>
                  <div className="text-xs text-slate-500">Synthesize your findings</div>
                </div>
              </button>
              
              <button onClick={() => handleNavigate('/xai')} className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50 transition-colors text-left border border-transparent hover:border-slate-200 group">
                <div className="p-2 bg-cyan-100 text-cyan-600 rounded-md group-hover:bg-cyan-600 group-hover:text-white transition-colors">
                  <Activity className="w-4 h-4" />
                </div>
                <div>
                  <div className="font-medium text-slate-900">Explainability</div>
                  <div className="text-xs text-slate-500">Deep dive into AI reasoning</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Timeline */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col h-[600px]">
          <h2 className="text-lg font-semibold text-slate-900 mb-6">Timeline</h2>
          <div className="flex-1 overflow-y-auto pr-2">
            {topic.timeline.length === 0 ? (
              <div className="text-sm text-slate-500 text-center py-10">No activities recorded yet.</div>
            ) : (
              <div className="space-y-6 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
                {topic.timeline.slice().reverse().map((event) => (
                  <div key={event.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div className="flex items-center justify-center w-5 h-5 rounded-full border border-white bg-slate-200 group-[.is-active]:bg-blue-500 text-slate-500 group-[.is-active]:text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                      <div className="w-1.5 h-1.5 rounded-full bg-white"></div>
                    </div>
                    <div className="w-[calc(100%-2rem)] md:w-[calc(50%-1.5rem)] p-3 rounded-lg border border-slate-200 bg-white shadow-sm">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-slate-900 text-sm capitalize">{event.type.replace('_', ' ')}</span>
                        <span className="text-xs text-slate-500">{formatDistanceToNow(new Date(event.timestamp))}</span>
                      </div>
                      <div className="text-slate-600 text-sm">{event.description}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
