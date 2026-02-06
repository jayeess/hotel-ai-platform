"use client";
import axios from "axios";
import { useEffect, useState } from "react";

const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function HistoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get(`${api}/history?limit=100`);
        setItems(res.data.items || []);
      } catch (e) {
        console.error(e);
        setError("Failed to load history");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="glass rounded-xl p-6">Loading history...</div>;
  if (error) return <div className="glass rounded-xl p-6 text-red-300">{error}</div>;

  return (
    <div className="glass rounded-xl p-6">
      <div className="text-indigo-200 font-semibold mb-4">Recent Predictions</div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-slate-300">
              <th className="text-left p-2">Timestamp</th>
              <th className="text-left p-2">Risk</th>
              <th className="text-left p-2">Prediction</th>
              <th className="text-left p-2">Lead Time</th>
              <th className="text-left p-2">Room Type</th>
            </tr>
          </thead>
          <tbody>
            {items.map((it, i) => (
              <tr key={i} className="border-t border-indigo-400/10">
                <td className="p-2 text-slate-300">{new Date(it.timestamp).toLocaleString()}</td>
                <td className="p-2">{Math.round(it.probability * 100)}%</td>
                <td className="p-2">{it.prediction}</td>
                <td className="p-2">{it.payload.lead_time}</td>
                <td className="p-2">{it.payload.room_type_reserved}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
