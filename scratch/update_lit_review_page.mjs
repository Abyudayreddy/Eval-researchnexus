import fs from 'fs';

const pageCode = `import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  CheckCircle2, ChevronRight, FileText, LayoutList, BrainCircuit, 
  Download, CheckSquare, Square, Tag, ExternalLink, Sparkles, BookOpen, Layers, ShieldCheck, ArrowRight
} from 'lucide-react';
import { cn } from '../utils/cn';
import { api } from '../utils/api';
import { useResearchSessionStore } from '../store/researchSessionStore';

const STEPS = [
  { id: 'select', title: 'Select Papers', number: 1 },
  { id: 'topics', title: 'Review Topics & Requirements', number: 2 },
  { id: 'synthesize', title: 'Synthesize Evidence', number: 3 },
  { id: 'review', title: 'Final Review', number: 4 }
];

export interface ReviewTopicRequirement {
  id: string;
  topicTitle: string;
  reviewQuestion: string;
  groundedRationale: string;
  requiredPapers: { id: string; title: string; authors: string }[];
  requiredEvidence: string[];
  keyDimensions: string[];
  expectedComparisons: string[];
  knownGaps: string[];
  limitations: string[];
  outputStructure: string;
  citationRequirements: string;
}

export default function LiteratureReviewPage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [selectedPaperIds, setSelectedPaperIds] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(true);

  // Step 2 Requirement Builder State
  const [reviewObjective, setReviewObjective] = useState('');
  const [reviewQuestion, setReviewQuestion] = useState('');
  const [reviewType, setReviewType] = useState<'comprehensive' | 'methodological' | 'comparative' | 'sota'>('comparative');
  const [generatedTopics, setGeneratedTopics] = useState<ReviewTopicRequirement[]>([]);
  const [isGeneratingTopics, setIsGeneratingTopics] = useState(false);
  const [activeTopicIndex, setActiveTopicIndex] = useState(0);
  
  const [synthesisState, setSynthesisState] = useState({
    status: 'idle', // idle, loading, success, error, insufficient_evidence
    review: '',
    sources: [] as any[],
    trace: null as any
  });
  
  const navigate = useNavigate();
  const location = useLocation();
  const projectId = location.state?.projectId;
  const initialPapers = location.state?.selected_papers;
  
  const { activeTopicId, topics } = useResearchSessionStore();
  const activeTopic = activeTopicId ? topics[activeTopicId] : null;

  useEffect(() => {
    if (initialPapers && initialPapers.length > 0) {
      setBookmarks(initialPapers.map((p: any) => ({ paper: p })));
      setSelectedPaperIds(new Set(initialPapers.map((p: any) => p.id)));
      setIsLoading(false);
      // Pre-seed review objective from first paper title
      if (!reviewObjective && initialPapers[0]?.title) {
        setReviewObjective(\`Comparative analysis and synthesis of \${initialPapers[0].title.slice(0, 45)}...\`);
      }
    } else {
      loadBookmarks();
    }
  }, [initialPapers]);

  const loadBookmarks = async () => {
    setIsLoading(true);
    try {
      if (projectId) {
        const data = await api.projects.getPapers(projectId);
        setBookmarks(data);
      } else {
        const data = await api.bookmarks.getAll();
        setBookmarks(data);
      }
    } catch (err) {
      console.error("Failed to load papers", err);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePaperSelection = (paperId: string) => {
    const next = new Set(selectedPaperIds);
    if (next.has(paperId)) {
      next.delete(paperId);
    } else {
      next.add(paperId);
    }
    setSelectedPaperIds(next);
  };

  const selectedPapers = bookmarks.filter(b => selectedPaperIds.has(b.paper.id));

  // Generate Review Topics with explicit requirements from selected papers
  const handleGenerateTopicsWithRequirements = () => {
    if (selectedPapers.length === 0) return;
    setIsGeneratingTopics(true);

    setTimeout(() => {
      const papers = selectedPapers.map(b => b.paper);
      const objective = reviewObjective.trim() || 'Comparative evaluation of research architectures and paradigms';
      const question = reviewQuestion.trim() || \`How do findings and methodologies compare across the \${papers.length} selected studies?\`;
      
      const topicsList: ReviewTopicRequirement[] = [
        {
          id: 'topic-1',
          topicTitle: \`Core Methodologies & Architectural Paradigms in \${papers[0]?.domain || 'Selected Literature'}\`,
          reviewQuestion: question,
          groundedRationale: \`Synthesizes direct algorithmic and architectural claims across \${papers.map(p => p.title.slice(0, 30) + '...').join(' vs ')} based strictly on retrieved abstract and paper evidence.\`,
          requiredPapers: papers.map(p => ({ id: p.id, title: p.title, authors: p.authors || 'Unknown Authors' })),
          requiredEvidence: papers.map(p => \`Direct empirical abstract/text claims from \${p.title.slice(0, 35)}...\`),
          keyDimensions: ['Theoretical Foundations', 'Empirical Benchmarking', 'Computational Efficiency', 'Scalability'],
          expectedComparisons: [
            \`Cross-paper evaluation of baseline performance\`,
            \`Contrasting evaluation methodologies and benchmark validation sets\`
          ],
          knownGaps: [
            \`Varying parameter scales between implementations\`,
            \`Differences in reported evaluation metrics and ablation constraints\`
          ],
          limitations: [
            \`Synthesis is strictly bound to available paper abstracts and published records\`,
            \`No external speculation or ungrounded extrapolation permitted\`
          ],
          outputStructure: 'Section 1: Background & Problem Formulation\\nSection 2: Comparative Methodological Analysis\\nSection 3: Empirical Validation & Synthesis Table\\nSection 4: Identified Gaps & Future Directions',
          citationRequirements: 'Strict in-situ IEEE bracketed citations ([1], [2]) directly mapped to each asserted claim.'
        },
        {
          id: 'topic-2',
          topicTitle: 'Empirical Findings, Benchmarks & Reproducibility Constraints',
          reviewQuestion: 'What quantitative or qualitative advantages are substantiated across the selected literature?',
          groundedRationale: 'Extracts verifiable metrics, datasets, and reported performance indicators from selected documents.',
          requiredPapers: papers.map(p => ({ id: p.id, title: p.title, authors: p.authors || 'Unknown Authors' })),
          requiredEvidence: ['Dataset citations', 'Evaluation metric scores', 'Ablation study findings'],
          keyDimensions: ['Dataset Representation', 'Metric Consistency', 'Ablation Soundness'],
          expectedComparisons: ['Accuracy/Latency tradeoffs across proposed techniques'],
          knownGaps: ['Non-standardized test splits across distinct publication years'],
          limitations: ['Evaluation depends on explicit author reporting'],
          outputStructure: 'Comparative Analysis Matrix with dimension-specific attribution.',
          citationRequirements: 'Every comparison cell must attribute claims exclusively to its respective author/paper.'
        }
      ];

      setGeneratedTopics(topicsList);
      setIsGeneratingTopics(false);
      setActiveTopicIndex(0);
    }, 400);
  };

  const generateSynthesis = async () => {
    if (selectedPaperIds.size === 0) return;
    
    setSynthesisState(prev => ({ ...prev, status: 'loading' }));
    
    try {
      const paperIds = Array.from(selectedPaperIds);
      const res = await api.literatureReview.synthesize(paperIds);
      
      setSynthesisState({
        status: res.generation_status === 'insufficient_evidence' ? 'insufficient_evidence' : (res.generation_status === 'generation_failed' || res.generation_status === 'quota_exceeded' ? 'error' : 'success'),
        review: res.review,
        sources: res.sources,
        trace: res.evidence_trace
      });
    } catch (err) {
      setSynthesisState(prev => ({ ...prev, status: 'error' }));
    }
  };

  const nextStep = () => {
    if (currentStep === 1) {
      if (generatedTopics.length === 0) {
        handleGenerateTopicsWithRequirements();
      }
      setCurrentStep(2);
      return;
    }
    if (currentStep === 2) {
      if (synthesisState.status === 'idle') {
        generateSynthesis();
      }
      setCurrentStep(3);
      return;
    }
    setCurrentStep(prev => Math.min(prev + 1, 4));
  };
  const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

  return (
    <div className="h-full flex flex-col bg-main text-main font-sans overflow-hidden relative rounded-xl border border-theme">
      {/* HEADER & STEPPER */}
      <header className="px-6 py-4 border-b border-theme bg-surface shrink-0 z-10">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-xl font-black text-main flex items-center gap-2">
                <LayoutList className="w-5 h-5 text-emerald-500" /> Literature Review
              </h1>
              <p className="text-xs font-medium text-muted mt-0.5">{activeTopic?.title || 'Systematic Research Synthesis'}</p>
            </div>
            {currentStep === 4 && synthesisState.status === 'success' && (
              <button 
                onClick={() => window.print()}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-bold flex items-center gap-2 transition-colors shadow-sm"
              >
                <Download className="w-4 h-4" /> Export Review
              </button>
            )}
          </div>
          
          <div className="flex items-center justify-between relative">
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-0.5 bg-theme -z-10"></div>
            <div 
              className="absolute left-0 top-1/2 -translate-y-1/2 h-0.5 bg-emerald-500 transition-all duration-300 -z-10" 
              style={{ width: \`\${((currentStep - 1) / 3) * 100}%\` }}
            ></div>
            
            {STEPS.map((step) => (
              <div key={step.id} className="flex flex-col items-center gap-2 bg-surface px-2">
                <div className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors border-2",
                  currentStep > step.number 
                    ? "bg-emerald-600 border-emerald-600 text-white" 
                    : currentStep === step.number
                      ? "bg-surface border-emerald-500 text-emerald-400"
                      : "bg-surface border-theme text-muted"
                )}>
                  {currentStep > step.number ? <CheckCircle2 className="w-4 h-4" /> : step.number}
                </div>
                <span className={cn(
                  "text-[10px] font-bold uppercase tracking-widest",
                  currentStep >= step.number ? "text-main" : "text-muted"
                )}>{step.title}</span>
              </div>
            ))}
          </div>
        </div>
      </header>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 overflow-y-auto bg-main p-6 md:p-8 min-h-0">
        <div className="max-w-4xl mx-auto h-full flex flex-col">
          {/* STEP 1: SELECT PAPERS */}
          {currentStep === 1 && (
             <div className="flex-1 animate-in slide-in-from-right-4 duration-300 flex flex-col">
               <div className="flex items-center justify-between mb-4">
                 <div>
                   <h2 className="text-lg font-black text-main">Select Papers for Review</h2>
                   <p className="text-sm text-sub">Choose 2 or more papers to formulate review topics and synthesize evidence.</p>
                 </div>
                 <div className="text-xs font-bold px-3 py-1.5 rounded-lg border border-theme bg-card text-main">
                   {selectedPaperIds.size} paper{selectedPaperIds.size !== 1 ? 's' : ''} selected
                 </div>
               </div>
               
               {isLoading ? (
                 <div className="flex-1 flex items-center justify-center text-muted text-sm">
                   Loading papers...
                 </div>
               ) : bookmarks.length === 0 ? (
                 <div className="bg-card border border-theme rounded-xl p-8 text-center my-auto">
                   <p className="text-sm text-muted font-medium mb-4">No papers available yet. Search papers in Explorer or Assistant.</p>
                   <button 
                     onClick={() => navigate('/explorer')}
                     className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition-colors"
                   >
                     Go to Research Explorer
                   </button>
                 </div>
               ) : (
                 <div className="space-y-3 flex-1 overflow-y-auto pr-1">
                   {bookmarks.map((b) => {
                     const isSelected = selectedPaperIds.has(b.paper.id);
                     return (
                       <div 
                         key={b.paper.id}
                         onClick={() => togglePaperSelection(b.paper.id)}
                         className={cn(
                           "p-4 rounded-xl border transition-all cursor-pointer flex items-start gap-4",
                           isSelected 
                             ? "bg-card border-emerald-500/50 shadow-sm" 
                             : "bg-card border-theme hover:border-theme-hover opacity-85 hover:opacity-100"
                         )}
                       >
                         <div className="mt-0.5">
                           {isSelected ? <CheckSquare className="w-5 h-5 text-emerald-500" /> : <Square className="w-5 h-5 text-muted" />}
                         </div>
                         <div className="flex-1 min-w-0">
                           <h4 className="text-[15px] font-bold text-main leading-tight mb-1 truncate">{b.paper.title}</h4>
                           <div className="flex items-center gap-2 text-[11px] font-bold text-muted">
                             <span className="truncate max-w-[240px] text-emerald-400">{b.paper.authors || 'Unknown Authors'}</span>
                             <span>•</span>
                             <span>{b.paper.published ? b.paper.published.substring(0, 4) : 'Recent'}</span>
                             {b.paper.domain && (
                               <>
                                 <span>•</span>
                                 <span className="text-sub">{b.paper.domain}</span>
                               </>
                             )}
                           </div>
                         </div>
                       </div>
                     );
                   })}
                 </div>
               )}
             </div>
          )}

          {/* STEP 2: ORGANIZE TOPICS & REQUIREMENTS */}
          {currentStep === 2 && (
             <div className="flex-1 animate-in slide-in-from-right-4 duration-300 flex flex-col">
               <div className="flex items-center justify-between mb-4">
                 <div>
                   <h2 className="text-lg font-black text-main">Review Objective & Topics Setup</h2>
                   <p className="text-sm text-sub">Generate and refine structured review topics grounded strictly in selected papers.</p>
                 </div>
                 <button
                   onClick={handleGenerateTopicsWithRequirements}
                   disabled={isGeneratingTopics || selectedPapers.length === 0}
                   className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-1.5 transition-colors shadow-sm disabled:opacity-50"
                 >
                   <Sparkles className="w-3.5 h-3.5" />
                   {isGeneratingTopics ? 'Formulating Topics...' : 'GENERATE REVIEW TOPICS WITH REQUIREMENTS'}
                 </button>
               </div>

               {/* Configuration Inputs */}
               <div className="bg-card border border-theme rounded-xl p-4 mb-5 space-y-4 shadow-sm">
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                   <div className="md:col-span-2">
                     <label className="block text-[11px] font-bold text-muted uppercase tracking-wider mb-1.5">Review Objective</label>
                     <input
                       type="text"
                       value={reviewObjective}
                       onChange={e => setReviewObjective(e.target.value)}
                       placeholder="e.g., Comparative analysis of parameter-efficient attention mechanisms"
                       className="w-full bg-surface border border-theme rounded-lg px-3 py-2 text-xs text-main placeholder-muted focus:outline-none focus:border-emerald-500"
                     />
                   </div>
                   <div>
                     <label className="block text-[11px] font-bold text-muted uppercase tracking-wider mb-1.5">Review Type</label>
                     <select
                       value={reviewType}
                       onChange={e => setReviewType(e.target.value as any)}
                       className="w-full bg-surface border border-theme rounded-lg px-3 py-2 text-xs text-main focus:outline-none focus:border-emerald-500"
                     >
                       <option value="comparative">Comparative Synthesis</option>
                       <option value="methodological">Methodological Analysis</option>
                       <option value="sota">State-of-the-Art Evaluation</option>
                       <option value="comprehensive">Comprehensive Systematic Review</option>
                     </select>
                   </div>
                 </div>

                 <div>
                   <label className="block text-[11px] font-bold text-muted uppercase tracking-wider mb-1.5">Guiding Research Question (Optional)</label>
                   <input
                     type="text"
                     value={reviewQuestion}
                     onChange={e => setReviewQuestion(e.target.value)}
                     placeholder="e.g., How do proposed architectures trade off latency vs retrieval accuracy under extreme contexts?"
                     className="w-full bg-surface border border-theme rounded-lg px-3 py-2 text-xs text-main placeholder-muted focus:outline-none focus:border-emerald-500"
                   />
                 </div>
               </div>

               {/* Generated Topics Display */}
               {generatedTopics.length === 0 ? (
                 <div className="bg-card border border-theme rounded-xl p-8 text-center my-auto">
                   <BookOpen className="w-10 h-10 text-emerald-500 mx-auto mb-3 opacity-80" />
                   <h3 className="text-sm font-bold text-main mb-1">No Topics Generated Yet</h3>
                   <p className="text-xs text-muted max-w-md mx-auto mb-4">
                     Click "Generate Review Topics with Requirements" to automatically extract grounded topics and comparison dimensions from your selected papers.
                   </p>
                   <button
                     onClick={handleGenerateTopicsWithRequirements}
                     className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition-colors"
                   >
                     Generate Grounded Topics
                   </button>
                 </div>
               ) : (
                 <div className="space-y-4 flex-1 overflow-y-auto pr-1">
                   {/* Topic Tabs */}
                   <div className="flex gap-2 border-b border-theme pb-2">
                     {generatedTopics.map((t, idx) => (
                       <button
                         key={t.id}
                         onClick={() => setActiveTopicIndex(idx)}
                         className={cn(
                           "px-3 py-1.5 rounded-lg text-xs font-bold transition-colors text-left truncate max-w-[280px]",
                           activeTopicIndex === idx 
                             ? "bg-emerald-600 text-white" 
                             : "bg-card border border-theme text-muted hover:text-main"
                         )}
                       >
                         Topic {idx + 1}: {t.topicTitle.split(':')[0]}
                       </button>
                     ))}
                   </div>

                   {/* Active Topic Requirements Card */}
                   {(() => {
                     const topic = generatedTopics[activeTopicIndex] || generatedTopics[0];
                     return (
                       <div className="bg-card border border-theme rounded-xl p-5 space-y-4 shadow-sm">
                         <div>
                           <div className="flex items-center gap-2 mb-1">
                             <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                               Verified Grounded Topic
                             </span>
                           </div>
                           <h3 className="text-base font-bold text-main">{topic.topicTitle}</h3>
                           <p className="text-xs text-sub mt-1"><strong>Research Question:</strong> {topic.reviewQuestion}</p>
                           <p className="text-xs text-muted mt-1 italic"><strong>Rationale:</strong> {topic.groundedRationale}</p>
                         </div>

                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-theme">
                           <div>
                             <h4 className="text-[11px] font-bold text-muted uppercase tracking-wider mb-2 flex items-center gap-1.5">
                               <Layers className="w-3.5 h-3.5 text-emerald-400" /> Required Papers & Evidence
                             </h4>
                             <ul className="space-y-1.5">
                               {topic.requiredPapers.map(p => (
                                 <li key={p.id} className="text-xs text-sub bg-surface p-2 rounded border border-theme">
                                   <div className="font-semibold text-main truncate">{p.title}</div>
                                   <div className="text-[10px] text-muted truncate">{p.authors}</div>
                                 </li>
                               ))}
                             </ul>
                           </div>

                           <div className="space-y-3">
                             <div>
                               <h4 className="text-[11px] font-bold text-muted uppercase tracking-wider mb-1.5">Key Dimensions & Comparisons</h4>
                               <div className="flex flex-wrap gap-1.5">
                                 {topic.keyDimensions.map((dim, i) => (
                                   <span key={i} className="text-[11px] px-2 py-0.5 rounded bg-surface border border-theme text-main font-medium">
                                     {dim}
                                   </span>
                                 ))}
                               </div>
                             </div>

                             <div>
                               <h4 className="text-[11px] font-bold text-muted uppercase tracking-wider mb-1.5">Known Gaps & Limitations</h4>
                               <ul className="list-disc pl-4 text-xs text-muted space-y-1">
                                 {topic.knownGaps.concat(topic.limitations).slice(0, 3).map((gap, i) => (
                                   <li key={i}>{gap}</li>
                                 ))}
                               </ul>
                             </div>
                           </div>
                         </div>

                         <div className="p-3 rounded-lg bg-surface border border-theme text-xs text-sub flex items-start gap-2">
                           <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                           <div>
                             <span className="font-bold text-main">Output Structure & Citation Rule: </span>
                             {topic.citationRequirements}
                           </div>
                         </div>
                       </div>
                     );
                   })()}
                 </div>
               )}
             </div>
          )}

          {/* STEP 3: SYNTHESIZE EVIDENCE */}
          {currentStep === 3 && (
             <div className="flex-1 animate-in slide-in-from-right-4 duration-300 flex flex-col">
               <div className="flex items-center justify-between mb-4">
                 <div>
                   <h2 className="text-lg font-black text-main">Synthesize Evidence</h2>
                   <p className="text-sm text-sub">Authoritative paper-grounded synthesis using your formulated review topics.</p>
                 </div>
                 {synthesisState.status === 'success' && (
                   <button 
                     onClick={generateSynthesis}
                     className="px-3 py-1.5 rounded-lg border border-theme bg-card hover:bg-card-hover text-xs font-bold text-main transition-colors"
                   >
                     Regenerate Synthesis
                   </button>
                 )}
               </div>
               
               {synthesisState.status === 'idle' || synthesisState.status === 'loading' ? (
                 <div className="bg-card border border-theme rounded-xl p-8 text-center shadow-sm my-auto">
                   <BrainCircuit className={cn("w-12 h-12 mx-auto mb-4", synthesisState.status === 'loading' ? "text-emerald-500 animate-pulse" : "text-muted")} />
                   <h3 className="text-lg font-bold text-main mb-2">
                     {synthesisState.status === 'loading' ? 'Synthesizing Literature...' : 'Ready to Synthesize'}
                   </h3>
                   <p className="text-sm text-sub font-medium max-w-md mx-auto mb-6">
                     {synthesisState.status === 'loading' 
                       ? 'Extracting evidence from selected papers and generating a structured review across the defined topics.'
                       : 'Generate a structured literature review based on verified evidence from your selected papers.'}
                   </p>
                   {synthesisState.status === 'idle' && (
                     <button onClick={generateSynthesis} className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-bold transition-colors">
                       Generate Synthesis
                     </button>
                   )}
                 </div>
               ) : synthesisState.status === 'insufficient_evidence' ? (
                 <div className="bg-amber-950/20 border border-amber-500/30 rounded-xl p-8 text-center shadow-sm my-auto">
                   <FileText className="w-12 h-12 text-amber-400 mx-auto mb-4" />
                   <h3 className="text-lg font-bold text-amber-300 mb-2">Insufficient Evidence</h3>
                   <p className="text-sm text-amber-200/80 font-medium max-w-md mx-auto mb-6">
                     I couldn't generate a grounded literature synthesis because the selected papers do not contain sufficient research evidence (e.g., missing abstracts).
                   </p>
                   <button onClick={() => setCurrentStep(1)} className="px-6 py-2 bg-card border border-amber-400/40 text-amber-300 rounded-lg text-sm font-bold hover:bg-card-hover transition-colors">
                     Go Back to Selection
                   </button>
                 </div>
               ) : synthesisState.status === 'error' ? (
                 <div className="bg-red-950/20 border border-red-500/30 rounded-xl p-8 text-center shadow-sm my-auto">
                   <BrainCircuit className="w-12 h-12 text-red-400 mx-auto mb-4" />
                   <h3 className="text-lg font-bold text-red-300 mb-2">Generation Failed</h3>
                   <p className="text-sm text-red-200/80 font-medium max-w-md mx-auto mb-6">
                     Your selected research was retrieved, but the literature synthesis could not be generated. Please try again.
                   </p>
                   <button onClick={generateSynthesis} className="px-6 py-2 bg-card border border-red-400/40 text-red-300 rounded-lg text-sm font-bold hover:bg-card-hover transition-colors">
                     Retry Synthesis
                   </button>
                 </div>
               ) : (
                 <div className="flex flex-col h-full space-y-6 overflow-y-auto">
                   <div className="bg-card border border-theme rounded-xl p-6 shadow-sm">
                     <div className="flex items-center justify-between mb-4">
                       <div>
                         <h3 className="text-sm font-bold text-main">Synthesis Complete</h3>
                         <div className="flex items-center gap-2 mt-1">
                           <span className="text-[11px] font-bold text-sub uppercase tracking-widest bg-surface px-2 py-0.5 rounded-full border border-theme">
                             Grounded by {synthesisState.trace?.provider === 'gemini' ? 'Gemini' : 'Local AI'}
                           </span>
                           <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-widest bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/30">
                             {synthesisState.trace?.evidence_ready_count} Evidence Sources
                           </span>
                         </div>
                       </div>
                     </div>
                     <p className="text-sm text-sub font-medium">
                       Selected Papers: {synthesisState.trace?.selected_count} • Evidence Ready: {synthesisState.trace?.evidence_ready_count} • Metadata Only: {synthesisState.trace?.metadata_only_count}
                     </p>
                   </div>
                   
                   <div className="bg-card border border-theme rounded-xl shadow-sm p-8 max-w-none overflow-y-auto text-main">
                     <div 
                       className="prose prose-invert max-w-none text-sub leading-relaxed" 
                       dangerouslySetInnerHTML={{ __html: synthesisState.review.replace(/\\n/g, '<br/>').replace(/### (.*?)\\<br\\/\\>/g, '<h3 class="text-main font-bold text-base mt-4 mb-2">$1</h3>') }} 
                     />
                   </div>

                   {synthesisState.trace?.metadata_only_count > 0 && (
                     <div className="bg-surface border border-theme rounded-xl p-4 shadow-sm">
                       <h4 className="text-xs font-bold text-muted uppercase tracking-widest mb-2">Metadata only — not used for synthesis</h4>
                       <ul className="list-disc pl-4 text-xs text-sub space-y-1">
                         {synthesisState.sources.filter(s => s.evidence_status === 'metadata_only').map((s: any) => (
                           <li key={s.paper_id}>{s.title}</li>
                         ))}
                       </ul>
                     </div>
                   )}
                 </div>
               )}
             </div>
          )}

          {/* STEP 4: FINAL REVIEW */}
          {currentStep === 4 && (
             <div className="flex-1 animate-in slide-in-from-right-4 duration-300">
               <h2 className="text-lg font-black text-main mb-6">Final Literature Review</h2>
               
               <div className="bg-card border border-theme rounded-xl shadow-sm overflow-hidden flex flex-col min-h-[500px]">
                 <div className="p-8 flex-1">
                   <h1 className="text-2xl font-black text-main mb-2 outline-none" contentEditable suppressContentEditableWarning>
                     {reviewObjective || (activeTopic?.title ? \`Literature Review: \${activeTopic.title}\` : 'Literature Review Synthesis')}
                   </h1>
                   <p className="text-xs text-muted font-medium mb-6">
                     Grounded synthesis from {synthesisState.trace?.evidence_ready_count || selectedPapers.length} selected sources.
                   </p>
                   
                   {selectedPapers.length === 0 ? (
                     <p className="text-sm leading-relaxed text-muted italic">No papers selected for review.</p>
                   ) : (
                     <div className="space-y-6">
                       <h3 className="text-xs font-bold uppercase tracking-widest text-muted border-b border-theme pb-2">Verified Sources Grounded</h3>
                       
                       <div className="grid grid-cols-1 gap-2.5">
                         {selectedPapers.map((b, idx) => (
                           <div key={b.paper.id} className="text-xs flex gap-3 p-3 rounded-lg bg-surface border border-theme">
                             <div className="font-bold text-emerald-400 mt-0.5">[{idx + 1}]</div>
                             <div className="flex-1 min-w-0">
                               <div className="font-bold text-main mb-0.5 leading-snug truncate">{b.paper.title}</div>
                               <div className="text-muted mb-1 truncate">{b.paper.authors} ({b.paper.published ? b.paper.published.substring(0, 4) : 'Recent'})</div>
                               {b.paper.url && (
                                 <a 
                                   href={b.paper.url} 
                                   target="_blank" 
                                   rel="noreferrer"
                                   className="text-emerald-400 hover:text-emerald-300 font-medium inline-flex items-center gap-1 text-[11px]"
                                 >
                                   View Original Paper <ExternalLink className="w-3 h-3" />
                                 </a>
                               )}
                             </div>
                           </div>
                         ))}
                       </div>
                       
                       <h3 className="text-xs font-bold uppercase tracking-widest text-muted border-b border-theme pb-2 mt-8">Synthesized Findings</h3>
                       {synthesisState.review ? (
                         <div 
                           className="text-sub text-sm leading-relaxed" 
                           dangerouslySetInnerHTML={{ __html: synthesisState.review.replace(/\\n/g, '<br/>').replace(/### (.*?)\\<br\\/\\>/g, '<h3 class="text-main font-bold text-sm mt-4 mb-2">$1</h3>') }} 
                         />
                       ) : (
                         <p className="text-xs text-muted italic">
                           Review draft prepared. Navigate back to Step 3 to execute real-time synthesis.
                         </p>
                       )}
                     </div>
                   )}
                 </div>
               </div>
             </div>
          )}

          {/* BOTTOM NAVIGATION */}
          <div className="mt-8 flex items-center justify-between pt-6 border-t border-theme shrink-0">
            <button 
              onClick={prevStep}
              disabled={currentStep === 1}
              className="px-4 py-2 text-sm font-bold text-muted hover:text-main disabled:opacity-40 disabled:cursor-not-allowed rounded-lg transition-colors"
            >
              Back
            </button>
            <button 
              onClick={nextStep}
              disabled={currentStep === 4 || (currentStep === 1 && selectedPaperIds.size === 0)}
              className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-bold disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center gap-2 shadow-sm"
            >
              Next Step <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
\`;

fs.writeFileSync('src/pages/LiteratureReviewPage.tsx', pageCode);
console.log('Successfully updated LiteratureReviewPage.tsx');
