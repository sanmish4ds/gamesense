import { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchMatch, fetchWormData, fetchBattingStats, fetchBowlingStats } from "../services/api";
import { useMatchWebSocket } from "../hooks/useMatchWebSocket";
import { LiveScorecard } from "../components/LiveScorecard/LiveScorecard";
import { BattingTable } from "../components/PlayerStats/BattingTable";
import { BowlingTable } from "../components/PlayerStats/BowlingTable";
import { WormChart } from "../components/BallByBall/WormChart";
import type { LiveMatchEvent, Match } from "../types";

type Tab = "scorecard" | "batting" | "bowling" | "analytics";

export function MatchDetail() {
  const { matchId } = useParams<{ matchId: string }>();
  const [innings, setInnings] = useState(1);
  const [tab, setTab] = useState<Tab>("scorecard");
  const qc = useQueryClient();

  const { data: match, isLoading } = useQuery({
    queryKey: ["match", matchId],
    queryFn: () => fetchMatch(matchId!),
    enabled: !!matchId,
    refetchInterval: 30_000,
  });

  const { data: worm } = useQuery({
    queryKey: ["worm", matchId, innings],
    queryFn: () => fetchWormData(matchId!, innings),
    enabled: !!matchId && tab === "analytics",
  });

  const { data: batting } = useQuery({
    queryKey: ["batting", matchId, innings],
    queryFn: () => fetchBattingStats(matchId!, innings),
    enabled: !!matchId && tab === "batting",
  });

  const { data: bowling } = useQuery({
    queryKey: ["bowling", matchId, innings],
    queryFn: () => fetchBowlingStats(matchId!, innings),
    enabled: !!matchId && tab === "bowling",
  });

  // WebSocket live updates — patch the cached match
  useMatchWebSocket(match?.is_live ? matchId : undefined, (event: LiveMatchEvent) => {
    qc.setQueryData<Match>(["match", matchId], (prev) =>
      prev
        ? {
            ...prev,
            score: (event.score as Match["score"]) ?? prev.score,
            status: event.status ?? prev.status,
            batting_team: event.batting_team ?? prev.batting_team,
            bowling_team: event.bowling_team ?? prev.bowling_team,
            current_over: event.current_over ?? prev.current_over,
          }
        : prev
    );
  });

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-4">
        <div className="h-48 bg-gray-900 rounded-xl animate-pulse" />
        <div className="h-32 bg-gray-900 rounded-xl animate-pulse" />
      </div>
    );
  }

  if (!match) {
    return <div className="text-center py-16 text-gray-500">Match not found.</div>;
  }

  const TABS: { key: Tab; label: string }[] = [
    { key: "scorecard", label: "Scorecard" },
    { key: "batting", label: "Batting" },
    { key: "bowling", label: "Bowling" },
    { key: "analytics", label: "Analytics" },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
      <LiveScorecard match={match} />

      {/* Innings Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-500 mr-1">Innings:</span>
        {[1, 2].map((i) => (
          <button
            key={i}
            onClick={() => setInnings(i)}
            className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
              innings === i ? "bg-cricket-green text-white" : "bg-gray-800 text-gray-400"
            }`}
          >
            {i}st {i === 1 ? "" : "nd"}
          </button>
        ))}
      </div>

      {/* Tab Bar */}
      <div className="flex border-b border-gray-800">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              tab === t.key
                ? "border-cricket-green text-cricket-green"
                : "border-transparent text-gray-400 hover:text-white"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div>
        {tab === "scorecard" && (
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
            {match.scorecard?.full_scorecard ? (
              <pre className="text-xs text-gray-300 overflow-auto max-h-96">
                {JSON.stringify(match.scorecard.full_scorecard, null, 2)}
              </pre>
            ) : (
              <p className="text-gray-500 text-sm text-center py-8">
                Detailed scorecard not yet available.
              </p>
            )}
          </div>
        )}

        {tab === "batting" && (
          <BattingTable data={batting?.data ?? []} title={`Batting — Innings ${innings}`} />
        )}

        {tab === "bowling" && (
          <BowlingTable data={bowling?.data ?? []} title={`Bowling — Innings ${innings}`} />
        )}

        {tab === "analytics" && (
          <WormChart data={worm?.data ?? []} title={`Worm Chart — Innings ${innings}`} />
        )}
      </div>
    </div>
  );
}
