import React, { useEffect, useState } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { researchDomains } from '../config/researchDomains';

export type AtmosphereState = 'hero' | 'discover' | 'understand' | 'organize' | 'capture' | 'build' | 'explain' | 'domains' | 'cta';

interface Props {
  activeSection: AtmosphereState;
  activeDomainId?: string; // used when in the domains section
}

export const ResearchAtmosphere: React.FC<Props> = ({ activeSection, activeDomainId }) => {
  const { scrollYProgress } = useScroll();
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);
    const listener = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mediaQuery.addEventListener('change', listener);
    return () => mediaQuery.removeEventListener('change', listener);
  }, []);

  // Parallax subtle shifts
  const yShift1 = useTransform(scrollYProgress, [0, 1], ['0%', '10%']);
  const yShift2 = useTransform(scrollYProgress, [0, 1], ['0%', '-5%']);

  // Dynamic Background Glows based on section
  const getBackgroundStyle = () => {
    switch (activeSection) {
      case 'discover': return { background: 'radial-gradient(circle at 30% 50%, rgba(139, 111, 247, 0.06) 0%, transparent 50%), radial-gradient(circle at 70% 60%, rgba(233, 122, 90, 0.04) 0%, transparent 50%)' };
      case 'understand': return { background: 'radial-gradient(circle at 40% 40%, rgba(139, 111, 247, 0.04) 0%, transparent 50%), radial-gradient(circle at 60% 70%, rgba(232, 121, 138, 0.06) 0%, transparent 50%)' };
      case 'organize': return { background: 'radial-gradient(circle at 50% 50%, rgba(233, 122, 90, 0.04) 0%, transparent 60%), radial-gradient(circle at 80% 30%, rgba(47, 143, 114, 0.04) 0%, transparent 50%)' };
      case 'capture': return { background: 'radial-gradient(circle at 50% 50%, rgba(233, 162, 59, 0.06) 0%, transparent 60%)' };
      case 'build': return { background: 'radial-gradient(circle at 20% 50%, rgba(59, 167, 160, 0.06) 0%, transparent 60%)' };
      case 'explain': return { background: 'radial-gradient(circle at 50% 50%, rgba(117, 100, 201, 0.06) 0%, transparent 60%)' };
      case 'domains': {
        const domain = activeDomainId ? researchDomains[activeDomainId] : researchDomains['ai'];
        return { background: `radial-gradient(circle at 50% 50%, ${domain.color}15 0%, transparent 60%)` };
      }
      case 'cta': return { background: 'radial-gradient(circle at 50% 50%, rgba(139, 111, 247, 0.06) 0%, transparent 40%), radial-gradient(circle at 30% 60%, rgba(59, 167, 160, 0.04) 0%, transparent 40%), radial-gradient(circle at 70% 40%, rgba(233, 122, 90, 0.04) 0%, transparent 40%)' };
      default: return { background: 'radial-gradient(circle at 20% 30%, rgba(139, 111, 247, 0.04) 0%, transparent 50%), radial-gradient(circle at 80% 60%, rgba(59, 167, 160, 0.03) 0%, transparent 50%)' };
    }
  };

  return (
    <div className="fixed inset-0 z-0 pointer-events-none overflow-hidden bg-[var(--bg-main)] transition-colors duration-200">
      {/* MEDIUM SCIENTIFIC GRID */}
      <motion.div 
        style={{ y: reducedMotion ? 0 : yShift1 }}
        className="absolute inset-0"
      >
        <div className="absolute inset-0" style={{ 
          backgroundImage: 'linear-gradient(to right, var(--animation-grid) 1px, transparent 1px), linear-gradient(to bottom, var(--animation-grid) 1px, transparent 1px)', 
          backgroundSize: '100px 100px' 
        }} />
        <div className="absolute inset-0" style={{ 
          backgroundImage: 'radial-gradient(circle at center, var(--animation-grid-dot) 1.5px, transparent 1.5px)', 
          backgroundSize: '100px 100px',
          backgroundPosition: '-1px -1px'
        }} />
      </motion.div>

      {/* Dynamic Gradients */}
      <motion.div 
        className="absolute inset-0 transition-all duration-1000 ease-in-out opacity-[var(--animation-opacity,0.5)]"
        style={getBackgroundStyle()}
      />

      {/* Domain Motifs Layer */}
      <motion.div style={{ y: reducedMotion ? 0 : yShift2 }} className="absolute inset-0 opacity-[var(--animation-opacity,0.6)]">
        <AnimatePresence mode="popLayout">
           {/* Render specific motifs based on activeSection/activeDomainId */}
           <AtmosphereRenderer key={sectionKey(activeSection, activeDomainId)} section={activeSection} activeDomainId={activeDomainId} />
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

const sectionKey = (section: string, domainId?: string) => section === 'domains' ? `domains-${domainId}` : section;

// --- Atmosphere Renderer ---
const AtmosphereRenderer = ({ section, activeDomainId }: { section: AtmosphereState, activeDomainId?: string }) => {
  // We constrain the visual intensity by only rendering a few elements at a time.
    if (section === 'hero') {
      return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
          {/* 5-6 specific outer scientific elements matching domains (Light to Medium Opacity) */}
          <NeuralNode x="12%" y="20%" scale={1.2} opacity={0.35} />
          <DNAHelix x="88%" y="25%" scale={1.2} opacity={0.35} />
          <OrbitalPath x="15%" y="75%" scale={1.3} opacity={0.35} />
          <DataPoints x="85%" y="70%" scale={1.4} opacity={0.35} />
          <EarthContour x="50%" y="10%" scale={1} opacity={0.3} />
          <EnergyPulse x="50%" y="85%" scale={1} opacity={0.3} />
        </motion.div>
      );
    }

  if (section === 'discover') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
        <NeuralNode x="20%" y="40%" />
        <DataPoints x="80%" y="60%" />
      </motion.div>
    );
  }

  if (section === 'understand') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
        <NeuralNode x="30%" y="30%" />
        <DNAHelix x="70%" y="50%" />
      </motion.div>
    );
  }

  if (section === 'organize') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
        <DataPoints x="20%" y="50%" />
        <LeafPattern x="80%" y="40%" />
      </motion.div>
    );
  }

  if (section === 'capture') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
        <EnergyPulse x="85%" y="50%" />
      </motion.div>
    );
  }

  if (section === 'build') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
        <KnowledgeGraph x="20%" y="60%" />
        <DataPoints x="80%" y="30%" />
      </motion.div>
    );
  }

  if (section === 'explain') {
    return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 1 }}>
        <EarthContour x="20%" y="30%" />
        <NeuralNode x="80%" y="70%" />
      </motion.div>
    );
  }


  if (section === 'domains') {
    // Render specific motif based on domain
    return (
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 1.05 }} transition={{ duration: 0.8 }}>
         {activeDomainId === 'ai' && <NeuralNode x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'data' && <DataPoints x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'healthcare' && <DNAHelix x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'agriculture' && <LeafPattern x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'environment' && <EarthContour x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'energy' && <EnergyPulse x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'space' && <OrbitalPath x="50%" y="50%" scale={2} opacity={0.1} />}
         {activeDomainId === 'interdisciplinary' && <KnowledgeGraph x="50%" y="50%" scale={2} opacity={0.1} />}
      </motion.div>
    );
  }

  if (section === 'cta') {
     return (
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 2 }}>
         {/* Convergence of motifs */}
         <NeuralNode x="20%" y="20%" opacity={0.05} />
         <DataPoints x="80%" y="20%" opacity={0.05} />
         <DNAHelix x="15%" y="80%" opacity={0.05} />
         <OrbitalPath x="85%" y="80%" opacity={0.05} />
      </motion.div>
     );
  }

  return null;
};

