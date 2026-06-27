import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <nav className="bg-cricket-green border-b border-green-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/" className="flex items-center gap-2 font-bold text-xl text-white">
          <span className="text-2xl">🏏</span>
          <span>GameSense</span>
          <span className="text-xs bg-cricket-accent text-black px-1.5 py-0.5 rounded font-semibold ml-1">LIVE</span>
        </Link>
        <div className="flex gap-6 text-sm text-green-100">
          <Link to="/" className="hover:text-white transition-colors">Matches</Link>
          <Link to="/?live=true" className="hover:text-white transition-colors">Live</Link>
        </div>
      </div>
    </nav>
  );
}
