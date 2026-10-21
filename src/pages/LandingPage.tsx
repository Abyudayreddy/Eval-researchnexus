import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, Network, 
  Sparkles, Activity,
  CheckCircle2, Atom, FileText,
  ArrowRight, ChevronRight, Play, Filter,
  Bookmark, AlignLeft, FolderPlus, BarChart2
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { ResearchAtmosphere, AtmosphereState } from '../components/ResearchAtmosphere';
import { cn } from '../utils/cn';

// --- Floating Nav ---
const FloatingNav = () => {
  const { isAuthenticated } = useAuthStore();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="fixed top-6 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none">
      <motion.nav 
        animate={{ width: scrolled ? '90%' : '100%', maxWidth: scrolled ? '1000px' : '1200px', y: scrolled ? -10 : 0 }}
        className="pointer-events-auto bg-[#F8F8F5]/90 backdrop-blur-xl border border-[#E6E1D8] shadow-[0_8px_30px_rgba(23,35,63,0.04)] rounded-full px-6 py-3 flex items-center justify-between transition-all"
      >
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full border border-[#E6E1D8] flex items-center justify-center bg-white">
            <Atom className="w-4 h-4 text-[#142653]" />
          </div>
          <span className="font-bold text-[#142653] tracking-tight hidden sm:block">ResearchNexus AI</span>
        </div>

        <div className="hidden md:flex items-center gap-8">
          {['Explore', 'How It Works', 'Domains', 'Research OS'].map(link => (
            <a key={link} href={`#${link.toLowerCase().replace(/ /g, '-')}`} className="text-sm font-medium text-[#334155] hover:text-[#142653] transition-colors">
              {link}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <Link to="/dashboard" className="text-sm font-bold text-[#142653] px-4 py-2 hover:bg-[#142653]/5 rounded-full transition-colors">
              Dashboard
            </Link>
          ) : (
            <Link to="/login" className="text-sm font-bold text-[#334155] hover:text-[#142653] hover:underline decoration-2 decoration-[#8B6FF7] underline-offset-4 transition-all hidden sm:block">
              Log In
            </Link>
          )}
          <Link to={isAuthenticated ? "/research" : "/register"} className="bg-[#142653] text-white text-sm font-bold px-6 py-2.5 rounded-full hover:bg-[#142653]/90 hover:-translate-y-0.5 hover:shadow-md transition-all flex items-center gap-2">
            Start Researching <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </motion.nav>
    </div>
  );
};

// --- Hero ---
const Hero = () => {
  const { isAuthenticated } = useAuthStore();
  
  return (
  <section className="relative min-h-[95vh] pt-32 pb-20 px-6 flex flex-col md:flex-row items-center justify-center max-w-7xl mx-auto">
    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#8B6FF7] via-[#E97A5A] to-[#3BA7A0] via-[#63B76A] to-[#E9A23B] z-50"></div>
    
    <div className="w-full md:w-1/2 z-10 pr-0 md:pr-12 relative">
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-[#8B6FF7]/10 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="inline-block px-3 py-1 bg-[#F8F8F5] border border-[#E6E1D8] rounded-full mb-6">
        <span className="font-mono text-xs font-bold text-[#E97A5A] uppercase tracking-widest">The Research OS</span>
      </div>
      <h1 className="text-6xl md:text-[84px] font-extrabold text-[#142653] tracking-tighter leading-[1.05] mb-6 drop-shadow-sm">
        Research,<br/>
        <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#8B6FF7] to-[#E97A5A]">understood.</span>
      </h1>
      <p className="text-xl md:text-2xl text-[#334155] font-medium leading-relaxed mb-10 max-w-xl">
        Find research. Understand evidence. Connect ideas. Build knowledge.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link to={isAuthenticated ? "/research" : "/register"} className="bg-[#142653] text-white text-lg font-bold px-8 py-4 rounded-full hover:-translate-y-1 hover:shadow-lg hover:shadow-[#142653]/20 transition-all inline-flex items-center justify-center gap-2">
          Start Researching <ArrowRight className="w-5 h-5" />
        </Link>
        <a href="#how-it-works" className="bg-[#F8F8F5] border border-[#E6E1D8] text-[#142653] text-lg font-bold px-8 py-4 rounded-full hover:-translate-y-1 hover:shadow-md transition-all inline-flex items-center justify-center gap-2">
          See How It Works <Play className="w-5 h-5" />
        </a>
      </div>
    </div>

    <div className="w-full md:w-1/2 h-[500px] relative mt-16 md:mt-0 hidden md:block">
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-[#4B8BF5]/10 via-transparent to-transparent blur-3xl pointer-events-none"></div>
        
        <motion.div animate={{ y: [0, -10, 0] }} transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }} className="relative z-20 bg-white border border-[#E6E1D8] px-8 py-4 rounded-3xl shadow-2xl shadow-[#142653]/5 flex items-center gap-4">
           <Atom className="w-8 h-8 text-[#8B6FF7]" />
           <span className="font-bold text-[#142653] text-2xl tracking-tight">ResearchNexus AI</span>
        </motion.div>
        
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-[0.15]" viewBox="0 0 500 500">
           <motion.circle cx="250" cy="250" r="160" stroke="#142653" strokeWidth="1" fill="none" strokeDasharray="4 4" animate={{ rotate: 360 }} transition={{ duration: 60, repeat: Infinity, ease: "linear" }} />
           <motion.circle cx="250" cy="250" r="240" stroke="#142653" strokeWidth="1" fill="none" strokeDasharray="2 8" animate={{ rotate: -360 }} transition={{ duration: 90, repeat: Infinity, ease: "linear" }} />
           <line x1="250" y1="50" x2="250" y2="450" stroke="#142653" strokeWidth="1" strokeDasharray="2 4" />
           <line x1="50" y1="250" x2="450" y2="250" stroke="#142653" strokeWidth="1" strokeDasharray="2 4" />
        </svg>

        {/* Orbiting UI Fragments */}
        <motion.div animate={{ y: [-15, 15, -15], x: [-5, 5, -5] }} transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }} className="absolute top-[5%] left-[5%] bg-white/90 backdrop-blur-md border border-[#E6E1D8] p-4 rounded-2xl shadow-xl w-48 z-10">
          <div className="flex items-center gap-2 mb-2"><FileText className="w-4 h-4 text-[#3BA7A0]"/><span className="font-mono text-[9px] font-bold text-[#334155] uppercase tracking-widest">Paper Card</span></div>
          <div className="h-2 w-full bg-[#F3F0E8] rounded mb-1.5"></div>
          <div className="h-2 w-5/6 bg-[#F3F0E8] rounded"></div>
        </motion.div>

        <motion.div animate={{ y: [15, -15, 15], x: [5, -5, 5] }} transition={{ duration: 8, repeat: Infinity, ease: "easeInOut", delay: 1 }} className="absolute bottom-[15%] left-[-5%] bg-white/90 backdrop-blur-md border border-[#E6E1D8] p-4 rounded-2xl shadow-xl w-64 z-30">
          <div className="flex items-center gap-2 mb-2"><Sparkles className="w-4 h-4 text-[#8B6FF7]"/><span className="font-mono text-[9px] font-bold text-[#334155] uppercase tracking-widest">AI Insight</span></div>
          <p className="text-xs text-[#142653] font-medium leading-relaxed">The evidence suggests strong correlation <span className="bg-[#8B6FF7]/10 text-[#8B6FF7] font-mono px-1 rounded shadow-sm">[1]</span>.</p>
        </motion.div>

        <motion.div animate={{ y: [-8, 8, -8] }} transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 2 }} className="absolute top-[25%] right-[0%] bg-white/90 backdrop-blur-md border border-[#E6E1D8] p-3 rounded-2xl shadow-lg z-10 flex items-center gap-3">
           <div className="w-8 h-8 rounded-full bg-[#E8798A]/10 flex items-center justify-center"><Activity className="w-4 h-4 text-[#E8798A]"/></div>
           <span className="font-mono text-[10px] font-bold text-[#142653] uppercase tracking-wider">Healthcare</span>
        </motion.div>

        <motion.div animate={{ y: [10, -10, 10] }} transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 3 }} className="absolute bottom-[5%] right-[10%] bg-[#142653] text-white p-4 rounded-2xl shadow-2xl shadow-[#142653]/30 w-52 z-20">
           <span className="font-mono text-[9px] font-bold text-white/60 uppercase tracking-widest block mb-2">Citation Trace</span>
           <div className="font-medium text-xs border-l-2 border-[#8B6FF7] pl-2 leading-relaxed">Nature Vol. 582, p. 112</div>
        </motion.div>
      </div>
    </div>
  </section>
  );
};

