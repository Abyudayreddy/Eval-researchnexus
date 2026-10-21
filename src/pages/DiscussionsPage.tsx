import { useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Panel, PanelGroup, PanelResizeHandle, ImperativePanelHandle } from 'react-resizable-panels';
import { 
  MessageSquare, Search, Filter, Plus, Hash, CheckCircle2, Bookmark, Pin, 
  Briefcase, Users, FileText, ChevronRight, X, Eye, 
  MoreHorizontal, ChevronDown, Share2, ThumbsUp, Zap, 
  LayoutList, Bot, ShieldCheck, HelpCircle, BookOpen
} from 'lucide-react';
import { cn } from '../utils/cn';

const mockDiscussions = [
  {
    id: '1',
    title: 'How to mitigate hallucinations in domain-specific RAG?',
    author: { name: 'Dr. Sarah Chen', role: 'Expert', avatar: 'S' },
    domain: 'Artificial Intelligence',
    project: 'Project Alpha',
    linkedPaper: 'Retrieval-Augmented Generation for NLP Tasks',
    type: 'Question',
    tags: ['RAG', 'Hallucination', 'LLMs'],
    replies: 12,
    views: 340,
    participants: 5,
    lastUpdated: '2 hours ago',
    status: 'Open',
    pinned: true,
  },
  {
    id: '2',
    title: 'Reviewing AlphaFold 3 capabilities in drug discovery pipelines',
    author: { name: 'Dr. James Wilson', role: 'Moderator', avatar: 'J' },
    domain: 'Healthcare',
    project: 'BioResearch Beta',
    linkedPaper: 'Highly accurate protein structure prediction',
    type: 'Paper Review',
    tags: ['AlphaFold', 'Proteins', 'Biotech'],
    replies: 8,
    views: 215,
    participants: 3,
    lastUpdated: '5 hours ago',
    status: 'Hot',
    pinned: false,
  },
  {
    id: '3',
    title: 'Discussion on methodology: Contrastive Learning vs Cross-Entropy',
    author: { name: 'Elena Rodriguez', role: 'Researcher', avatar: 'E' },
    domain: 'Artificial Intelligence',
    project: 'None',
    linkedPaper: 'Supervised Contrastive Learning',
    type: 'Methodology Discussion',
    tags: ['Contrastive', 'Loss', 'Vision'],
    replies: 24,
    views: 890,
    participants: 12,
    lastUpdated: '1 day ago',
    status: 'Resolved',
    pinned: false,
  }
];

const mockThread = [
  {
    id: 'c1',
    author: { name: 'Dr. Sarah Chen', role: 'Expert', avatar: 'S', time: '2 hours ago' },
    content: "I've been evaluating the latest hybrid RAG architectures (specifically combining BM25 with DPR) and noticing that while overall factual accuracy improves, hallucination rates on highly specialized medical vocabulary remain unacceptable (~15%). Has anyone successfully mitigated this without doing full continuous pre-training?",
    likes: 15,
    isAccepted: false,
    replies: [
      {
        id: 'r1',
        author: { name: 'David Kim', role: 'Researcher', avatar: 'D', time: '1 hour ago' },
        content: "We faced a similar issue in our genomics pipeline. We found that injecting a cross-encoder re-ranking step immediately after the BM25 retrieval drastically reduced hallucinations because the cross-encoder handles the specialized terminology much better than the bi-encoder dot product. Have you tried a cross-encoder approach?",
        likes: 8,
        isAccepted: true
      },
      {
        id: 'r2',
        author: { name: 'Dr. Sarah Chen', role: 'Expert', avatar: 'S', time: '45 mins ago' },
        content: "That's an interesting point. Did the cross-encoder introduce significant latency in your inference pipeline? We have a strict 500ms latency budget.",
        likes: 3,
        isAccepted: false
      }
    ]
  },
  {
    id: 'c2',
    author: { name: 'Elena Rodriguez', role: 'Researcher', avatar: 'E', time: '30 mins ago' },
    content: "Another approach, as highlighted in the latest Lewis et al. paper, is to expand the queries synthetically before retrieval. We use a lightweight LLM to generate synonym queries for the medical terms, run retrieval on all of them, and then deduplicate.",
    likes: 5,
    isAccepted: false,
    replies: []
  }
];

