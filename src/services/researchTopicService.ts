import { api } from '../utils/api';
import toolkitJson from '../data/research_review_toolkit.json';

export interface DynamicResearchTopic {
  id: string;
  title: string;
  query: string;
  domain: string;
  domainId: string;
  sourceBadge: 'Online + Offline' | 'Online';
  paperCount?: number;
  trendingTag?: string;
}

// 8 Supported Canonical Domains
export const RESEARCH_DOMAINS = [
  { id: 'artificial-intelligence', name: 'Artificial Intelligence', sourceBadge: 'Online + Offline' as const },
  { id: 'environmental-science', name: 'Environmental Science', sourceBadge: 'Online + Offline' as const },
  { id: 'interdisciplinary', name: 'Interdisciplinary Research', sourceBadge: 'Online + Offline' as const },
  { id: 'data-science', name: 'Data Science', sourceBadge: 'Online' as const },
  { id: 'healthcare', name: 'Healthcare', sourceBadge: 'Online' as const },
  { id: 'materials-science', name: 'Materials Science', sourceBadge: 'Online' as const },
  { id: 'energy', name: 'Energy', sourceBadge: 'Online' as const },
  { id: 'space-science', name: 'Space Science', sourceBadge: 'Online' as const }
];

// Fallback high-quality queries derived strictly from known-good ResearchReviewToolkit questions
const TOOLKIT_SCENARIOS = (toolkitJson as any).scenarios || [];

/**
 * Deterministic pseudo-random number based on a seed string (e.g. today's date "YYYY-MM-DD")
 */
function seededRandom(seed: string): () => number {
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = (hash << 5) - hash + seed.charCodeAt(i);
    hash |= 0;
  }
  return () => {
    hash = (hash * 9301 + 49297) % 233280;
    return Math.abs(hash / 233280);
  };
}

/**
 * Get Today's ISO date string (YYYY-MM-DD)
 */
export function getTodayDateString(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

/**
 * Fetch and construct dynamic research topics derived from:
 * 1. Verified domain papers in active corpora (API)
 * 2. Real research questions and concepts from research_review_toolkit.json
 * Refreshes deterministically daily using localStorage cache.
 */
export async function getDynamicResearchTopics(): Promise<{
  tryExamples: DynamicResearchTopic[];
  popularStarters: DynamicResearchTopic[];
}> {
  const today = getTodayDateString();
  const cacheKey = `rn_dynamic_topics_${today}`;

  try {
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      const parsed = JSON.parse(cached);
      if (parsed.tryExamples && parsed.popularStarters) {
        return parsed;
      }
    }
  } catch (e) {
    console.warn('Could not read cached dynamic topics', e);
  }

  const rng = seededRandom(today);

  // Group verified toolkit scenarios by domain
  const scenariosByDomain: Record<string, any[]> = {};
  for (const sc of TOOLKIT_SCENARIOS) {
    const dName = sc.domain || 'Artificial Intelligence';
    if (!scenariosByDomain[dName]) scenariosByDomain[dName] = [];
    scenariosByDomain[dName].push(sc);
  }

  // Build high-relevance topics across multiple domains
  const generatedStarters: DynamicResearchTopic[] = [];

  // 1. Check domain counts if accessible from backend
  let domainCounts: Record<string, number> = {};
  try {
    const countsResp = await api.papers.getDomainCounts();
    if (countsResp && typeof countsResp === 'object') {
      domainCounts = countsResp;
    }
  } catch (err) {
    // Offline or server not responding to domain-counts, use default
  }

  // Construct diverse candidates across domains
  for (const dom of RESEARCH_DOMAINS) {
    const matchingScenarios = scenariosByDomain[dom.name] || scenariosByDomain[dom.id] || [];
    if (matchingScenarios.length > 0) {
      // Pick deterministic index for today
      const idx = Math.floor(rng() * matchingScenarios.length);
      const chosen = matchingScenarios[idx];
      generatedStarters.push({
        id: `topic_${dom.id}_${today}`,
        title: chosen.title || chosen.question.slice(0, 40),
        query: chosen.question,
        domain: dom.name,
        domainId: dom.id,
        sourceBadge: dom.sourceBadge,
        paperCount: domainCounts[dom.id] || domainCounts[dom.name] || undefined,
        trendingTag: chosen.tags?.[0] || 'Research'
      });
    } else {
      // Create grounded topic from domain title
      generatedStarters.push({
        id: `topic_${dom.id}_${today}`,
        title: `${dom.name} Methodologies`,
        query: `${dom.name} research methods and foundational papers`,
        domain: dom.name,
        domainId: dom.id,
        sourceBadge: dom.sourceBadge,
        paperCount: domainCounts[dom.id] || undefined
      });
    }
  }

  // Shuffle deterministically
  const shuffled = [...generatedStarters].sort(() => rng() - 0.5);

  const tryExamples = shuffled.slice(0, 4);
  const popularStarters = shuffled.slice(0, 8);

  const result = { tryExamples, popularStarters };

  try {
    localStorage.setItem(cacheKey, JSON.stringify(result));
  } catch (e) {
    // ignore quota errors
  }

  return result;
}