// --- The Alternating Research Journey (Redesigned completely as per prompt) ---
const AlternatingJourney = ({ onSectionChange }: { onSectionChange?: (section: AtmosphereState) => void }) => {
  const { isAuthenticated } = useAuthStore();
  
  const sections = [
    {
      id: '01',
      label: 'PROJECTS',
      title: 'Start with a Workspace.',
      paragraph: 'Create dedicated projects to keep your research organized. Example: Start a project called \'Climate Change Impact\' to store all your searches, papers, and notes for that specific topic in one place.',
      color: '#E97A5A', // Coral
      alignLeft: true,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(233,122,90,0.08)] w-full max-w-lg aspect-[4/3] flex items-center justify-center p-8 relative overflow-hidden">
          <div className="absolute top-[-50px] right-[-50px] w-48 h-48 bg-[#E97A5A]/10 rounded-full blur-[40px] pointer-events-none"></div>
          <motion.div initial={{y: 20, opacity: 0}} whileInView={{y: 0, opacity: 1}} className="bg-white border border-[#E6E1D8] rounded-xl p-5 flex flex-col gap-4 w-full shadow-xl relative overflow-hidden z-10">
            <div className="absolute top-0 left-0 w-1 h-full bg-[#E97A5A]"></div>
            <div className="flex justify-between items-center">
              <FolderPlus className="text-[#E97A5A] w-6 h-6"/>
              <span className="text-[10px] font-bold bg-[#E97A5A]/10 text-[#E97A5A] px-2 py-1 rounded uppercase">Active Workspace</span>
            </div>
            <div className="font-bold text-[#142653] text-lg">Climate Change Impact</div>
            <div className="text-xs text-[#334155] font-medium">Last updated 2 hours ago</div>
            <div className="flex gap-2 mt-2 pt-4 border-t border-[#E6E1D8]">
              <div className="text-[10px] font-bold text-[#334155] bg-[#F8F8F5] border border-[#E6E1D8] px-2 py-1 rounded">12 Papers</div>
              <div className="text-[10px] font-bold text-[#334155] bg-[#F8F8F5] border border-[#E6E1D8] px-2 py-1 rounded">4 Notes</div>
            </div>
          </motion.div>
        </div>
      )
    },
    {
      id: '02',
      label: 'DISCOVER',
      title: 'Find the research that matters.',
      paragraph: 'Use the Research Explorer to find relevant papers instantly. Example: Search \'hybrid retrieval methods\' and the AI will fetch and rank the best papers from your selected domains.',
      color: '#8B6FF7', // Violet
      alignLeft: false,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(139,111,247,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex flex-col">
          <div className="border-b border-[#E6E1D8] p-4 flex items-center gap-3 bg-[#F8F8F5]">
            <Search className="w-4 h-4 text-[#8B6FF7]" />
            <div className="font-mono text-sm text-[#142653] font-bold">Hybrid retrieval methods</div>
          </div>
          <div className="p-4 flex gap-4 h-full bg-[#F8F8F5]">
            <div className="w-1/4 flex flex-col gap-2">
              <div className="text-xs font-bold text-[#334155] uppercase tracking-widest">Filters</div>
              <div className="bg-white border border-[#E6E1D8] rounded p-2 text-[10px] flex items-center justify-between"><span className="text-[#142653]">AI Domain</span><CheckCircle2 className="w-3 h-3 text-[#8B6FF7]"/></div>
              <div className="bg-white border border-[#E6E1D8] rounded p-2 text-[10px] flex items-center justify-between"><span className="text-[#142653]">2023 - 2024</span><CheckCircle2 className="w-3 h-3 text-[#8B6FF7]"/></div>
            </div>
            <div className="w-3/4 flex flex-col gap-3">
              <motion.div initial={{y:10, opacity:0}} whileInView={{y:0, opacity:1}} className="bg-white border-2 border-[#8B6FF7] rounded-lg p-3 shadow-sm relative">
                <div className="absolute top-2 right-2 bg-[#8B6FF7]/10 text-[#8B6FF7] text-[9px] font-bold px-1.5 py-0.5 rounded uppercase">High Relevance</div>
                <div className="w-3/4 h-3 bg-[#F3F0E8] rounded mb-2"></div>
                <div className="w-full h-2 bg-[#F3F0E8] rounded mb-1"></div>
                <div className="w-5/6 h-2 bg-[#F3F0E8] rounded"></div>
              </motion.div>
              <motion.div initial={{y:10, opacity:0}} whileInView={{y:0, opacity:1}} transition={{delay:0.1}} className="bg-white border border-[#E6E1D8] rounded-lg p-3 opacity-60">
                <div className="w-2/3 h-3 bg-[#F3F0E8] rounded mb-2"></div>
                <div className="w-full h-2 bg-[#F3F0E8] rounded mb-1"></div>
              </motion.div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: '03',
      label: 'UNDERSTAND',
      title: 'Turn papers into knowledge.',
      paragraph: 'Chat with the AI Assistant to understand complex papers faster. Example: Ask \'How does this method reduce hallucination?\' and get a summary backed by direct citations.',
      color: '#4B8BF5', // Blue
      alignLeft: true,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(75,139,245,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex flex-col p-4 relative">
          <div className="absolute bottom-[-50px] left-[-50px] w-48 h-48 bg-[#4B8BF5]/10 rounded-full blur-[40px] pointer-events-none"></div>
          <motion.div initial={{x:20, opacity:0}} whileInView={{x:0, opacity:1}} className="self-end bg-[#4B8BF5]/10 text-[#4B8BF5] rounded-xl rounded-tr-sm p-3 max-w-[80%] mb-4 text-sm font-medium z-10">
            How does hybrid retrieval reduce hallucination?
          </motion.div>
          <motion.div initial={{x:-20, opacity:0}} whileInView={{x:0, opacity:1}} transition={{delay: 0.2}} className="self-start bg-[#F8F8F5] border border-[#E6E1D8] rounded-xl rounded-tl-sm p-4 max-w-[90%] flex flex-col gap-3 z-10">
            <div className="flex items-center gap-2 mb-1">
              <Sparkles className="w-4 h-4 text-[#4B8BF5]" />
              <span className="font-mono text-[10px] font-bold text-[#142653]">AI ASSISTANT</span>
            </div>
            <div className="text-sm text-[#142653] leading-relaxed">
              Hybrid retrieval reduces hallucination by grounding the LLM in highly specific semantic vectors alongside exact keyword matches <span className="inline-block bg-[#4B8BF5]/10 text-[#4B8BF5] font-mono px-1 rounded text-[10px]">[1]</span>.
            </div>
            <div className="flex gap-2 mt-2 pt-3 border-t border-[#E6E1D8]">
              <div className="bg-white border border-[#E6E1D8] text-[9px] font-bold text-[#334155] px-2 py-1 rounded flex items-center gap-1"><FileText className="w-3 h-3 text-[#4B8BF5]"/> Reference 1</div>
            </div>
          </motion.div>
        </div>
      )
    },
    {
      id: '04',
      label: 'ORGANIZE',
      title: 'Keep the papers worth returning to.',
      paragraph: 'Save and categorize papers in your Paper Library. Example: Bookmark that critical 2024 Nature paper into your \'Must Read\' collection so you never lose track of it.',
      color: '#63B76A', // Leaf Green
      alignLeft: false,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(99,183,106,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex flex-col p-4 bg-[#F8F8F5]">
           <div className="flex justify-between items-center mb-4">
             <div className="flex gap-4 border-b border-[#E6E1D8] pb-2 w-full">
               <span className="text-sm font-bold text-[#63B76A] border-b-2 border-[#63B76A] pb-2">Must Read (1)</span>
               <span className="text-sm font-medium text-[#334155]">Bookmarks</span>
             </div>
           </div>
           <div className="flex flex-col gap-3 overflow-hidden">
             {[1,2,3].map((_, i) => (
               <motion.div key={i} initial={{opacity:0, y:10}} whileInView={{opacity:1, y:0}} transition={{delay: i*0.1}} className={cn("bg-white border p-3 rounded-lg flex justify-between items-center", i === 0 ? "border-[#63B76A]/50 shadow-sm" : "border-[#E6E1D8]")}>
                 <div className="flex gap-3 items-center w-3/4">
                   <div className="w-8 h-8 rounded bg-[#63B76A]/10 flex items-center justify-center shrink-0"><FileText className="w-4 h-4 text-[#63B76A]"/></div>
                   <div className="w-full">
                     <div className="h-2 w-full bg-[#F3F0E8] rounded mb-1"></div>
                     <div className="h-2 w-1/2 bg-[#F3F0E8] rounded"></div>
                   </div>
                 </div>
                 <Bookmark className="w-4 h-4 text-[#63B76A]" fill={i === 0 ? "#63B76A" : "none"} />
               </motion.div>
             ))}
           </div>
        </div>
      )
    },
    {
      id: '05',
      label: 'CAPTURE',
      title: 'Remember what you learn.',
      paragraph: 'Jot down ideas in your connected Notebook while you read. Example: Highlight a methodology section and save a note saying \'Compare this baseline to our dataset\'.',
      color: '#E9A23B', // Warm Amber
      alignLeft: true,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(233,162,59,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex">
          <div className="w-1/3 border-r border-[#E6E1D8] bg-[#F8F8F5] p-4 flex flex-col gap-2">
             <div className="text-[10px] font-bold text-[#334155] uppercase tracking-widest mb-2">Topic Notes</div>
             <div className="bg-white border border-[#E6E1D8] p-2 rounded shadow-sm text-[10px] font-bold text-[#142653]">Baseline Comparison</div>
             <div className="bg-transparent border border-transparent p-2 rounded text-[10px] font-medium text-[#334155]">Data cleaning</div>
          </div>
          <div className="w-2/3 p-4 flex flex-col gap-4 bg-white relative">
             <div className="absolute top-[-50px] right-[-50px] w-32 h-32 bg-[#E9A23B]/10 rounded-full blur-[30px] pointer-events-none"></div>
             <motion.div initial={{scale:0.95, opacity:0}} whileInView={{scale:1, opacity:1}} className="bg-[#FEFCE8] border border-[#FEF08A] rounded-xl p-4 shadow-sm h-full relative z-10">
               <div className="font-bold text-[#142653] text-sm mb-2">Baseline Comparison</div>
               <p className="text-xs text-[#142653]/70 leading-relaxed font-mono">
                 Compare this baseline to our dataset. The dual-encoder outperforms in zero-shot domains.
               </p>
               <div className="absolute bottom-3 left-3 bg-white border border-[#FEF08A] rounded px-2 py-1 text-[9px] text-[#142653] flex items-center gap-1 font-bold shadow-sm">
                 <Network className="w-3 h-3 text-[#E9A23B]"/> Connected to Paper
               </div>
             </motion.div>
          </div>
        </div>
      )
    },
    {
      id: '06',
      label: 'BUILD',
      title: 'Turn discoveries into a review.',
      paragraph: 'Draft your paper using the Literature Review tool. Example: Drag and drop your saved citations and notes directly into your Introduction and Methodology sections.',
      color: '#3BA7A0', // Teal
      alignLeft: false,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(59,167,160,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex flex-col">
          <div className="h-12 border-b border-[#E6E1D8] bg-[#F8F8F5] flex items-center px-4 gap-4">
            <AlignLeft className="w-4 h-4 text-[#3BA7A0]" />
            <div className="font-mono text-xs font-bold text-[#142653]">Literature Review Draft</div>
          </div>
          <div className="flex h-full">
            <div className="w-1/3 border-r border-[#E6E1D8] p-3 flex flex-col gap-2">
               <div className="text-[10px] font-bold text-[#334155] uppercase tracking-widest mb-1">Outline</div>
               <div className="text-xs font-bold text-[#3BA7A0] bg-[#3BA7A0]/10 rounded p-1.5">1. Introduction</div>
               <div className="text-xs font-medium text-[#142653] p-1.5">2. Methodology</div>
               <div className="text-[10px] font-bold text-[#334155] uppercase tracking-widest mt-4 mb-1">Sources</div>
               <motion.div animate={{scale:[1, 1.05, 1]}} transition={{duration: 2, repeat: Infinity}} className="text-[10px] bg-white border-2 border-dashed border-[#3BA7A0]/50 rounded p-1.5 text-[#3BA7A0] font-bold text-center">
                 + Drag Citation Here
               </motion.div>
            </div>
            <div className="w-2/3 p-4 bg-white">
               <motion.div initial={{opacity:0}} whileInView={{opacity:1}} transition={{duration:1}}>
                 <div className="text-lg font-bold text-[#142653] mb-3">1. Introduction</div>
                 <div className="w-full h-2 bg-[#F3F0E8] rounded mb-2"></div>
                 <div className="w-full h-2 bg-[#F3F0E8] rounded mb-2"></div>
                 <div className="w-3/4 h-2 bg-[#F3F0E8] rounded mb-4"></div>
                 <div className="bg-[#F8F8F5] border border-[#E6E1D8] rounded p-2 text-[10px] text-[#142653] font-bold flex items-center gap-2 shadow-sm">
                   <FileText className="w-3 h-3 text-[#3BA7A0]"/> <span>[Smith et al. 2024]</span>
                 </div>
               </motion.div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: '07',
      label: 'EXPLAIN',
      title: 'Trust the AI\'s reasoning.',
      paragraph: 'See exactly how the AI arrived at its answer using Explainable AI. Example: Click on an AI response to see the exact paragraphs and papers it used to generate that specific claim.',
      color: '#7564C9', // Indigo-Violet
      alignLeft: true,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(117,100,201,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex flex-col items-center justify-center relative p-6">
          <svg className="absolute inset-0 w-full h-full opacity-20 pointer-events-none" viewBox="0 0 400 300">
             <path d="M 200 50 L 200 250" stroke="#7564C9" strokeWidth="2" strokeDasharray="4 4" />
          </svg>
          <motion.div initial={{y:-20, opacity:0}} whileInView={{y:0, opacity:1}} className="bg-[#7564C9]/10 text-[#7564C9] text-[10px] font-bold px-3 py-1.5 rounded-full z-10 mb-4 border border-[#7564C9]/20 uppercase">
            User Question
          </motion.div>
          <motion.div initial={{y:-20, opacity:0}} whileInView={{y:0, opacity:1}} transition={{delay:0.2}} className="bg-white border border-[#E6E1D8] text-[#142653] text-xs font-bold px-3 py-1.5 rounded-lg shadow-sm z-10 mb-4 flex items-center gap-2">
            <Search className="w-3 h-3 text-[#7564C9]"/> 3 Papers Retrieved
          </motion.div>
          <motion.div initial={{y:-20, opacity:0}} whileInView={{y:0, opacity:1}} transition={{delay:0.4}} className="bg-white border border-[#E6E1D8] text-[#142653] text-xs font-bold px-3 py-1.5 rounded-lg shadow-sm z-10 mb-4 flex items-center gap-2">
            <Filter className="w-3 h-3 text-[#7564C9]"/> 2 Paragraphs Selected
          </motion.div>
          <motion.div initial={{y:-20, opacity:0}} whileInView={{y:0, opacity:1}} transition={{delay:0.6}} className="bg-[#142653] text-white text-xs font-bold px-4 py-2 rounded-lg shadow-xl z-10 flex items-center gap-2">
            <Sparkles className="w-3 h-3 text-[#7564C9]"/> Final AI Answer
          </motion.div>
        </div>
      )
    },
    {
      id: '08',
      label: 'ANALYTICS',
      title: 'Track your research progress.',
      paragraph: 'View insights into your reading and research habits. Example: Check your Analytics dashboard to see how many papers you\'ve read this week and your most active research domains.',
      color: '#E8798A', // Rose
      alignLeft: false,
      UIFragment: () => (
        <div className="bg-white border border-[#E6E1D8] rounded-2xl shadow-[0_20px_50px_rgba(232,121,138,0.08)] overflow-hidden w-full max-w-lg aspect-[4/3] flex flex-col p-6 relative">
          <div className="absolute top-[-50px] right-[-50px] w-40 h-40 bg-[#E8798A]/10 rounded-full blur-[40px] pointer-events-none"></div>
          <div className="flex items-center gap-3 mb-6 relative z-10">
            <BarChart2 className="w-5 h-5 text-[#E8798A]" />
            <div className="font-bold text-[#142653]">Reading Activity</div>
          </div>
          <div className="flex-1 flex items-end gap-2 border-b border-[#E6E1D8] pb-2 relative z-10">
            {[30, 60, 40, 80, 50, 90, 70].map((h, i) => (
              <motion.div 
                key={i} 
                initial={{height: 0}} 
                whileInView={{height: `${h}%`}} 
                transition={{duration: 0.5, delay: i * 0.1}} 
                className="flex-1 bg-[#E8798A] rounded-t-sm" 
                style={{opacity: 0.4 + (i * 0.1)}}
              ></motion.div>
            ))}
          </div>
          <div className="flex justify-between text-[10px] font-bold text-[#334155] mt-2 relative z-10 uppercase tracking-widest">
            <span>Mon</span>
            <span>Sun</span>
          </div>
        </div>
      )
    }
  ];

  return (
    <section id="how-it-works" className="py-32 bg-[#F8F8F5] border-y border-[#E6E1D8]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-24 md:mb-32">
          <span className="font-mono text-xs font-bold text-[#E97A5A] uppercase tracking-widest bg-white border border-[#E6E1D8] px-3 py-1 rounded-full">The Research Journey</span>
          <h2 className="text-4xl md:text-6xl font-bold text-[#142653] tracking-tight mt-8 mb-6 max-w-4xl">Everything you need to move from a question to meaningful research.</h2>
          <p className="text-xl text-[#334155] font-medium max-w-2xl">ResearchNexus AI connects discovery, understanding, organization, and evidence into one continuous research experience.</p>
        </div>

        <div className="flex flex-col gap-32 md:gap-40">
          {sections.map((section, idx) => {
            const stateMapping = ['discover', 'understand', 'organize', 'capture', 'build', 'explain'];
            return (
            <motion.div 
              key={section.id} 
              onViewportEnter={() => onSectionChange?.(stateMapping[idx] as AtmosphereState)}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              viewport={{ once: true, margin: "-100px" }}
              className={cn("flex flex-col items-center gap-12 md:gap-24 relative", section.alignLeft ? "md:flex-row" : "md:flex-row-reverse")}
            >
              {/* Thin Separator for all except the first */}
              {idx !== 0 && <div className="absolute -top-16 md:-top-20 left-0 w-full h-[1px] bg-[#E6E1D8]"></div>}

              {/* Text Content */}
              <div className="w-full md:w-5/12 flex flex-col items-start z-10">
                <div className="font-mono text-xs font-bold px-3 py-1 rounded-full border mb-6" style={{ color: section.color, backgroundColor: `${section.color}10`, borderColor: `${section.color}30` }}>
                  {section.label}
                </div>
                <h3 className="text-3xl md:text-5xl font-bold text-[#142653] tracking-tight mb-6 leading-[1.1]">{section.title}</h3>
                <p className="text-lg text-[#334155] font-medium leading-relaxed">{section.paragraph}</p>
              </div>

              {/* Visual Fragment */}
              <div className="w-full md:w-7/12 flex justify-center relative z-10">
                <div className="absolute inset-0 scale-150 blur-[150px] opacity-30 pointer-events-none rounded-full transition-all duration-1000" style={{ backgroundColor: section.color }}></div>
                <div className="relative z-10 w-full flex justify-center hover:-translate-y-2 transition-transform duration-500">
                  <section.UIFragment />
                </div>
              </div>
            </motion.div>
          );
          })}
        </div>

        {/* Final Conclusion Statement */}
        <div className="mt-40 text-center border-t border-[#E6E1D8] pt-24">
           <h2 className="text-4xl md:text-5xl font-bold text-[#142653] tracking-tight mb-4">One research question. One connected journey.</h2>
           <p className="text-xl text-[#334155] font-medium mb-10 max-w-2xl mx-auto">ResearchNexus AI keeps the papers, ideas, evidence, and knowledge you build along the way connected.</p>
           <Link to={isAuthenticated ? "/research" : "/register"} className="bg-[#142653] text-white text-lg font-bold px-8 py-4 rounded-full hover:bg-[#142653]/90 transition-colors inline-flex justify-center items-center gap-2">
             Start Researching <ArrowRight className="w-5 h-5" />
           </Link>
        </div>
      </div>
    </section>
  );
};

// --- Cinematic Carousel for Domain Universe ---
const CinematicCarousel = ({ onDomainChange }: { onDomainChange?: (id: string) => void }) => {
  const domains = [
    { id: 'artificial-intelligence', name: 'ARTIFICIAL INTELLIGENCE', desc: 'Machine learning, deep learning, RAG, and intelligent systems.', color: '#8B6FF7', artwork: 'ai' },
    { id: 'data-science', name: 'DATA SCIENCE', desc: 'Analytics, data mining, statistical modeling, and research insights.', color: '#E97A5A', artwork: 'data' },
    { id: 'healthcare', name: 'HEALTHCARE', desc: 'Medical AI, disease prediction, clinical research, drug discovery, and biotechnology.', color: '#E8798A', artwork: 'health' },
    { id: 'materials-science', name: 'MATERIALS SCIENCE', desc: 'Nanotechnology, advanced materials, polymers, and structural engineering research.', color: '#4B8BF5', artwork: 'materials' },
    { id: 'environmental-science', name: 'ENVIRONMENTAL SCIENCE', desc: 'Climate change, pollution analysis, ecology, and environmental research.', color: '#2F8F72', artwork: 'env' },
    { id: 'energy', name: 'ENERGY', desc: 'Renewable energy, energy systems, storage, and emerging technologies.', color: '#E9A23B', artwork: 'energy' },
    { id: 'space-science', name: 'SPACE SCIENCE', desc: 'Astrophysics, orbital research, planetary science, and space exploration.', color: '#7564C9', artwork: 'space' },
    { id: 'interdisciplinary', name: 'INTERDISCIPLINARY RESEARCH', desc: 'Research that connects ideas across scientific disciplines.', color: '#3BA7A0', artwork: 'inter' },
  ];

  const [activeIdx, setActiveIdx] = useState(0);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') setActiveIdx(prev => Math.min(prev + 1, domains.length - 1));
      if (e.key === 'ArrowLeft') setActiveIdx(prev => Math.max(prev - 1, 0));
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [domains.length]);

  const activeDomain = domains[activeIdx];

  useEffect(() => {
    onDomainChange?.(activeDomain.id);
  }, [activeIdx, activeDomain.id, onDomainChange]);

  const getArtwork = (type: string, color: string) => {
    return (
      <div className="absolute inset-0 overflow-hidden">
        {/* Soft background blending for every card */}
        <div className="absolute inset-0 mix-blend-multiply opacity-20" style={{ background: `linear-gradient(135deg, transparent 0%, ${color} 100%)` }}></div>
        {/* Large atmospheric glow */}
        <div className="absolute -top-10 -right-10 w-64 h-64 rounded-full blur-[80px] opacity-40" style={{ backgroundColor: color }}></div>
        <div className="absolute -bottom-20 -left-20 w-80 h-80 rounded-full blur-[100px] opacity-30" style={{ backgroundColor: color }}></div>
        
        {/* Domain-specific highly detailed SVG artwork */}
        <svg className="absolute inset-0 w-full h-full opacity-80" viewBox="0 0 200 200" preserveAspectRatio="xMidYMid slice">
          {type === 'ai' && (
            <g>
              <path d="M30 100 Q80 20 170 100 Q80 180 30 100" stroke={color} strokeWidth="0.5" fill="none" opacity="0.5" />
              <path d="M50 100 Q100 50 150 100 Q100 150 50 100" stroke={color} strokeWidth="1" fill="none" opacity="0.6" />
              {[...Array(40)].map((_, i) => (
                <circle key={i} cx={20 + (i * 17) % 160} cy={20 + (i * 23) % 160} r={Math.random() * 3 + 1} fill={color} opacity={Math.random() * 0.8 + 0.2} />
              ))}
              {[...Array(30)].map((_, i) => (
                <line key={i} x1={20 + (i * 17) % 160} y1={20 + (i * 23) % 160} x2={20 + ((i+1) * 17) % 160} y2={20 + ((i+1) * 23) % 160} stroke={color} strokeWidth="0.5" opacity="0.4" />
              ))}
              <circle cx="100" cy="100" r="15" fill={color} opacity="0.9" />
              <circle cx="100" cy="100" r="25" fill="none" stroke={color} strokeWidth="2" opacity="0.5" strokeDasharray="4 4" className="animate-[spin_10s_linear_infinite]" style={{ transformOrigin: '100px 100px' }} />
            </g>
          )}
          {type === 'data' && (
            <g>
              <rect x="20" y="80" width="25" height="120" fill={color} opacity="0.5" rx="4" />
              <rect x="55" y="110" width="25" height="90" fill={color} opacity="0.7" rx="4" />
              <rect x="90" y="40" width="25" height="160" fill={color} opacity="0.8" rx="4" />
              <rect x="125" y="140" width="25" height="60" fill={color} opacity="0.4" rx="4" />
              <rect x="160" y="60" width="25" height="140" fill={color} opacity="0.9" rx="4" />
              <path d="M32 70 L67 100 L102 30 L137 130 L172 50" stroke={color} strokeWidth="3" fill="none" />
              <path d="M32 70 L67 100 L102 30 L137 130 L172 50 L172 200 L32 200 Z" fill={color} opacity="0.1" />
              {[...Array(15)].map((_, i) => <circle key={i} cx={Math.random()*200} cy={Math.random()*200} r="2" fill={color} opacity="0.6"/>)}
            </g>
          )}
          {type === 'health' && (
            <g>
              <path d="M 40,0 C 120,50 120,150 40,200" stroke={color} strokeWidth="4" fill="none" opacity="0.8" />
              <path d="M 160,0 C 80,50 80,150 160,200" stroke={color} strokeWidth="4" fill="none" opacity="0.8" />
              {[20, 50, 80, 110, 140, 170].map(y => (
                <line key={y} x1={40 + (y < 100 ? y*0.6 : (200-y)*0.6)} y1={y} x2={160 - (y < 100 ? y*0.6 : (200-y)*0.6)} y2={y} stroke={color} strokeWidth="3" opacity="0.6" />
              ))}
              <path d="M 0,100 L 40,100 L 50,70 L 70,140 L 90,80 L 100,100 L 200,100" stroke={color} strokeWidth="2" fill="none" opacity="0.5" />
            </g>
          )}
          {type === 'materials' && (
            <g>
              <polygon points="100,20 150,50 150,110 100,140 50,110 50,50" fill="none" stroke={color} strokeWidth="2" opacity="0.8" />
              <polygon points="100,50 130,70 130,100 100,120 70,100 70,70" fill={color} opacity="0.4" />
              <line x1="100" y1="20" x2="100" y2="50" stroke={color} strokeWidth="2" opacity="0.6" />
              <line x1="150" y1="50" x2="130" y2="70" stroke={color} strokeWidth="2" opacity="0.6" />
              <line x1="150" y1="110" x2="130" y2="100" stroke={color} strokeWidth="2" opacity="0.6" />
              <line x1="100" y1="140" x2="100" y2="120" stroke={color} strokeWidth="2" opacity="0.6" />
              <line x1="50" y1="110" x2="70" y2="100" stroke={color} strokeWidth="2" opacity="0.6" />
              <line x1="50" y1="50" x2="70" y2="70" stroke={color} strokeWidth="2" opacity="0.6" />
              <circle cx="100" cy="85" r="15" fill={color} opacity="0.9" className="animate-[pulse_4s_ease-in-out_infinite]" />
              <path d="M 0,50 L 200,50 M 0,100 L 200,100 M 0,150 L 200,150 M 50,0 L 50,200 M 100,0 L 100,200 M 150,0 L 150,200" stroke={color} strokeWidth="0.5" opacity="0.2" />
            </g>
          )}
          {type === 'env' && (
            <g>
              <circle cx="100" cy="100" r="70" fill="none" stroke={color} strokeWidth="2" opacity="0.4" />
              <path d="M 40,60 Q 100,120 160,60 M 30,100 Q 100,160 170,100 M 40,140 Q 100,200 160,140" stroke={color} strokeWidth="1.5" fill="none" opacity="0.6" />
              <circle cx="100" cy="100" r="90" fill="none" stroke={color} strokeWidth="1" strokeDasharray="4 8" className="animate-[spin_20s_linear_infinite]" style={{ transformOrigin: '100px 100px' }} />
              <path d="M 100,30 L 100,170 M 30,100 L 170,100 M 50,50 L 150,150 M 50,150 L 150,50" stroke={color} strokeWidth="0.5" opacity="0.3" />
            </g>
          )}
          {type === 'energy' && (
            <g>
              <path d="M 120,10 L 40,110 L 100,110 L 80,190 L 160,90 L 100,90 Z" fill={color} opacity="0.9" />
              <circle cx="100" cy="100" r="80" fill="none" stroke={color} strokeWidth="1" strokeDasharray="2 6" className="animate-[spin_15s_linear_infinite]" style={{ transformOrigin: '100px 100px' }} />
              <circle cx="100" cy="100" r="60" fill="none" stroke={color} strokeWidth="2" strokeDasharray="10 20" className="animate-[spin_10s_linear_infinite_reverse]" style={{ transformOrigin: '100px 100px' }} />
            </g>
          )}
          {type === 'space' && (
            <g>
              <circle cx="100" cy="100" r="35" fill={color} opacity="0.9" />
              <ellipse cx="100" cy="100" rx="80" ry="15" fill="none" stroke={color} strokeWidth="3" transform="rotate(-25 100 100)" opacity="0.8" />
              <ellipse cx="100" cy="100" rx="95" ry="25" fill="none" stroke={color} strokeWidth="1" transform="rotate(-25 100 100)" strokeDasharray="4 4" opacity="0.5" />
              {[...Array(40)].map((_, i) => (
                <circle key={i} cx={Math.random()*200} cy={Math.random()*200} r={Math.random()*2+0.5} fill={color} opacity={Math.random()*0.8+0.2} className="animate-[pulse_3s_ease-in-out_infinite]" style={{ animationDelay: `${Math.random()*2}s` }} />
              ))}
            </g>
          )}
          {type === 'inter' && (
            <g>
              <circle cx="100" cy="100" r="40" fill={color} opacity="0.3" />
              <circle cx="100" cy="100" r="15" fill={color} opacity="0.9" />
              {[0, 60, 120, 180, 240, 300].map(angle => {
                const x = 100 + 60 * Math.cos(angle * Math.PI / 180);
                const y = 100 + 60 * Math.sin(angle * Math.PI / 180);
                return (
                  <g key={angle}>
                    <line x1="100" y1="100" x2={x} y2={y} stroke={color} strokeWidth="2" opacity="0.6" />
                    <circle cx={x} cy={y} r="8" fill={color} opacity="0.8" />
                    <circle cx={x} cy={y} r="14" fill="none" stroke={color} strokeWidth="1" opacity="0.4" />
                  </g>
                );
              })}
              <path d="M 160,100 L 130,151 L 70,151 L 40,100 L 70,48 L 130,48 Z" fill="none" stroke={color} strokeWidth="1" opacity="0.3" />
            </g>
          )}
        </svg>
      </div>
    );
  };

  return (
    <section id="domains" className="py-32 relative overflow-hidden transition-colors duration-1000 bg-[#F8F8F5]">
      {/* Soft Immersive Stage Background */}
      <div className="absolute inset-0 opacity-40 transition-colors duration-1000" style={{ background: `radial-gradient(circle at 50% 60%, ${activeDomain.color}20 0%, transparent 60%)` }}></div>
      
      
      {/* Fine scientific grid */}
      <div className="absolute inset-0 pointer-events-none opacity-20" style={{ backgroundImage: 'linear-gradient(to right, #142653 1px, transparent 1px), linear-gradient(to bottom, #142653 1px, transparent 1px)', backgroundSize: '60px 60px', maskImage: 'radial-gradient(ellipse at center, black 40%, transparent 80%)' }}></div>
      
      {/* Floating nodes in the background */}
      <motion.div animate={{ y: [0, -30, 0] }} transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }} className="absolute top-[20%] left-[10%] w-2 h-2 rounded-full bg-[#142653]/20 blur-[1px]"></motion.div>
      <motion.div animate={{ y: [0, 40, 0] }} transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }} className="absolute top-[30%] right-[15%] w-3 h-3 rounded-full bg-[#142653]/10 blur-[2px]"></motion.div>
      <motion.div animate={{ y: [0, -20, 0] }} transition={{ duration: 12, repeat: Infinity, ease: "easeInOut" }} className="absolute bottom-[20%] left-[20%] w-1.5 h-1.5 rounded-full bg-[#142653]/30 blur-[1px]"></motion.div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="mb-16 text-center">
          <span className="font-mono text-[10px] font-bold text-[#E97A5A] uppercase tracking-widest bg-white border border-[#E6E1D8] px-3 py-1 rounded-full shadow-sm">The Domain Universe</span>
          <h2 className="text-5xl md:text-7xl font-extrabold text-[#142653] tracking-tight mt-6 mb-6">
            Eight domains.<br/>
            <span style={{ color: activeDomain.color }} className="transition-colors duration-1000">One</span> research universe.
          </h2>
          <p className="text-lg text-[#334155] font-medium max-w-xl mx-auto">Explore research across disciplines and discover connections between fields, all within one connected research environment.</p>
        </div>

        {/* Cinematic Carousel Container */}
        <div className="relative w-full h-[400px] md:h-[600px] flex justify-center items-center perspective-[1200px] overflow-hidden">
          {domains.map((domain, i) => {
            const offset = i - activeIdx;
            const absOffset = Math.abs(offset);
            if (absOffset > 2 && window.innerWidth >= 768) return null; // hide far ones on desktop
            if (absOffset > 1 && window.innerWidth < 768) return null; // only show 1 adjacent on mobile

            // Depth calculation
            const scale = absOffset === 0 ? 1.05 : 1 - absOffset * 0.15;
            const translateX = offset * (window.innerWidth < 768 ? 260 : 340);
            const rotateY = offset * -15; // negative angle to face center
            const zIndex = 10 - absOffset;
            const opacity = absOffset === 0 ? 1 : absOffset === 1 ? 0.7 : 0.2;
            const brightness = absOffset === 0 ? 1.1 : 0.8;

            return (
              <motion.div
                key={domain.id}
                onClick={() => setActiveIdx(i)}
                initial={false}
                animate={{ scale, x: translateX, rotateY, zIndex, opacity, filter: `brightness(${brightness})` }}
                transition={{ type: "spring", stiffness: 200, damping: 25 }}
                className={cn(
                  "absolute w-[300px] md:w-[600px] h-[360px] md:h-[400px] rounded-[2rem] border overflow-hidden cursor-pointer shadow-2xl transition-all",
                  absOffset === 0 ? "border-transparent shadow-[0_40px_80px_rgba(20,38,83,0.4)] bg-[#142653] ring-4 ring-[#142653]/10" : "border-[#E6E1D8] shadow-md bg-[#F8F8F5] hover:scale-[0.88] hover:shadow-xl"
                )}
                style={{ transformStyle: 'preserve-3d' }}
              >
                {/* Artwork */}
                <div className="absolute inset-0 z-0 bg-[#142653]">
                  {getArtwork(domain.artwork, domain.color)}
                </div>

                {/* Content Overlay */}
                <div className={cn("absolute inset-0 flex flex-col justify-between z-10 bg-gradient-to-t from-[#142653]/90 via-[#142653]/40 to-transparent", absOffset !== 0 && "opacity-50")}>
                   <div className="p-6 md:p-8 flex flex-col items-center">
                     <span className="font-mono text-[10px] md:text-xs font-bold uppercase tracking-[0.2em] mb-2" style={{ color: domain.color }}>DOMAIN 0{i + 1}</span>
                     <h3 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight leading-tight text-center drop-shadow-md">{domain.name}</h3>
                   </div>
                   
                   <AnimatePresence>
                     {absOffset === 0 && (
                       <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="p-6 md:p-8 flex flex-col items-center bg-gradient-to-t from-[#142653] to-transparent">
                         <p className="text-sm md:text-base text-white/80 text-center font-medium leading-relaxed mb-6 px-4">{domain.desc}</p>
                         <Link to={`/research-domains/${domain.id}`} className="bg-white/10 backdrop-blur-md border border-white/20 text-white text-xs font-bold px-6 py-2.5 rounded-full hover:bg-white/20 transition-all uppercase tracking-widest inline-flex items-center gap-2 hover:-translate-y-1">
                           Explore <ArrowRight className="w-3 h-3" />
                         </Link>
                       </motion.div>
                     )}
                   </AnimatePresence>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Carousel Controls */}
        <div className="mt-8 flex items-center justify-center gap-6 relative z-10">
          <button onClick={() => setActiveIdx(prev => Math.max(prev - 1, 0))} className="w-10 h-10 rounded-full border border-[#E6E1D8] bg-white flex items-center justify-center text-[#142653] hover:bg-[#F3F0E8] transition-colors disabled:opacity-30 disabled:cursor-not-allowed" disabled={activeIdx === 0}>
            <ChevronRight className="w-5 h-5 rotate-180" />
          </button>
          <div className="flex gap-2">
            {domains.map((_, i) => (
              <button key={i} onClick={() => setActiveIdx(i)} className={cn("w-2.5 h-2.5 rounded-full transition-all duration-300", i === activeIdx ? "bg-[#142653] scale-125" : "bg-[#E6E1D8] hover:bg-[#5E6B82]")} aria-label={`Go to domain ${i+1}`} />
            ))}
          </div>
          <button onClick={() => setActiveIdx(prev => Math.min(prev + 1, domains.length - 1))} className="w-10 h-10 rounded-full border border-[#E6E1D8] bg-white flex items-center justify-center text-[#142653] hover:bg-[#F3F0E8] transition-colors disabled:opacity-30 disabled:cursor-not-allowed" disabled={activeIdx === domains.length - 1}>
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
        
        {/* Subtle Connecting Lines Visualization Background */}
        <div className="absolute inset-0 pointer-events-none z-0 hidden md:block">
           <svg className="w-full h-full opacity-[0.03]">
             <line x1="10%" y1="20%" x2="90%" y2="80%" stroke="#142653" strokeWidth="2" />
             <line x1="90%" y1="20%" x2="10%" y2="80%" stroke="#142653" strokeWidth="2" />
           </svg>
        </div>

        {/* Final Text */}
        <div className="text-center mt-24 relative z-10">
           <div className="font-mono text-xs font-bold text-[#334155] uppercase tracking-widest mb-4">Explore the Research Universe</div>
           <h3 className="text-4xl font-bold text-[#142653] tracking-tight mb-4">Different fields.<br/>Connected knowledge.</h3>
           <p className="text-lg text-[#334155] font-medium max-w-xl mx-auto mb-8">Move across domains, discover relevant research, and bring ideas from different fields into one research workflow.</p>
           <Link to="/research" className="bg-white border border-[#E6E1D8] text-[#142653] text-lg font-bold px-8 py-4 rounded-full hover:bg-[#F3F0E8] transition-colors inline-flex justify-center items-center gap-2 shadow-sm">
             Explore All Domains <ArrowRight className="w-5 h-5" />
           </Link>
        </div>
      </div>
    </section>
  );
};


const AudiencePanels = () => {
  const { isAuthenticated } = useAuthStore();
  
  return (
  <section className="py-32 bg-white border-y border-[#E6E1D8]">
    <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-8">
      {/* Student Panel */}
      <div className="bg-[#F8F8F5] border border-[#E6E1D8] p-12 rounded-[2.5rem]">
        <div className="font-mono text-xs font-bold text-[#E97A5A] uppercase tracking-widest mb-6">For Students</div>
        <h2 className="text-4xl font-bold text-[#142653] tracking-tight mb-8">Learn from research.</h2>
        <ul className="space-y-4 mb-12">
          {['Search papers.', 'Understand difficult concepts.', 'Ask questions.', 'Take notes.', 'Build knowledge.'].map(item => (
            <li key={item} className="flex items-center gap-3 text-lg font-medium text-[#334155]"><CheckCircle2 className="w-5 h-5 text-[#E97A5A]"/> {item}</li>
          ))}
        </ul>
        <Link to={isAuthenticated ? "/research" : "/register"} className="bg-white border border-[#E6E1D8] text-[#142653] font-bold px-6 py-3 rounded-full hover:bg-[#F3F0E8] transition-colors inline-flex items-center gap-2 shadow-sm">
          Start Exploring <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Researcher Panel */}
      <div className="bg-[#142653] text-white p-12 rounded-[2.5rem] relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-[#3BA7A0] blur-[100px] opacity-20 pointer-events-none"></div>
        <div className="relative z-10">
          <div className="font-mono text-xs font-bold text-[#3BA7A0] uppercase tracking-widest mb-6">For Researchers</div>
          <h2 className="text-4xl font-bold text-white tracking-tight mb-8">Build on what already exists.</h2>
          <ul className="space-y-4 mb-12">
            {['Discover literature.', 'Compare methodologies.', 'Track papers.', 'Organize research.', 'Build reviews.'].map(item => (
              <li key={item} className="flex items-center gap-3 text-lg font-medium text-white/70"><CheckCircle2 className="w-5 h-5 text-[#3BA7A0]"/> {item}</li>
            ))}
          </ul>
          <Link to={isAuthenticated ? "/research" : "/register"} className="bg-[#3BA7A0] text-white font-bold px-6 py-3 rounded-full hover:bg-[#3BA7A0]/90 transition-colors inline-flex items-center gap-2">
            Start Researching <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  </section>
  );
};

