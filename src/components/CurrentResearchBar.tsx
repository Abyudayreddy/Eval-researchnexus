import { formatDistanceToNow } from 'date-fns';
import { ArrowRight, Brain, Leaf, Stethoscope, Briefcase, Globe, Cpu } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useResearchSessionStore } from '../store/researchSessionStore';

const domainIcons: Record<string, React.ReactNode> = {
  'Artificial Intelligence': <Brain className="h-4 w-4 text-purple-400" />,
  'Environment': <Leaf className="h-4 w-4 text-green-400" />,
  'Healthcare': <Stethoscope className="h-4 w-4 text-blue-400" />,
  'Business': <Briefcase className="h-4 w-4 text-amber-400" />,
  'Technology': <Cpu className="h-4 w-4 text-cyan-400" />,
  'General': <Globe className="h-4 w-4 text-slate-400" />,
};

export function CurrentResearchBar() {
  const navigate = useNavigate();
  const { activeTopicId, topics } = useResearchSessionStore();

  if (!activeTopicId) return null;

  const topic = topics[activeTopicId];
  if (!topic) return null;

  const icon = domainIcons[topic.domain] || domainIcons['General'];
  
  const handleContinue = () => {
    navigate(`/research-overview/${topic.id}`);
  };

  return (
    <div className="border-b border-white/5 bg-slate-900/50 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-screen-2xl mx-auto px-4 h-10 flex items-center justify-between text-sm">
        
        {/* Left Side: Domain and Topic */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 font-bold text-slate-100 text-xs tracking-widest uppercase">
            Current Research
          </div>
          <div className="h-3.5 w-px bg-white/20" />
          <div className="flex items-center gap-1.5 font-medium text-slate-300">
            {icon}
            <span>{topic.title || topic.domain}</span>
          </div>
        </div>

        {/* Right Side: Status and Action */}
        <div className="flex items-center gap-4">
          <div className="text-xs text-slate-500">
            Auto Saved {formatDistanceToNow(new Date(topic.autoSavedAt), { addSuffix: true })}
          </div>
          <button 
            onClick={handleContinue}
            className="flex items-center gap-1.5 text-blue-400 hover:text-blue-300 transition-colors text-xs font-medium bg-blue-500/10 hover:bg-blue-500/20 px-2 py-1 rounded-md"
          >
            Continue
            <ArrowRight className="h-3 w-3" />
          </button>
        </div>
        
      </div>
    </div>
  );
}
