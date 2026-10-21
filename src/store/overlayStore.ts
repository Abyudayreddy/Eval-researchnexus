import { create } from 'zustand';

type OverlayType = 
  | 'centered_sheet' 
  | 'side_drawer' 
  | 'action_sheet' 
  | 'confirmation_sheet' 
  | 'filter_drawer' 
  | null;

interface OverlayState {
  activeOverlay: OverlayType;
  overlayData: any; // payload for the active overlay
  
  openOverlay: (type: OverlayType, data?: any) => void;
  closeOverlay: () => void;
}

export const useOverlayStore = create<OverlayState>((set) => ({
  activeOverlay: null,
  overlayData: null,
  
  openOverlay: (type, data = null) => set({ activeOverlay: type, overlayData: data }),
  closeOverlay: () => set({ activeOverlay: null, overlayData: null }),
}));
