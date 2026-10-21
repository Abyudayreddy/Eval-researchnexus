import { motion } from 'framer-motion';
import { 
  Brain, Cpu, Network, Bot, Code, Terminal,
  Database, LineChart, BarChart3, PieChart, Binary, ActivitySquare,
  Dna, Stethoscope, Activity, HeartPulse, Microscope, Syringe,
  Leaf, Sprout, Tractor, Droplets, Sun, Trees,
  Globe, Wind, CloudRain, Mountain, Waves, SunDim,
  Zap, Battery, Lightbulb, PlugZap, Flame,
  Rocket, Telescope, Orbit, Moon, Stars, Satellite,
  Link2, Share2, GitMerge, Workflow, Boxes, Hexagon
} from 'lucide-react';

interface DomainHeroBackgroundProps {
  domainId: string;
}

const floatingAnimation = {
  y: [0, -20, 0],
  transition: { duration: 7, repeat: Infinity, ease: "easeInOut" }
};

const floatingReverse = {
  y: [0, 20, 0],
  transition: { duration: 8, repeat: Infinity, ease: "easeInOut" }
};

const floatingHorizontal = {
  x: [0, 15, 0],
  transition: { duration: 9, repeat: Infinity, ease: "easeInOut" }
};

const pulseGlow = {
  opacity: [0.3, 0.6, 0.3],
  scale: [1, 1.1, 1],
  transition: { duration: 5, repeat: Infinity, ease: "easeInOut" }
};

const floatRotate = {
  y: [0, -15, 0],
  rotate: [0, 5, 0],
  transition: { duration: 10, repeat: Infinity, ease: "easeInOut" }
};

export default function DomainHeroBackground({ domainId }: DomainHeroBackgroundProps) {
  
  // Renders specific icons for each domain in a scattered layout
  const renderIcons = () => {
    switch(domainId) {
      case 'artificial-intelligence':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[15%] opacity-20 text-white"><Brain className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-10 right-[35%] opacity-15 text-white"><Network className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/2 right-[5%] opacity-15 text-white"><Cpu className="w-16 h-16" /></motion.div>
            <motion.div animate={floatRotate} className="absolute top-20 right-[40%] opacity-10 text-white"><Bot className="w-20 h-20" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute bottom-24 right-[15%] opacity-10 text-white"><Code className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingAnimation} className="absolute top-1/4 right-[25%] opacity-10 text-white"><Terminal className="w-12 h-12" /></motion.div>
          </>
        );
      case 'data-science':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-12 right-[20%] opacity-20 text-white"><Database className="w-28 h-28" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-16 right-[10%] opacity-15 text-white"><LineChart className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/4 right-[35%] opacity-10 text-white"><BarChart3 className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute bottom-10 right-[40%] opacity-15 text-white"><PieChart className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute top-10 right-[5%] opacity-10 text-white"><Binary className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute top-1/2 right-[25%] opacity-10 text-white"><ActivitySquare className="w-12 h-12" /></motion.div>
          </>
        );
      case 'healthcare':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[15%] opacity-20 text-white"><Dna className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-12 right-[30%] opacity-15 text-white"><Stethoscope className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/3 right-[5%] opacity-20 text-white"><HeartPulse className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute top-20 right-[45%] opacity-10 text-white"><Microscope className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute bottom-8 right-[10%] opacity-15 text-white"><Activity className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingAnimation} className="absolute bottom-1/3 right-[20%] opacity-10 text-white"><Syringe className="w-12 h-12" /></motion.div>
          </>
        );
      case 'materials-science':
        return (
          <>
            <div className="absolute -top-32 -left-32 w-[600px] h-[600px] bg-blue-500 rounded-full mix-blend-multiply filter blur-[100px] opacity-20 animate-blob"></div>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[20%] opacity-20 text-white"><Leaf className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-10 right-[10%] opacity-15 text-white"><Sprout className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/4 right-[35%] opacity-10 text-white"><Tractor className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute top-32 right-[5%] opacity-15 text-white"><Trees className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute bottom-20 right-[40%] opacity-10 text-white"><Droplets className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute top-10 right-[45%] opacity-10 text-white"><Sun className="w-16 h-16" /></motion.div>
          </>
        );

      case 'environmental-science':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-8 right-[15%] opacity-20 text-white"><Globe className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-16 right-[30%] opacity-15 text-white"><Wind className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/3 right-[5%] opacity-20 text-white"><CloudRain className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute bottom-10 right-[10%] opacity-15 text-white"><Mountain className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute top-10 right-[40%] opacity-10 text-white"><Waves className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingAnimation} className="absolute bottom-1/3 right-[45%] opacity-10 text-white"><SunDim className="w-16 h-16" /></motion.div>
          </>
        );
      case 'energy':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[15%] opacity-20 text-white"><Zap className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-12 right-[30%] opacity-15 text-white"><Battery className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/3 right-[5%] opacity-20 text-white"><Lightbulb className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute top-20 right-[40%] opacity-15 text-white"><Sun className="w-20 h-20" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute bottom-10 right-[10%] opacity-10 text-white"><PlugZap className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-1/4 right-[45%] opacity-10 text-white"><Flame className="w-12 h-12" /></motion.div>
          </>
        );
      case 'space-science':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-8 right-[20%] opacity-20 text-white"><Rocket className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-16 right-[10%] opacity-15 text-white"><Orbit className="w-28 h-28" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/4 right-[35%] opacity-15 text-white"><Telescope className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute top-24 right-[5%] opacity-15 text-white"><Stars className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute bottom-10 right-[40%] opacity-10 text-white"><Moon className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[45%] opacity-10 text-white"><Satellite className="w-12 h-12" /></motion.div>
          </>
        );
      case 'interdisciplinary':
        return (
          <>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[20%] opacity-20 text-white"><Link2 className="w-32 h-32" /></motion.div>
            <motion.div animate={floatingReverse} className="absolute bottom-12 right-[10%] opacity-15 text-white"><Share2 className="w-24 h-24" /></motion.div>
            <motion.div animate={pulseGlow} className="absolute top-1/3 right-[35%] opacity-15 text-white"><GitMerge className="w-20 h-20" /></motion.div>
            <motion.div animate={floatRotate} className="absolute top-20 right-[5%] opacity-15 text-white"><Workflow className="w-16 h-16" /></motion.div>
            <motion.div animate={floatingHorizontal} className="absolute bottom-10 right-[30%] opacity-10 text-white"><Boxes className="w-14 h-14" /></motion.div>
            <motion.div animate={floatingAnimation} className="absolute top-10 right-[45%] opacity-10 text-white"><Hexagon className="w-12 h-12" /></motion.div>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
      {/* Pattern Layer */}
      <div className="absolute inset-0 bg-[radial-gradient(#ffffff_1.5px,transparent_1.5px)] [background-size:32px_32px] opacity-[0.1]"></div>
      
      {/* Glow Layer */}
      <motion.div 
        animate={pulseGlow}
        className="absolute -right-20 -top-20 w-96 h-96 bg-white rounded-full blur-[120px] opacity-[0.08]" 
      />
      
      {/* Floating Elements / Icons */}
      <div className="hidden lg:block relative w-full h-full">
        {renderIcons()}
      </div>
    </div>
  );
}
