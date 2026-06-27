import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend,
} from "recharts";
import type { WormDataPoint } from "../../types";

interface Props {
  data: WormDataPoint[];
  title?: string;
}

export function WormChart({ data, title = "Run Progression (Worm)" }: Props) {
  if (!data.length) return null;
  return (
    <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
      <h3 className="font-semibold text-white mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="over" stroke="#6b7280" tick={{ fontSize: 11 }} label={{ value: "Over", position: "insideBottom", offset: -2, fill: "#6b7280", fontSize: 11 }} />
          <YAxis stroke="#6b7280" tick={{ fontSize: 11 }} />
          <Tooltip
            contentStyle={{ background: "#111827", border: "1px solid #374151", borderRadius: 8, color: "#f9fafb" }}
            labelFormatter={(v) => `Over ${v}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="cumulative_runs"
            stroke="#1a6b35"
            strokeWidth={2}
            dot={false}
            name="Cumulative Runs"
          />
          <Line
            type="monotone"
            dataKey="over_runs"
            stroke="#f59e0b"
            strokeWidth={1.5}
            dot={false}
            name="Runs per Over"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
