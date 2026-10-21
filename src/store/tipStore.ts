import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface TipState {
  seenTips: Record<string, boolean>;
  dismissTip: (tipId: string) => void;
  hasSeenTip: (tipId: string) => boolean;
}

export const useTipStore = create<TipState>()(
  persist(
    (set, get) => ({
      seenTips: {},
      dismissTip: (tipId) => set((state) => ({
        seenTips: { ...state.seenTips, [tipId]: true }
      })),
      hasSeenTip: (tipId) => {
        return !!get().seenTips[tipId];
      }
    }),
    {
      name: 'researchmind-tips',
    }
  )
);
