export interface SubDomain {
  name: string;
}

export type Dataset =
  | string
  | { name: string; size: string; type: string };

export type Topic =
  | string
  | { name: string; popularity: number; growth: string };

export type Paper =
  | string
  | { title: string; authors: string; year?: string; citations?: number; date?: string };

export type LearningStep = { title: string; desc: string; step?: string | number };

export interface DomainConfig {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  isOfflineAvailable: boolean;
  isOnlineAvailable: boolean;
  sourceBadge: 'Online + Offline' | 'Online';
  subdomains: SubDomain[];
  datasets: Dataset[];
  topics: Topic[];
  papers: Paper[];
  learningPath: LearningStep[];
  statistics: { label: string; value: string }[];
  heroGradient?: string;
  searchPlaceholder?: string;
  suggestedSearches?: string[];
  heroMetrics?: { label: string; value: string }[];
}

export const researchDomains: Record<string, DomainConfig> = {
  'artificial-intelligence': {
    id: 'artificial-intelligence',
    title: 'Artificial Intelligence',
    description: 'Explore the frontiers of artificial intelligence, machine learning, and cognitive computing.',
    icon: 'Brain',
    color: 'purple',
    isOfflineAvailable: true,
    isOnlineAvailable: true,
    sourceBadge: 'Online + Offline',
    subdomains: [
      { name: 'Machine Learning' },
      { name: 'Deep Learning' },
      { name: 'Retrieval-Augmented Generation (RAG)' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-indigo-900 via-purple-900 to-violet-900',
    searchPlaceholder: 'Search AI papers, LLMs, neural networks...',
    suggestedSearches: ['Large Language Models', 'Computer Vision', 'Agentic AI', 'Reinforcement Learning'],
    heroMetrics: [
      { label: 'Top Conference', value: 'NeurIPS' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'environmental-science': {
    id: 'environmental-science',
    title: 'Environmental Science',
    description: 'Research on climate, ecology, and environmental preservation.',
    icon: 'Globe',
    color: 'emerald',
    isOfflineAvailable: true,
    isOnlineAvailable: true,
    sourceBadge: 'Online + Offline',
    subdomains: [
      { name: 'Climate Change' },
      { name: 'Pollution Analysis' },
      { name: 'Sustainability' },
      { name: 'Water Resource Management' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-emerald-900 via-green-800 to-sky-900',
    searchPlaceholder: 'Search climate models, ecology, biodiversity...',
    suggestedSearches: ['Climate Change', 'Carbon Capture', 'Ecology', 'Biodiversity'],
    heroMetrics: [
      { label: 'Top Journal', value: 'Nature Env' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'interdisciplinary': {
    id: 'interdisciplinary',
    title: 'Interdisciplinary Research',
    description: 'Cross-domain research merging multiple scientific fields.',
    icon: 'LineChart',
    color: 'teal',
    isOfflineAvailable: true,
    isOnlineAvailable: true,
    sourceBadge: 'Online + Offline',
    subdomains: [
      { name: 'Smart Cities' },
      { name: 'Sustainable Development' },
      { name: 'Industry 4.0' },
      { name: 'Digital Twins' },
      { name: 'Green Computing' },
      { name: 'Computational Biology' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-indigo-900 via-teal-900 to-purple-900',
    searchPlaceholder: 'Search bioinformatics, neuro-symbolic AI...',
    suggestedSearches: ['Bioinformatics', 'Neuro-Symbolic AI', 'Computational Biology', 'Human-AI Collaboration'],
    heroMetrics: [
      { label: 'Top Journal', value: 'Nature Inter' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'data-science': {
    id: 'data-science',
    title: 'Data Science',
    description: 'Analytics, statistical modeling, and insights from large-scale data.',
    icon: 'Database',
    color: 'blue',
    isOfflineAvailable: false,
    isOnlineAvailable: true,
    sourceBadge: 'Online',
    subdomains: [
      { name: 'Data Analytics' },
      { name: 'Statistics' },
      { name: 'Big Data' },
      { name: 'Predictive Analytics' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-blue-900 via-cyan-900 to-sky-900',
    searchPlaceholder: 'Search predictive models, data mining, statistical analysis...',
    suggestedSearches: ['Data Mining', 'Predictive Analytics', 'Time Series', 'Feature Engineering'],
    heroMetrics: [
      { label: 'Top Conference', value: 'KDD' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'healthcare': {
    id: 'healthcare',
    title: 'Healthcare',
    description: 'Advancing medical science, diagnostics, and global health research.',
    icon: 'Stethoscope',
    color: 'rose',
    isOfflineAvailable: false,
    isOnlineAvailable: true,
    sourceBadge: 'Online',
    subdomains: [
      { name: 'Medical AI' },
      { name: 'Disease Prediction' },
      { name: 'Clinical Research' },
      { name: 'Drug Discovery' },
      { name: 'Biotechnology' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-emerald-900 via-teal-900 to-cyan-900',
    searchPlaceholder: 'Search clinical trials, genomics, medical imaging...',
    suggestedSearches: ['Medical Imaging', 'Genomics', 'Clinical Trials', 'Predictive Diagnostics'],
    heroMetrics: [
      { label: 'Top Journal', value: 'Lancet' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'materials-science': {
    id: 'materials-science',
    title: 'Materials Science',
    description: 'Research into new materials, nanomaterials, and metallurgy.',
    icon: 'Database',
    color: 'blue',
    isOfflineAvailable: false,
    isOnlineAvailable: true,
    sourceBadge: 'Online',
    subdomains: [
      { name: 'Nanomaterials' },
      { name: 'Biomaterials' },
      { name: 'Semiconductors' },
      { name: 'Polymers' },
      { name: 'Metallurgy' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-blue-900 via-indigo-900 to-purple-900',
    searchPlaceholder: 'Search nanomaterials, superconductors, polymers...',
    suggestedSearches: ['Nanotechnology', 'Superconductors', 'Biomaterials', 'Smart Materials'],
    heroMetrics: [
      { label: 'Top Journal', value: 'Nature Materials' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'energy': {
    id: 'energy',
    title: 'Energy',
    description: 'Advancements in renewable energy, power grids, and sustainable resources.',
    icon: 'Zap',
    color: 'amber',
    isOfflineAvailable: false,
    isOnlineAvailable: true,
    sourceBadge: 'Online',
    subdomains: [
      { name: 'Solar Energy' },
      { name: 'Wind Energy' },
      { name: 'Hydrogen Energy' },
      { name: 'Battery Technology' },
      { name: 'Smart Grids' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-orange-900 via-amber-800 to-yellow-900',
    searchPlaceholder: 'Search renewables, grid tech, solid state batteries...',
    suggestedSearches: ['Renewable Energy', 'Battery Storage', 'Smart Grid', 'Hydrogen Energy'],
    heroMetrics: [
      { label: 'Top Journal', value: 'Energy Sci' },
      { label: 'Latest Pub', value: '2025' }
    ]
  },
  'space-science': {
    id: 'space-science',
    title: 'Space Science',
    description: 'Exploration of astrophysics, astronomy, and aerospace technologies.',
    icon: 'Rocket',
    color: 'indigo',
    isOfflineAvailable: false,
    isOnlineAvailable: true,
    sourceBadge: 'Online',
    subdomains: [
      { name: 'Astronomy' },
      { name: 'Satellites' },
      { name: 'Astrophysics' },
      { name: 'Space Exploration' }
    ],
    datasets: [],
    topics: [],
    papers: [],
    learningPath: [],
    statistics: [],
    heroGradient: 'from-slate-900 via-violet-900 to-indigo-950',
    searchPlaceholder: 'Search astrophysics, orbital mechanics, planetary science...',
    suggestedSearches: ['Mars Exploration', 'Exoplanets', 'Satellite Imaging', 'Astrophysics'],
    heroMetrics: [
      { label: 'Top Journal', value: 'Astrophysics J' },
      { label: 'Latest Pub', value: '2025' }
    ]
  }
};