// --- Micro-Animations (Domain Motifs) ---
// Each is rendered as a clean SVG or minimal DOM elements. CSS transforms are used for cheap movement.

const NeuralNode = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="100" height="100" viewBox="0 0 100 100">
      <motion.circle cx="50" cy="50" r="10" fill="none" stroke="var(--animation-primary)" strokeWidth="1" initial={{ scale: 1 }} animate={{ scale: [1, 1.5, 1] }} transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }} />
      <circle cx="50" cy="50" r="4" fill="var(--animation-primary)" />
      <line x1="50" y1="50" x2="20" y2="20" stroke="var(--animation-primary)" strokeWidth="1" strokeDasharray="2 2" />
      <line x1="50" y1="50" x2="80" y2="30" stroke="var(--animation-primary)" strokeWidth="1" strokeDasharray="2 2" />
      <line x1="50" y1="50" x2="40" y2="80" stroke="var(--animation-primary)" strokeWidth="1" strokeDasharray="2 2" />
      <circle cx="20" cy="20" r="2" fill="var(--animation-primary)" />
      <circle cx="80" cy="30" r="2" fill="var(--animation-primary)" />
      <circle cx="40" cy="80" r="2" fill="var(--animation-primary)" />
    </svg>
  </div>
);

const DataPoints = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="120" height="80" viewBox="0 0 120 80">
      <path d="M10,70 L30,40 L50,60 L80,20 L110,30" fill="none" stroke="var(--animation-warm)" strokeWidth="1.5" strokeOpacity="0.5" />
      <motion.circle cx="10" cy="70" r="3" fill="var(--animation-warm)" animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 2, repeat: Infinity }} />
      <motion.circle cx="30" cy="40" r="3" fill="var(--animation-warm)" animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 2, repeat: Infinity, delay: 0.4 }} />
      <motion.circle cx="80" cy="20" r="3" fill="var(--animation-warm)" animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 2, repeat: Infinity, delay: 0.8 }} />
    </svg>
  </div>
);