export default function DiscussionsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [isLeftCollapsed, setIsLeftCollapsed] = useState(false);
  const [isRightCollapsed, setIsRightCollapsed] = useState(false);
  const [rightTab, setRightTab] = useState<'resources' | 'participants' | 'activity' | 'files'>('resources');
  const [showCreateModal, setShowCreateModal] = useState(false);

  const leftPanelRef = useRef<ImperativePanelHandle>(null);
  const rightPanelRef = useRef<ImperativePanelHandle>(null);

  const activeDiscussion = id ? mockDiscussions.find(d => d.id === id) : null;

  return (
    <div className="absolute inset-0 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col font-sans">
      
      {/* Floating Quick Collaborate Button */}
      <div className="absolute bottom-6 right-6 z-50 group">
        <button 
          onClick={() => setShowCreateModal(true)}
          className="p-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-full shadow-lg transition-transform hover:scale-105 flex items-center justify-center"
          title="Quick Collaborate"
        >
          <Plus className="w-6 h-6" />
        </button>
      </div>

      {/* CREATE MODAL */}
      {showCreateModal && (
        <div className="absolute inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white w-full max-w-2xl rounded-2xl shadow-xl flex flex-col max-h-full">
            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
              <h2 className="text-xl font-black text-slate-900 flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-emerald-600" /> Start a Discussion
              </h2>
              <button onClick={() => setShowCreateModal(false)} className="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"><X className="w-5 h-5" /></button>
            </div>
            <div className="p-6 overflow-y-auto space-y-5 flex-1">
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Discussion Title</label>
                <input type="text" placeholder="e.g., Thoughts on the latest methodology in..." className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500" />
              </div>
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Details / Context</label>
                <textarea rows={4} placeholder="Provide context, ask a question, or share your insights..." className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-800 resize-none focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Discussion Type</label>
                  <select className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:border-emerald-500">
                    <option>Question</option>
                    <option>Paper Review</option>
                    <option>Methodology Discussion</option>
                    <option>General</option>
                  </select>
                </div>
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Visibility</label>
                  <select className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:border-emerald-500">
                    <option>Public (All Researchers)</option>
                    <option>Private (Invite Only)</option>
                    <option>Project Members Only</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Attach Resources</label>
                <div className="flex gap-2">
                  <button className="px-3 py-2 bg-white border border-slate-200 rounded-lg text-[11px] font-bold text-slate-600 hover:border-blue-400 hover:text-blue-600 flex items-center gap-1.5 transition-colors">
                    <BookOpen className="w-3.5 h-3.5" /> Paper
                  </button>
                  <button className="px-3 py-2 bg-white border border-slate-200 rounded-lg text-[11px] font-bold text-slate-600 hover:border-purple-400 hover:text-purple-600 flex items-center gap-1.5 transition-colors">
                    <LayoutList className="w-3.5 h-3.5" /> Lit Review
                  </button>
                  <button className="px-3 py-2 bg-white border border-slate-200 rounded-lg text-[11px] font-bold text-slate-600 hover:border-amber-400 hover:text-amber-600 flex items-center gap-1.5 transition-colors">
                    <FileText className="w-3.5 h-3.5" /> Note
                  </button>
                </div>
              </div>
            </div>
            <div className="p-6 border-t border-slate-100 flex justify-end gap-3 bg-slate-50 rounded-b-2xl">
              <button onClick={() => setShowCreateModal(false)} className="px-6 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-xl text-sm font-bold hover:bg-slate-50 transition-colors">Cancel</button>
              <button onClick={() => setShowCreateModal(false)} className="px-6 py-2.5 bg-emerald-600 text-white rounded-xl text-sm font-bold hover:bg-emerald-700 transition-colors flex items-center gap-2 shadow-sm">
                Start Discussion <Zap className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TOP HEADER */}
      <header className="px-6 py-4 border-b border-slate-100 flex flex-col md:flex-row md:items-center justify-between gap-4 shrink-0 bg-white">
        <div>
          <h1 className="text-xl font-black text-slate-900 flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-emerald-600" /> Research Discussions
          </h1>
          <p className="text-xs font-medium text-slate-500 mt-0.5">Collaborate, ask questions and exchange research insights.</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="px-3 py-1.5 text-xs font-bold text-slate-600 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm">
            <Search className="w-3.5 h-3.5" /> Search
          </button>
          <button className="px-3 py-1.5 text-xs font-bold text-slate-600 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm">
            <Filter className="w-3.5 h-3.5" /> Filter
          </button>
          <div className="w-px h-4 bg-slate-200 mx-1"></div>
          <button onClick={() => setShowCreateModal(true)} className="px-4 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm">
            <Plus className="w-3.5 h-3.5" /> New Discussion
          </button>
        </div>
      </header>

      <PanelGroup direction="horizontal" className="w-full flex-1">
        
        {/* ==================== LEFT PANEL: CATEGORIES ==================== */}
        <Panel 
          ref={leftPanelRef}
          defaultSize={20} 
          minSize={15} 
          maxSize={25} 
          collapsible 
          collapsedSize={4}
          onCollapse={() => setIsLeftCollapsed(true)}
          onExpand={() => setIsLeftCollapsed(false)}
          className={cn("bg-[#F8FAFC] flex flex-col h-full transition-all duration-300", !isLeftCollapsed && "border-r border-slate-200")}
        >
          {isLeftCollapsed ? (
            <div className="flex flex-col items-center py-4 space-y-4">
              <button onClick={() => leftPanelRef.current?.expand()} className="p-2 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors" title="Expand Categories">
                <Hash className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <>
              <div className="h-12 flex items-center justify-between px-5 shrink-0 border-b border-slate-100">
                <span className="font-bold text-slate-800 text-xs flex items-center gap-2">
                  <Hash className="w-3.5 h-3.5 text-emerald-600" /> Categories
                </span>
                <button onClick={() => leftPanelRef.current?.collapse()} className="text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-md hover:bg-slate-200">
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
              
              <div className="flex-1 overflow-y-auto p-3 scrollbar-hide space-y-6">
                
                <div className="space-y-1">
                  <button onClick={() => navigate('/discussions')} className="w-full flex items-center justify-between px-3 py-2 bg-emerald-50 text-emerald-700 rounded-lg text-xs font-bold transition-colors">
                    <span className="flex items-center gap-2"><MessageSquare className="w-3.5 h-3.5" /> All Discussions</span>
                  </button>
                  <button className="w-full flex items-center justify-between px-3 py-2 text-slate-600 hover:bg-slate-100 hover:text-slate-900 rounded-lg text-xs font-medium transition-colors">
                    <span className="flex items-center gap-2"><Users className="w-3.5 h-3.5 text-slate-400" /> My Discussions</span>
                  </button>
                  <button className="w-full flex items-center justify-between px-3 py-2 text-slate-600 hover:bg-slate-100 hover:text-slate-900 rounded-lg text-xs font-medium transition-colors">
                    <span className="flex items-center gap-2"><Bookmark className="w-3.5 h-3.5 text-blue-500" /> Bookmarked</span>
                  </button>
                  <button className="w-full flex items-center justify-between px-3 py-2 text-slate-600 hover:bg-slate-100 hover:text-slate-900 rounded-lg text-xs font-medium transition-colors">
                    <span className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Resolved</span>
                  </button>
                </div>

                <div>
                  <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 mb-2 flex items-center justify-between">
                    Research Domains <ChevronDown className="w-3 h-3" />
                  </h4>
                  <div className="space-y-1">
                    {['Artificial Intelligence', 'Healthcare', 'Data Science', 'Space Science'].map(domain => (
                      <button key={domain} className="w-full flex items-center gap-2 px-3 py-1.5 text-slate-600 hover:bg-slate-100 hover:text-slate-900 rounded-lg text-[11px] font-semibold transition-colors">
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-300"></span> {domain}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-3 mb-2 flex items-center justify-between">
                    Projects <ChevronDown className="w-3 h-3" />
                  </h4>
                  <div className="space-y-1">
                    {['Project Alpha', 'BioResearch Beta'].map(proj => (
                      <button key={proj} className="w-full flex items-center gap-2 px-3 py-1.5 text-slate-600 hover:bg-slate-100 hover:text-slate-900 rounded-lg text-[11px] font-semibold transition-colors">
                        <Briefcase className="w-3 h-3 text-slate-400" /> {proj}
                      </button>
                    ))}
                  </div>
                </div>

              </div>
            </>
          )}
        </Panel>
        
        <PanelResizeHandle className="w-[1px] bg-slate-200 hover:bg-emerald-500 transition-colors cursor-col-resize z-10" />
        
        {/* ==================== CENTER PANEL: FEED OR DETAIL ==================== */}
        <Panel defaultSize={55} className="flex flex-col bg-white h-full relative z-0">
          
          <div className="flex-1 overflow-y-auto scrollbar-hide bg-slate-50/50">
            {!activeDiscussion ? (
              
              <div className="max-w-4xl mx-auto p-6 md:p-8 space-y-8 animate-in fade-in duration-300">
                
                {/* BONUS: Research Collaboration Dashboard */}
                <div className="bg-slate-900 text-white p-6 rounded-2xl shadow-md border border-slate-800">
                  <h3 className="text-[10px] font-bold text-emerald-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                    <Users className="w-4 h-4" /> Collaboration Overview
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div>
                      <span className="block text-2xl font-black text-white mb-1">12</span>
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Active Discussions</span>
                    </div>
                    <div>
                      <span className="block text-2xl font-black text-amber-400 mb-1">5</span>
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Open Questions</span>
                    </div>
                    <div>
                      <span className="block text-2xl font-black text-emerald-400 mb-1">8</span>
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Resolved</span>
                    </div>
                    <div>
                      <span className="block text-2xl font-black text-blue-400 mb-1">24</span>
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Collaborators</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  {mockDiscussions.map((discussion) => (
                    <div 
                      key={discussion.id} 
                      onClick={() => navigate(`/discussions/${discussion.id}`)}
                      className="bg-white border border-slate-200 p-5 rounded-2xl shadow-sm hover:shadow-md hover:border-emerald-300 transition-all cursor-pointer group"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1 pr-4">
                          <div className="flex items-center gap-2 mb-2">
                            {discussion.pinned && <span className="bg-amber-100 text-amber-700 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest flex items-center gap-1"><Pin className="w-2.5 h-2.5" /> Pinned</span>}
                            {discussion.status === 'Resolved' && <span className="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest flex items-center gap-1"><CheckCircle2 className="w-2.5 h-2.5" /> Resolved</span>}
                            {discussion.status === 'Hot' && <span className="bg-rose-100 text-rose-700 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest flex items-center gap-1"><Zap className="w-2.5 h-2.5" /> Hot</span>}
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{discussion.type}</span>
                          </div>
                          <h3 className="text-[17px] font-bold text-slate-900 leading-snug group-hover:text-emerald-700 transition-colors">
                            {discussion.title}
                          </h3>
                        </div>
                        <div className="flex flex-col items-end gap-2 shrink-0">
                          <div className="flex items-center gap-3 text-slate-400">
                            <span className="flex items-center gap-1 text-[11px] font-bold"><MessageSquare className="w-3.5 h-3.5" /> {discussion.replies}</span>
                            <span className="flex items-center gap-1 text-[11px] font-bold"><Eye className="w-3.5 h-3.5" /> {discussion.views}</span>
                          </div>
                          <span className="text-[10px] font-medium text-slate-400">{discussion.lastUpdated}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-[10px] font-bold shrink-0">
                          {discussion.author.avatar}
                        </div>
                        <div className="text-xs font-semibold text-slate-700">
                          {discussion.author.name} <span className="text-[10px] text-slate-400 ml-1 px-1.5 py-0.5 bg-slate-100 rounded">{discussion.author.role}</span>
                        </div>
                      </div>

                      <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold bg-slate-100 text-slate-600 px-2 py-1 rounded uppercase tracking-wider">{discussion.domain}</span>
                          {discussion.project !== 'None' && <span className="text-[10px] font-bold bg-blue-50 text-blue-600 px-2 py-1 rounded uppercase tracking-wider">{discussion.project}</span>}
                        </div>
                        <div className="flex gap-1">
                          {discussion.tags.map(tag => (
                            <span key={tag} className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded">#{tag}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            ) : (

              // DISCUSSION DETAIL PAGE
              <div className="flex flex-col h-full animate-in fade-in duration-300">
                <div className="p-6 md:p-8 border-b border-slate-200 bg-white sticky top-0 z-10 shadow-sm">
                  <button onClick={() => navigate('/discussions')} className="text-[11px] font-bold text-slate-400 uppercase tracking-widest hover:text-emerald-600 flex items-center gap-1 mb-4 transition-colors">
                    <ChevronRight className="w-3 h-3 rotate-180" /> Back to Feed
                  </button>
                  
                  <div className="flex items-center gap-2 mb-3">
                    <span className="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest">{activeDiscussion.type}</span>
                    {activeDiscussion.status === 'Resolved' && <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-widest flex items-center gap-1"><CheckCircle2 className="w-2.5 h-2.5" /> Resolved</span>}
                  </div>
                  
                  <h1 className="text-2xl font-black text-slate-900 leading-tight mb-4">
                    {activeDiscussion.title}
                  </h1>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-xs font-bold shrink-0">
                        {activeDiscussion.author.avatar}
                      </div>
                      <div>
                        <div className="text-sm font-bold text-slate-800">
                          {activeDiscussion.author.name} <span className="text-[10px] text-indigo-600 ml-1 px-1.5 py-0.5 bg-indigo-50 border border-indigo-100 rounded">{activeDiscussion.author.role}</span>
                        </div>
                        <div className="text-[10px] font-medium text-slate-400 mt-0.5">Posted {activeDiscussion.lastUpdated}</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button className="px-3 py-1.5 text-xs font-bold text-slate-600 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm">
                        <Share2 className="w-3.5 h-3.5" /> Share
                      </button>
                      <button className="px-3 py-1.5 text-xs font-bold text-slate-600 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm">
                        <Bookmark className="w-3.5 h-3.5" /> Save
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex-1 p-6 md:p-8 space-y-6 bg-slate-50/50">
                  
                  {/* Thread Comments */}
                  {mockThread.map((comment) => (
                    <div key={comment.id} className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                      <div className="p-5 flex items-start gap-4">
                        <div className="w-8 h-8 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0">
                          {comment.author.avatar}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-slate-800">{comment.author.name}</span>
                              <span className="text-[10px] font-bold text-slate-400">• {comment.author.time}</span>
                            </div>
                            <button className="text-slate-400 hover:text-slate-700"><MoreHorizontal className="w-4 h-4" /></button>
                          </div>
                          <p className="text-sm text-slate-700 leading-relaxed font-medium mb-4">
                            {comment.content}
                          </p>
                          <div className="flex items-center gap-4">
                            <button className="flex items-center gap-1.5 text-[11px] font-bold text-slate-500 hover:text-emerald-600 transition-colors">
                              <ThumbsUp className="w-3.5 h-3.5" /> {comment.likes}
                            </button>
                            <button className="flex items-center gap-1.5 text-[11px] font-bold text-slate-500 hover:text-blue-600 transition-colors">
                              <MessageSquare className="w-3.5 h-3.5" /> Reply
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Nested Replies */}
                      {comment.replies.length > 0 && (
                        <div className="bg-slate-50 border-t border-slate-100 p-5 pl-14 space-y-5">
                          {comment.replies.map(reply => (
                            <div key={reply.id} className={cn("relative", reply.isAccepted && "bg-emerald-50/50 p-3 -m-3 rounded-xl border border-emerald-100")}>
                              {reply.isAccepted && (
                                <div className="absolute -left-10 top-0 text-emerald-500" title="Marked as Answer">
                                  <ShieldCheck className="w-5 h-5" />
                                </div>
                              )}
                              <div className="flex items-start gap-3">
                                <div className="w-6 h-6 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center text-[10px] font-bold shrink-0">
                                  {reply.author.avatar}
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-1">
                                    <span className="text-[11px] font-bold text-slate-800">{reply.author.name}</span>
                                    <span className="text-[9px] font-bold text-slate-400">• {reply.author.time}</span>
                                  </div>
                                  <p className="text-[13px] text-slate-700 leading-relaxed font-medium mb-2">
                                    {reply.content}
                                  </p>
                                  <div className="flex items-center gap-4">
                                    <button className="flex items-center gap-1 text-[10px] font-bold text-slate-500 hover:text-emerald-600 transition-colors">
                                      <ThumbsUp className="w-3 h-3" /> {reply.likes}
                                    </button>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                  
                  {/* Reply Input */}
                  <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-start gap-4">
                    <div className="w-8 h-8 rounded-full bg-emerald-500 text-white flex items-center justify-center text-xs font-bold shrink-0">
                      A
                    </div>
                    <div className="flex-1 border-2 border-slate-100 rounded-xl p-2 focus-within:border-emerald-400 transition-colors">
                      <textarea 
                        placeholder="Write a reply... (Markdown supported)" 
                        className="w-full bg-transparent text-sm font-medium text-slate-800 resize-none outline-none min-h-[60px] p-2"
                      />
                      <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                        <div className="flex items-center gap-1">
                          <button className="p-1.5 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-md transition-colors"><HelpCircle className="w-4 h-4" /></button>
                          <button className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"><FileText className="w-4 h-4" /></button>
                        </div>
                        <button className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition-colors shadow-sm">
                          Post Reply
                        </button>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            )}
          </div>

        </Panel>

        <PanelResizeHandle className="w-[1px] bg-slate-200 hover:bg-emerald-500 transition-colors cursor-col-resize z-10" />

        {/* ==================== RIGHT PANEL: DETAILS ==================== */}
        <Panel 
          ref={rightPanelRef}
          defaultSize={25} 
          minSize={20} 
          maxSize={35} 
          collapsible
          collapsedSize={4}
          onCollapse={() => setIsRightCollapsed(true)}
          onExpand={() => setIsRightCollapsed(false)}
          className={cn("bg-[#FBFDFB] flex flex-col h-full transition-all duration-300", !isRightCollapsed && "border-l border-slate-200")}
        >
          {isRightCollapsed ? (
            <div className="flex flex-col items-center py-4 space-y-4">
              <button onClick={() => rightPanelRef.current?.expand()} className="p-2 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors" title="Linked Resources">
                <FileText className="w-5 h-5" />
              </button>
              <button onClick={() => rightPanelRef.current?.expand()} className="p-2 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors" title="Participants">
                <Users className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <>
              {/* Tabs */}
              <div className="h-12 flex items-center px-2 border-b border-slate-200 shrink-0 overflow-x-auto scrollbar-hide gap-1 bg-white justify-between">
                <div className="flex items-center gap-1">
                  {[
                    { id: 'resources', label: 'RESOURCES' },
                    { id: 'participants', label: 'PEOPLE' },
                    { id: 'activity', label: 'ACTIVITY' },
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setRightTab(tab.id as 'resources' | 'participants' | 'activity' | 'files')}
                      className={cn(
                        "px-3 py-2 text-[9px] sm:text-[10px] font-bold tracking-widest whitespace-nowrap transition-colors",
                        rightTab === tab.id
                          ? "text-emerald-600 border-b-2 border-emerald-600"
                          : "text-slate-400 hover:text-slate-700"
                      )}
                      style={{ marginBottom: rightTab === tab.id ? '-1px' : '0' }}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>
                <button onClick={() => rightPanelRef.current?.collapse()} className="p-1.5 text-slate-400 hover:text-slate-600 transition-colors mr-1 rounded-md hover:bg-slate-100">
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-5 scrollbar-hide">
                
                {rightTab === 'resources' && (
                  <div className="space-y-6 animate-in fade-in duration-300">
                    
                    {activeDiscussion && (
                      <div>
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-3">Linked Paper</span>
                        <div className="bg-white border border-slate-200 p-3 rounded-xl shadow-sm hover:border-blue-300 cursor-pointer transition-colors relative">
                          <div className="absolute top-0 right-0 w-8 h-8 bg-blue-50 rounded-bl-xl rounded-tr-xl flex items-center justify-center">
                            <BookOpen className="w-4 h-4 text-blue-500" />
                          </div>
                          <h5 className="text-[11px] font-bold text-slate-800 line-clamp-2 pr-6">{activeDiscussion.linkedPaper}</h5>
                        </div>
                      </div>
                    )}

                    <div>
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-3">Linked AI Context</span>
                      <div className="bg-emerald-50 border border-emerald-100 p-3 rounded-xl cursor-pointer hover:border-emerald-300 transition-colors flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center shrink-0 shadow-sm text-emerald-600">
                          <Bot className="w-4 h-4" />
                        </div>
                        <div>
                          <h5 className="text-[11px] font-bold text-slate-800">RAG Limitations Session</h5>
                          <p className="text-[9px] font-medium text-slate-500 mt-0.5">Connected by Dr. Sarah Chen</p>
                        </div>
                      </div>
                    </div>

                  </div>
                )}
                
                {rightTab === 'participants' && (
                  <div className="space-y-4 animate-in fade-in duration-300">
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-3">5 Active Participants</span>
                    
                    <div className="space-y-3">
                      {[
                        { name: 'Dr. Sarah Chen', role: 'Expert', avatar: 'S', active: true },
                        { name: 'David Kim', role: 'Researcher', avatar: 'D', active: true },
                        { name: 'Elena Rodriguez', role: 'Researcher', avatar: 'E', active: false },
                      ].map((p, i) => (
                        <div key={i} className="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg transition-colors cursor-pointer">
                          <div className="relative">
                            <div className="w-8 h-8 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center text-xs font-bold">
                              {p.avatar}
                            </div>
                            {p.active && <div className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-500 border-2 border-white rounded-full"></div>}
                          </div>
                          <div>
                            <p className="text-xs font-bold text-slate-800">{p.name}</p>
                            <p className="text-[10px] font-medium text-slate-400">{p.role}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {rightTab === 'activity' && (
                  <div className="space-y-6 animate-in fade-in duration-300">
                    <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2.5 before:-translate-x-px before:h-full before:w-0.5 before:bg-slate-200">
                      <div className="relative flex gap-4">
                        <div className="w-5 h-5 rounded-full bg-blue-100 border-2 border-white text-blue-500 flex items-center justify-center shrink-0 z-10 shadow-sm mt-1">
                          <MessageSquare className="w-2.5 h-2.5" />
                        </div>
                        <div>
                          <p className="text-xs font-semibold text-slate-700">David Kim replied</p>
                          <p className="text-[10px] text-slate-400">1 hour ago</p>
                        </div>
                      </div>
                      <div className="relative flex gap-4">
                        <div className="w-5 h-5 rounded-full bg-emerald-100 border-2 border-white text-emerald-500 flex items-center justify-center shrink-0 z-10 shadow-sm mt-1">
                          <ShieldCheck className="w-2.5 h-2.5" />
                        </div>
                        <div>
                          <p className="text-xs font-semibold text-slate-700">Marked reply as Answer</p>
                          <p className="text-[10px] text-slate-400">1 hour ago</p>
                        </div>
                      </div>
                      <div className="relative flex gap-4">
                        <div className="w-5 h-5 rounded-full bg-amber-100 border-2 border-white text-amber-500 flex items-center justify-center shrink-0 z-10 shadow-sm mt-1">
                          <Pin className="w-2.5 h-2.5" />
                        </div>
                        <div>
                          <p className="text-xs font-semibold text-slate-700">Pinned discussion</p>
                          <p className="text-[10px] text-slate-400">2 hours ago</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

              </div>
            </>
          )}
        </Panel>

      </PanelGroup>

    </div>
  );
}
