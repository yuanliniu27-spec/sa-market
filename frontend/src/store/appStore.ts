import { create } from 'zustand';

interface Application {
  id: string;
  name: string;
  display_name: string;
  description: string;
  type: string;
  category: string;
  icon_url?: string;
  publisher_name: string;
  rating_avg: number;
  install_count: number;
  created_at: string;
}

interface AppState {
  applications: Application[];
  currentApp: Application | null;
  loading: boolean;
  error: string | null;

  setApplications: (apps: Application[]) => void;
  setCurrentApp: (app: Application | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  applications: [],
  currentApp: null,
  loading: false,
  error: null,

  setApplications: (apps) => set({ applications: apps }),
  setCurrentApp: (app) => set({ currentApp: app }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
