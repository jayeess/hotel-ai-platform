"use client";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Area,
} from "recharts";

type Point = { date: string; bookings: number; type: "observed" | "forecast" };
type CI = { date: string; lower: number; upper: number };

export function ForecastChart({
  observed,
  forecast,
  ci,
}: {
  observed: Point[];
  forecast: Point[];
  ci: CI[];
}) {
  const ciArea = ci.map((d) => ({ date: d.date, lower: d.lower, upper: d.upper }));

  return (
    <div className="glass rounded-xl p-6">
      <div className="text-indigo-200 font-semibold mb-4">12-Week Booking Outlook</div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area
            data={ciArea}
            dataKey="upper"
            stroke="#818CF8"
            fill="#818CF866"
            name="Confidence Upper"
          />
          <Area
            data={ciArea}
            dataKey="lower"
            stroke="#818CF8"
            fill="#818CF833"
            name="Confidence Lower"
          />
          <Line data={observed} dataKey="bookings" name="Observed" stroke="#22d3ee" />
          <Line data={forecast} dataKey="bookings" name="Forecast" stroke="#ef4444" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
