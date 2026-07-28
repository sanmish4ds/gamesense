import { Link, useLocation } from "react-router-dom";

export function Navbar() {
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 border-b border-cricket-border bg-gray-950/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cricket-green to-cricket-dark flex items-center justify-center shadow-lg shadow-emerald-900/40">
            <span className="text-xl leading-none">🏏</span>
          </div>
          <span className="font-black text-xl tracking-tight bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
            SportWire
          </span>
          <span className="hidden sm:inline-flex items-center gap-1 text-[10px] bg-cricket-live/10 text-cricket-live border border-cricket-live/30 px-2 py-0.5 rounded-full font-bold tracking-widest">
            <span className="w-1.5 h-1.5 bg-cricket-live rounded-full animate-pulse" />
            LIVE
          </span>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-1 text-sm">
          <Link
            to="/"
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              location.pathname === "/" && !location.search.includes("live")
                ? "text-white bg-white/10"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            }`}
          >
            Matches
          </Link>
          <Link
            to="/?live=true"
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg font-medium transition-colors ${
              location.search.includes("live")
                ? "text-cricket-live bg-cricket-live/10"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            }`}
          >
            <span className="w-1.5 h-1.5 bg-cricket-live rounded-full animate-pulse" />
            Live
          </Link>
        </div>
      </div>
    </nav>
  );
}
