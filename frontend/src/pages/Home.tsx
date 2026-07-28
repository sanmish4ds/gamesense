import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchMatches } from "../services/api";
import { MatchCard } from "../components/MatchList/MatchCard";

export function Home() {
  const [liveOnly, setLiveOnly] = useState(false);

  // Sync with ?live=true in URL
  useEffect(() => {
    setLiveOnly(window.location.search.includes("live=true"));
  }, []);

  const { data: matches, isLoading, isError } = useQuery({
    queryKey: ["matches", liveOnly],
    queryFn: () => fetchMatches(liveOnly),
    refetchInterval: 15_000,
  });

  const liveCount = matches?.filter((m) => m.is_live).length ?? 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-cricket-dark via-gray-900 to-gray-950 border border-cricket-border p-8">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_left,rgba(5,150,105,0.15),transparent_60%)]" />
        <div className="relative">
          <div className="flex items-center gap-2 mb-2">
            {liveCount > 0 && (
              <span className="flex items-center gap-1.5 text-xs text-cricket-live font-semibold bg-cricket-live/10 border border-cricket-live/20 px-2.5 py-1 rounded-full">
                <span className="w-1.5 h-1.5 bg-cricket-live rounded-full animate-pulse" />
                {liveCount} match{liveCount !== 1 ? "es" : ""} live
              </span>
            )}
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
            Live Cricket
            <span className="bg-gradient-to-r from-cricket-green to-emerald-400 bg-clip-text text-transparent"> Analytics</span>
          </h1>
          <p className="text-gray-400 mt-2 text-sm sm:text-base max-w-lg">
            Real-time scores, ball-by-ball analysis and deep match statistics — all in one place.
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white">
          {liveOnly ? "Live Matches" : "All Matches"}
          {matches && (
            <span className="ml-2 text-sm font-normal text-gray-500">
              ({matches.length})
            </span>
          )}
        </h2>
        <div className="flex gap-2 bg-gray-900 border border-cricket-border p-1 rounded-xl">
          <button
            onClick={() => setLiveOnly(false)}
            className={`px-4 py-1.5 rounded-lg text-sm font-semibold transition-all ${
              !liveOnly
                ? "bg-cricket-green text-white shadow"
                : "text-gray-400 hover:text-white"
            }`}
          >
            All
          </button>
          <button
            onClick={() => setLiveOnly(true)}
            className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-sm font-semibold transition-all ${
              liveOnly
                ? "bg-cricket-live text-white shadow"
                : "text-gray-400 hover:text-white"
            }`}
          >
            <span className="w-1.5 h-1.5 bg-current rounded-full animate-pulse" />
            Live
          </button>
        </div>
      </div>

      {/* Content */}
      {isLoading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-cricket-card border border-cricket-border rounded-2xl h-48 animate-pulse" />
          ))}
        </div>
      )}

      {isError && (
        <div className="text-center py-20 text-gray-500">
          <div className="text-4xl mb-3">⚠️</div>
          <p className="text-lg font-medium text-gray-400">Unable to load matches</p>
          <p className="text-sm mt-1">Check your API connection.</p>
        </div>
      )}

      {matches && matches.length === 0 && (
        <div className="text-center py-20 text-gray-500">
          <div className="text-4xl mb-3">🏏</div>
          <p className="text-lg font-medium text-gray-400">
            {liveOnly ? "No live matches right now." : "No matches found."}
          </p>
        </div>
      )}

      {matches && matches.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {matches.map((m) => (
            <MatchCard key={m.id} match={m} />
          ))}
        </div>
      )}
    </div>
  );
}
