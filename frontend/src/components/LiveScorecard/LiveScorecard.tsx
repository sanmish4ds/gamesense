import clsx from "clsx";
import type { Match, ScoreEntry } from "../../types";

interface Props {
  match: Match;
}

export function LiveScorecard({ match }: Props) {
  const scores = (match.score as ScoreEntry[] | null) ?? [];

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
      {/* Match Header */}
      <div className="bg-cricket-green px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-bold text-white leading-tight">{match.name}</h1>
          {match.is_live && (
            <span className="flex items-center gap-1.5 bg-cricket-live/20 border border-cricket-live text-cricket-live text-xs font-bold px-2 py-1 rounded-full">
              <span className="w-1.5 h-1.5 bg-cricket-live rounded-full animate-pulse" />
              LIVE
            </span>
          )}
        </div>
        {match.venue && (
          <p className="text-green-200 text-sm mt-1 truncate">{match.venue}</p>
        )}
      </div>

      {/* Score Blocks */}
      <div className="p-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {scores.map((s, i) => (
            <ScoreBlock
              key={i}
              score={s}
              isBatting={match.batting_team === s.inning?.replace(/ Inning \d/, "")}
            />
          ))}
        </div>

        {/* Status */}
        <div className="mt-4 p-3 bg-gray-800 rounded-lg">
          <p className="text-sm text-gray-300 text-center">
            {match.match_winner
              ? <span className="text-cricket-accent font-semibold">{match.match_winner}</span>
              : match.status}
          </p>
          {match.is_live && match.current_over != null && (
            <p className="text-xs text-gray-500 text-center mt-1">
              Over {match.current_over}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

function ScoreBlock({ score, isBatting }: { score: ScoreEntry; isBatting: boolean }) {
  const teamName = score.inning?.replace(/ Inning \d/, "") ?? score.inning;
  return (
    <div
      className={clsx(
        "rounded-lg p-4 border",
        isBatting
          ? "bg-cricket-green/10 border-cricket-green/40"
          : "bg-gray-800 border-gray-700"
      )}
    >
      <div className="flex items-center gap-2 mb-2">
        {isBatting && <span className="w-2 h-2 bg-cricket-accent rounded-full shrink-0" />}
        <p className="text-sm text-gray-400 truncate">{teamName}</p>
      </div>
      <p className="text-3xl font-bold tabular-nums text-white">
        {score.runs}
        <span className="text-gray-400">/{score.wickets}</span>
      </p>
      <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
        <span>{score.overs} ov</span>
        <span>CRR {score.run_rate}</span>
      </div>
    </div>
  );
}
