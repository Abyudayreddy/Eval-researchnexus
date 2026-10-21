import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { useToastStore } from './toastStore';

export type TopicStatus = 'Quick Search' | 'Research Started' | 'Active Research' | 'Completed Research' | 'Archived Research';

export interface TimelineEvent {
  id: string;
  timestamp: string;
  type: 'search' | 'bookmark' | 'note' | 'ai_chat' | 'literature_review' | 'xai';
  description: string;
  data?: any;
}

export interface ResearchTopic {
  id: string;
  title: string;
  domain: string;
  status: TopicStatus;
  selectedPapers: any[];
  aiConversations: any[];
  notes: any[];
  bookmarks: any[];
  literatureReviews: any[];
  timeline: TimelineEvent[];
  lastOpenedAt: string;
  autoSavedAt: string;
  
  // Restoration state
  restorationState?: {
    currentPage?: string;
    searchQuery?: string;
    activeFilters?: any;
  };
}

interface ResearchSessionState {
  activeTopicId: string | null;
  topics: Record<string, ResearchTopic>;
  xaiTraces: any[];
  activeTraceId: string | null;
  
  // Persistent state for Research Explorer so searches survive refresh
  searchExplorerState: {
    query: string;
    searchMode: 'hybrid' | 'semantic' | 'keyword';
    publicationYear: string | null;
    sortBy: string;
    hasSearched: boolean;
    results: any[];
  };
  
  // Actions
  setActiveTopic: (id: string | null) => void;
  addXaiTrace: (trace: any) => string;
  clearXaiHistory: () => void;
  setActiveTraceId: (id: string | null) => void;
  createAndSetActiveTopic: (topic: Partial<ResearchTopic>) => string;
  updateActiveTopic: (updates: Partial<ResearchTopic>) => void;
  addTimelineEvent: (event: Omit<TimelineEvent, 'id' | 'timestamp'>) => void;
  setSearchExplorerState: (updates: Partial<ResearchSessionState['searchExplorerState']>) => void;
  
  // High-level Auto-save intent trigger
  triggerMeaningfulAction: (actionType: TimelineEvent['type'], description: string, domainContext?: string, data?: any) => void;
}

const generateId = () => Math.random().toString(36).substring(2, 9);

export const useResearchSessionStore = create<ResearchSessionState>()(
  persist(
    (set, get) => ({
      activeTopicId: null,
      topics: {},
      xaiTraces: [],
      activeTraceId: null,
      
      searchExplorerState: {
        query: '',
        searchMode: 'hybrid',
        publicationYear: null,
        sortBy: 'relevance',
        hasSearched: false,
        results: []
      },

      setActiveTopic: (id) => set({ activeTopicId: id }),
      addXaiTrace: (trace) => {
        const newTrace = { ...trace, id: Math.random().toString(36).substring(2, 9), timestamp: new Date().toISOString() };
        set((state) => {
          // Deduplicate by query to prevent identical searches cluttering XAI history
          const filteredTraces = state.xaiTraces.filter(t => t.query !== trace.query);
          return { xaiTraces: [newTrace, ...filteredTraces].slice(0, 50) };
        });
        return newTrace.id;
      },
      clearXaiHistory: () => set({ xaiTraces: [] }),
      setActiveTraceId: (id) => set({ activeTraceId: id }),
      
      setSearchExplorerState: (updates) => set((state) => ({
        searchExplorerState: { ...state.searchExplorerState, ...updates }
      })),

      createAndSetActiveTopic: (topicInit) => {
        const id = topicInit.id || generateId();
        const now = new Date().toISOString();
        const newTopic: ResearchTopic = {
          id,
          title: topicInit.title || 'Untitled Research',
          domain: topicInit.domain || 'General',
          status: topicInit.status || 'Research Started',
          selectedPapers: topicInit.selectedPapers || [],
          aiConversations: topicInit.aiConversations || [],
          notes: topicInit.notes || [],
          bookmarks: topicInit.bookmarks || [],
          literatureReviews: topicInit.literatureReviews || [],
          timeline: topicInit.timeline || [],
          lastOpenedAt: now,
          autoSavedAt: now,
          ...topicInit,
        };

        set((state) => ({
          activeTopicId: id,
          topics: {
            ...state.topics,
            [id]: newTopic,
          }
        }));
        
        return id;
      },

      updateActiveTopic: (updates) => {
        const { activeTopicId, topics } = get();
        if (!activeTopicId) return;

        const currentTopic = topics[activeTopicId];
        set({
          topics: {
            ...topics,
            [activeTopicId]: {
              ...currentTopic,
              ...updates,
              autoSavedAt: new Date().toISOString(),
            }
          }
        });
      },

      addTimelineEvent: (eventInit) => {
        const { activeTopicId, topics } = get();
        if (!activeTopicId) return;

        const currentTopic = topics[activeTopicId];
        const newEvent: TimelineEvent = {
          ...eventInit,
          id: generateId(),
          timestamp: new Date().toISOString(),
        };

        set({
          topics: {
            ...topics,
            [activeTopicId]: {
              ...currentTopic,
              timeline: [...currentTopic.timeline, newEvent],
              autoSavedAt: new Date().toISOString(),
            }
          }
        });
      },

      triggerMeaningfulAction: (actionType, description, domainContext = 'General', data) => {
        const { activeTopicId, createAndSetActiveTopic, addTimelineEvent } = get();
        
        if (!activeTopicId) {
          // Auto-create a context based on meaningful intent
          createAndSetActiveTopic({
            title: `New ${domainContext} Research`,
            domain: domainContext,
            status: 'Research Started',
          });
          useToastStore.getState().addToast('Work automatically saved. You can continue this research later.', 'success');
        } else {
          useToastStore.getState().addToast('Progress saved automatically.', 'success');
        }
        
        addTimelineEvent({
          type: actionType,
          description,
          data
        });
      }
    }),
    {
      name: 'research-session-storage',
    }
  )
);
