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
      className={clsx(
        "group block rounded-2xl border p-5 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-xl",
        match.is_live
          ? "bg-gradient-to-br from-cricket-dark/40 via-cricket-card to-cricket-card border-cricket-green/30 hover:border-cricket-green/60 hover:shadow-emerald-900/30"
          : "bg-cricket-card border-cricket-border hover:border-gray-600"
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <span className="text-[11px] font-semibold text-gray-500 uppercase tracking-wider bg-gray-800 px-2 py-0.5 rounded">
          {match.match_type ?? "Cricket"}
        </span>
        {match.is_live ? (
          <span className="flex items-center gap-1.5 text-xs font-bold text-cricket-live bg-cricket-live/10 border border-cricket-live/20 px-2.5 py-0.5 rounded-full">
            <span className="w-1.5 h-1.5 bg-cricket-live rounded-full animate-pulse" />
            LIVE
          </span>
        ) : match.match_winner ? (
          <span className="text-[11px] text-cricket-accent font-semibold">Completed</span>
        ) : (
          <span className="text-[11px] text-gray-600">Upcoming</span>
        )}
      </div>

      {/* Teams & Scores */}
      <div className="space-y-3">
        <TeamRow
          name={match.team1_name ?? "Team 1"}
          score={score1}
          isBatting={match.batting_team === match.team1_name}
        />
        <div className="border-t border-white/5" />
        <TeamRow
          name={match.team2_name ?? "Team 2"}
          score={score2}
          isBatting={match.batting_team === match.team2_name}
        />
      </div>

      {/* Footer */}
      <div className="mt-4 pt-3 border-t border-white/5 space-y-1">
        <p className="text-xs text-gray-400 line-clamp-1 font-medium">
          {match.match_winner ? `🏆 ${match.match_winner}` : match.status}
        </p>
        {match.venue && (
          <p className="text-[11px] text-gray-600 truncate">📍 {match.venue}</p>
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
    <div className="flex items-center justify-between gap-3">
      <div className="flex items-center gap-2 min-w-0">
        <div className={clsx(
          "w-2 h-2 rounded-full shrink-0 transition-all",
          isBatting ? "bg-cricket-green shadow-sm shadow-emerald-500/50" : "bg-gray-700"
        )} />
        <span className={clsx(
          "text-sm font-semibold truncate",
          isBatting ? "text-white" : "text-gray-400"
        )}>
          {name}
        </span>
      </div>
      {score ? (
        <div className="text-right shrink-0">
          <span className={clsx(
            "text-base font-black tabular-nums",
            isBatting ? "text-white" : "text-gray-500"
          )}>
            {score.runs}<span className="text-gray-600 font-normal">/</span>{score.wickets}
          </span>
          <span className="text-[11px] text-gray-600 ml-1.5">({score.overs} ov)</span>
        </div>
      ) : (
        <span className="text-xs text-gray-700 italic">yet to bat</span>
      )}
    </div>
  );
}
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
