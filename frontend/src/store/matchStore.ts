import { create } from "zustand";
import type { Match, LiveMatchEvent } from "../types";

interface MatchStore {
  liveMatches: Match[];
  setLiveMatches: (matches: Match[]) => void;
  applyLiveEvent: (matchId: string, event: LiveMatchEvent) => void;
}

export const useMatchStore = create<MatchStore>((set) => ({
  liveMatches: [],

  setLiveMatches: (matches) => set({ liveMatches: matches }),

  applyLiveEvent: (matchId, event) =>
    set((state) => ({
      liveMatches: state.liveMatches.map((m) =>
        m.id === matchId
          ? {
              ...m,
              score: event.score ?? m.score,
              status: event.status ?? m.status,
              batting_team: event.batting_team ?? m.batting_team,
              bowling_team: event.bowling_team ?? m.bowling_team,
              current_over: event.current_over ?? m.current_over,
            }
          : m
      ),
    })),
}));
