import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchMatches } from "../services/api";
import { MatchCard } from "../components/MatchList/MatchCard";

export function Home() {
  const [liveOnly, setLiveOnly] = useState(false);

  const { data: matches, isLoading, isError } = useQuery({
    queryKey: ["matches", liveOnly],
    queryFn: () => fetchMatches(liveOnly),
    refetchInterval: 15_000,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Filter Bar */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-white">Cricket Matches</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setLiveOnly(false)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              !liveOnly ? "bg-cricket-green text-white" : "bg-gray-800 text-gray-400 hover:text-white"
            }`}
          >
            All
          </button>
          <button
            onClick={() => setLiveOnly(true)}
            className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              liveOnly ? "bg-cricket-live text-white" : "bg-gray-800 text-gray-400 hover:text-white"
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
            <div key={i} className="bg-gray-900 rounded-xl border border-gray-800 h-44 animate-pulse" />
          ))}
        </div>
      )}

      {isError && (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg">Unable to load matches.</p>
          <p className="text-sm mt-1">Check your API connection.</p>
        </div>
      )}

      {matches && matches.length === 0 && (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg">{liveOnly ? "No live matches right now." : "No matches found."}</p>
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