const DNAHelix = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale}) rotate(45deg)`, opacity }}>
    <svg width="60" height="150" viewBox="0 0 60 150">
      <motion.path initial={{ d: "M10,10 Q50,45 10,80 T10,150" }} d="M10,10 Q50,45 10,80 T10,150" fill="none" stroke="var(--animation-accent)" strokeWidth="1.5" strokeOpacity="0.5" animate={{ d: ["M10,10 Q50,45 10,80 T10,150", "M30,10 Q70,45 30,80 T30,150", "M10,10 Q50,45 10,80 T10,150"] }} transition={{ duration: 6, repeat: Infinity, ease: 'linear' }} />
      <motion.path initial={{ d: "M50,10 Q10,45 50,80 T50,150" }} d="M50,10 Q10,45 50,80 T50,150" fill="none" stroke="var(--animation-accent)" strokeWidth="1.5" strokeOpacity="0.5" animate={{ d: ["M50,10 Q10,45 50,80 T50,150", "M30,10 Q-10,45 30,80 T30,150", "M50,10 Q10,45 50,80 T50,150"] }} transition={{ duration: 6, repeat: Infinity, ease: 'linear' }} />
    </svg>
  </div>
);

const LeafPattern = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="80" height="80" viewBox="0 0 80 80">
       <motion.path d="M40,70 Q40,40 15,25 Q40,15 65,25 Q40,40 40,70" fill="none" stroke="var(--animation-secondary)" strokeWidth="1.5" initial={{ scale: 1, rotate: 0 }} animate={{ scale: [1, 1.05, 1], rotate: [0, 5, 0] }} transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }} />
       <line x1="40" y1="70" x2="40" y2="35" stroke="var(--animation-secondary)" strokeWidth="1" />
    </svg>
  </div>
);

const EarthContour = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="100" height="100" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="40" fill="none" stroke="var(--animation-secondary)" strokeWidth="1" />
      <motion.path d="M20,35 Q50,15 80,35 M15,50 Q50,70 85,50 M25,70 Q50,85 75,70" fill="none" stroke="var(--animation-secondary)" strokeWidth="1" strokeOpacity="0.5" animate={{ y: [-2, 2, -2] }} transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }} />
    </svg>
  </div>
);

const EnergyPulse = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="80" height="80" viewBox="0 0 80 80">
       <polygon points="40,10 60,40 45,40 50,70 25,35 40,35" fill="none" stroke="var(--animation-warm)" strokeWidth="1.5" />
       <motion.circle cx="50" cy="70" r="2" fill="var(--animation-warm)" animate={{ opacity: [0, 1, 0], y: [0, -10, -20] }} transition={{ duration: 2, repeat: Infinity }} />
    </svg>
  </div>
);

const OrbitalPath = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="120" height="120" viewBox="0 0 120 120">
      <ellipse cx="60" cy="60" rx="50" ry="20" fill="none" stroke="var(--animation-primary)" strokeWidth="1" transform="rotate(-30 60 60)" />
      <ellipse cx="60" cy="60" rx="50" ry="20" fill="none" stroke="var(--animation-primary)" strokeWidth="1" strokeOpacity="0.4" transform="rotate(30 60 60)" />
      <circle cx="60" cy="60" r="8" fill="var(--animation-primary)" />
      <motion.circle cx="10" cy="60" r="3" fill="var(--animation-primary)" animate={{ rotate: 360 }} style={{ originX: '50px', originY: '0' }} transition={{ duration: 10, repeat: Infinity, ease: 'linear' }} />
    </svg>
  </div>
);

const KnowledgeGraph = ({ x, y, scale = 1, opacity = 0.15 }: any) => (
  <div className="absolute" style={{ left: x, top: y, transform: `translate(-50%, -50%) scale(${scale})`, opacity }}>
    <svg width="100" height="100" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="4" fill="var(--animation-secondary)" />
      <line x1="50" y1="50" x2="20" y2="30" stroke="var(--animation-secondary)" strokeWidth="1" strokeOpacity="0.5" />
      <line x1="50" y1="50" x2="80" y2="20" stroke="var(--animation-warm)" strokeWidth="1" strokeOpacity="0.5" />
      <line x1="50" y1="50" x2="70" y2="80" stroke="var(--animation-primary)" strokeWidth="1" strokeOpacity="0.5" />
      <line x1="50" y1="50" x2="30" y2="70" stroke="var(--animation-accent)" strokeWidth="1" strokeOpacity="0.5" />
      <circle cx="20" cy="30" r="3" fill="var(--animation-secondary)" />
      <circle cx="80" cy="20" r="3" fill="var(--animation-warm)" />
      <circle cx="70" cy="80" r="3" fill="var(--animation-primary)" />
      <circle cx="30" cy="70" r="3" fill="var(--animation-accent)" />
    </svg>
  </div>
);
