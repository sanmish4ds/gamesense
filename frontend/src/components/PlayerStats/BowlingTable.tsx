import type { BowlingStats } from "../../types";

interface Props {
  data: BowlingStats[];
  title?: string;
}

export function BowlingTable({ data, title = "Bowling" }: Props) {
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
              <th className="text-left px-4 py-2">Bowler</th>
              <th className="text-right px-3 py-2">O</th>
              <th className="text-right px-3 py-2">R</th>
              <th className="text-right px-3 py-2">W</th>
              <th className="text-right px-3 py-2">Eco</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-800/50 transition-colors">
                <td className="px-4 py-2.5 text-white font-medium">{row.bowler}</td>
                <td className="px-3 py-2.5 text-right text-gray-400 tabular-nums">{row.overs}</td>
                <td className="px-3 py-2.5 text-right tabular-nums">{row.runs}</td>
                <td className="px-3 py-2.5 text-right font-bold text-cricket-live tabular-nums">{row.wickets}</td>
                <td className="px-3 py-2.5 text-right text-gray-300 tabular-nums">{row.economy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
