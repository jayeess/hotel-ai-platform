"use client";
import axios from "axios";
import { useEffect, useState } from "react";
import { ForecastChart } from "@/components/ForecastChart";

const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ForecastPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await axios.get(`${api}/forecast`);
        setData(res.data);
      } catch (e) {
        console.error(e);
        setError("Failed to load forecast");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="glass rounded-xl p-6">Loading forecast...</div>;
  if (error) return <div className="glass rounded-xl p-6 text-red-300">{error}</div>;

  return (
    <ForecastChart
      observed={data.observed}
      forecast={data.forecast}
      ci={data.confidence_intervals}
    />
  );
}
