export interface ScoreEntry {
  inning: string;
  runs: number;
  wickets: number;
  overs: number;
  run_rate: number;
}

export interface Match {
  id: string;
  name: string;
  match_type: string | null;
  status: string | null;
  venue: string | null;
  date: string | null;
  team1_name: string | null;
  team2_name: string | null;
  is_live: boolean;
  score: ScoreEntry[] | null;
  batting_team: string | null;
  bowling_team: string | null;
  current_over: number | null;
  match_winner: string | null;
  scorecard?: FullScorecard | null;
  updated_at?: string | null;
}

export interface FullScorecard {
  match_id: string;
  name: string;
  status: string | null;
  venue: string | null;
  match_type: string | null;
  is_live: boolean;
  teams: { team1: string | null; team2: string | null };
  batting_team: string | null;
  bowling_team: string | null;
  current_over: number | null;
  scores: ScoreEntry[];
  toss: Record<string, string> | null;
  match_winner: string | null;
  full_scorecard: Record<string, unknown> | null;
}

export interface WormDataPoint {
  over: number;
  cumulative_runs: number;
  over_runs: number;
}

export interface BattingStats {
  batsman: string;
  runs: number;
  balls: number;
  fours: number;
  sixes: number;
  strike_rate: number;
}

export interface BowlingStats {
  bowler: string;
  overs: number;
  runs: number;
  wickets: number;
  economy: number;
}

export interface LiveMatchEvent {
  type: string;
  match_id: string;
  score: ScoreEntry[] | null;
  status: string | null;
  batting_team: string | null;
  bowling_team: string | null;
  current_over: number | null;
}
