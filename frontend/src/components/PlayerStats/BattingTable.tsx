import type { BattingStats } from "../../types";

interface Props {
  data: BattingStats[];
  title?: string;
}

export function BattingTable({ data, title = "Batting" }: Props) {
  if (!data.length) return null;
  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-800">
        <h3 className="font-semibold text-white">{title}</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-xs text-gray-500 border-b border-gray-800">
              <th className="text-left px-4 py-2">Batsman</th>
              <th className="text-right px-3 py-2">R</th>
              <th className="text-right px-3 py-2">B</th>
              <th className="text-right px-3 py-2">4s</th>
              <th className="text-right px-3 py-2">6s</th>
              <th className="text-right px-3 py-2">SR</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-800/50 transition-colors">
                <td className="px-4 py-2.5 text-white font-medium">{row.batsman}</td>
                <td className="px-3 py-2.5 text-right font-bold tabular-nums">{row.runs}</td>
                <td className="px-3 py-2.5 text-right text-gray-400 tabular-nums">{row.balls}</td>
                <td className="px-3 py-2.5 text-right text-blue-400 tabular-nums">{row.fours}</td>
                <td className="px-3 py-2.5 text-right text-cricket-accent tabular-nums">{row.sixes}</td>
                <td className="px-3 py-2.5 text-right text-gray-300 tabular-nums">{row.strike_rate}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