const FinalCTA = () => {
  const { isAuthenticated } = useAuthStore();
  
  return (
    <section className="py-40 bg-[#F8F8F5] relative overflow-hidden flex items-center justify-center text-center">
      {/* Subtle animated network background */}
      <svg className="absolute inset-0 w-full h-full opacity-5 pointer-events-none" viewBox="0 0 1000 1000">
         <circle cx="200" cy="200" r="4" fill="#142653"/><circle cx="800" cy="300" r="4" fill="#142653"/><circle cx="500" cy="800" r="4" fill="#142653"/>
         <line x1="200" y1="200" x2="800" y2="300" stroke="#142653" strokeWidth="1"/><line x1="800" y1="300" x2="500" y2="800" stroke="#142653" strokeWidth="1"/><line x1="500" y1="800" x2="200" y2="200" stroke="#142653" strokeWidth="1"/>
      </svg>
  
      <div className="relative z-10 max-w-3xl px-6">
        <h2 className="text-6xl md:text-[84px] font-extrabold text-[#142653] tracking-tighter mb-6 leading-[1.05]">
          Your next research question<br/>starts here.
        </h2>
        <p className="text-2xl text-[#334155] font-medium mb-12">
          Discover papers. Understand evidence. Connect ideas. Build knowledge.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link to={isAuthenticated ? "/research" : "/register"} className="bg-[#142653] text-white text-lg font-bold px-10 py-5 rounded-full hover:-translate-y-1 hover:shadow-xl hover:shadow-[#142653]/20 transition-all inline-flex justify-center items-center gap-2">
            Start Researching <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </section>
  );
};

