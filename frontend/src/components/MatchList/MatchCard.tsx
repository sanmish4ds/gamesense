import { Link } from "react-router-dom";
import clsx from "clsx";
import type { Match } from "../../types";

interface Props {
  match: Match;
}

export function MatchCard({ match }: Props) {
  const score1 = match.score?.[0];
  const score2 = match.score?.[1];

  return (
    <Link
      to={`/match/${match.id}`}
      className="block bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-cricket-green transition-colors"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-gray-400 uppercase tracking-wide">{match.match_type ?? "Cricket"}</span>
        {match.is_live ? (
          <span className="flex items-center gap-1 text-xs font-semibold text-cricket-live">
            <span className="w-1.5 h-1.5 bg-cricket-live rounded-full animate-pulse" />
            LIVE
          </span>
        ) : (
          <span className="text-xs text-gray-500">{match.status?.slice(0, 30)}</span>
        )}
      </div>

      {/* Teams & Scores */}
      <div className="space-y-2">
        <TeamRow
          name={match.team1_name ?? "Team 1"}
          score={score1}
          isBatting={match.batting_team === match.team1_name}
        />
        <TeamRow
          name={match.team2_name ?? "Team 2"}
          score={score2}
          isBatting={match.batting_team === match.team2_name}
        />
      </div>

      {/* Footer */}
      <div className="mt-3 pt-3 border-t border-gray-800">
        <p className="text-xs text-gray-400 truncate">
          {match.match_winner ? `Result: ${match.match_winner}` : match.status}
        </p>
        {match.venue && (
          <p className="text-xs text-gray-600 truncate mt-0.5">{match.venue}</p>
        )}
      </div>
    </Link>
  );
}

function TeamRow({
  name,
  score,
  isBatting,
}: {
  name: string;
  score?: { runs: number; wickets: number; overs: number } | null;
  isBatting: boolean;
}) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 min-w-0">
        {isBatting && (
          <span className="w-1.5 h-1.5 bg-cricket-accent rounded-full shrink-0" />
        )}
        <span className={clsx("text-sm font-medium truncate", isBatting ? "text-white" : "text-gray-400")}>
          {name}
        </span>
      </div>
      {score ? (
        <span className={clsx("text-sm font-bold tabular-nums", isBatting ? "text-white" : "text-gray-400")}>
          {score.runs}/{score.wickets}
          <span className="text-xs font-normal ml-1 text-gray-500">({score.overs})</span>
        </span>
      ) : (
        <span className="text-xs text-gray-600">Yet to bat</span>
      )}
    </div>
  );
}
