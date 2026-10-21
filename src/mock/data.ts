export interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  publishDate: string;
  citations: number;
  tags: string[];
  url: string;
}

export const mockPapers: Paper[] = [
  {
    id: "p1",
    title: "Generative Agents: Interactive Simulacra of Human Behavior",
    authors: ["Joon Sung Park", "Joseph C. O'Brien", "Carrie J. Cai"],
    abstract: "Believable proxies of human behavior can empower interactive applications...",
    publishDate: "2023-04-07",
    citations: 423,
    tags: ["LLM", "Agents", "Simulation"],
    url: "https://arxiv.org/abs/2304.03442"
  },
  {
    id: "p2",
    title: "Attention Is All You Need",
    authors: ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
    abstract: "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
    publishDate: "2017-06-12",
    citations: 84000,
    tags: ["Transformers", "NLP", "Core"],
    url: "https://arxiv.org/abs/1706.03762"
  }
];

export interface Project {
  id: string;
  name: string;
  lastModified: string;
  paperCount: number;
}

export const mockProjects: Project[] = [
  { id: "proj1", name: "LLM Agent Architecture", lastModified: "2 hours ago", paperCount: 12 },
  { id: "proj2", name: "Transformer Scaling Laws", lastModified: "1 day ago", paperCount: 8 }
];