const Footer = () => (
  <footer className="bg-white border-t border-[#E6E1D8] py-12 relative z-10">
    <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
      <div className="flex items-center gap-2">
        <Atom className="w-5 h-5 text-[#142653]" />
        <span className="font-bold text-[#142653]">ResearchNexus AI</span>
        <span className="text-[#334155] text-sm ml-2">Research, understood.</span>
      </div>
      <div className="flex flex-wrap justify-center gap-6 text-sm font-medium text-[#334155]">
        <a href="#how-it-works" className="hover:text-[#142653] transition-colors">How It Works</a>
        <a href="#domains" className="hover:text-[#142653] transition-colors">Domains</a>
        <Link to="/research" className="hover:text-[#142653] transition-colors">Research Explorer</Link>
        <Link to="/login" className="hover:text-[#142653] transition-colors">Login</Link>
      </div>
    </div>
  </footer>
);



// --- MAIN PAGE ---

const LandingPage = () => {
  const [activeSection, setActiveSection] = useState<AtmosphereState>('hero');
  const [activeDomainId, setActiveDomainId] = useState('ai');
  
  return (
    <div className="bg-[#F8F8F5] text-[#142653] font-sans overflow-x-hidden selection:bg-[#8B6FF7]/20 relative">
      <ResearchAtmosphere activeSection={activeSection} activeDomainId={activeDomainId} />
      <div className="relative z-10">
        <FloatingNav />
        <motion.div onViewportEnter={() => setActiveSection('hero')} viewport={{ margin: "-20% 0px -20% 0px" }}><Hero /></motion.div>
        
        <motion.div onViewportEnter={() => setActiveSection('discover')}>
           <AlternatingJourney onSectionChange={setActiveSection} />
        </motion.div>

        <motion.div onViewportEnter={() => setActiveSection('domains')}>
           <CinematicCarousel onDomainChange={setActiveDomainId} />
        </motion.div>
        
        <motion.div onViewportEnter={() => setActiveSection('cta')}>
          <AudiencePanels />
        </motion.div>
        
        <motion.div onViewportEnter={() => setActiveSection('cta')} viewport={{ margin: "-20% 0px -20% 0px" }}><FinalCTA /></motion.div>
        <Footer />
      </div>
    </div>
  );
};

export default LandingPage;
