import axios from "axios";
import type { Match, FullScorecard, WormDataPoint, BattingStats, BowlingStats } from "../types";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const api = axios.create({ baseURL: `${BASE}/api/v1` });

export const fetchMatches = (liveOnly = false): Promise<Match[]> =>
  api.get("/matches", { params: { live_only: liveOnly } }).then((r) => r.data);

export const fetchLiveMatches = (): Promise<Match[]> =>
  api.get("/matches/live").then((r) => r.data);

export const fetchMatch = (id: string): Promise<Match> =>
  api.get(`/matches/${id}`).then((r) => r.data);

export const fetchScorecard = (id: string): Promise<FullScorecard> =>
  api.get(`/matches/${id}/scorecard`).then((r) => r.data);

export const fetchWormData = (id: string, innings = 1): Promise<{ data: WormDataPoint[] }> =>
  api.get(`/analytics/matches/${id}/worm`, { params: { innings } }).then((r) => r.data);

export const fetchBattingStats = (id: string, innings = 1): Promise<{ data: BattingStats[] }> =>
  api.get(`/analytics/matches/${id}/batting`, { params: { innings } }).then((r) => r.data);

export const fetchBowlingStats = (id: string, innings = 1): Promise<{ data: BowlingStats[] }> =>
  api.get(`/analytics/matches/${id}/bowling`, { params: { innings } }).then((r) => r.data);
