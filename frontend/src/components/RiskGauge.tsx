"use client";
import { useMemo } from "react";

export function RiskGauge({ score }: { score: number }) {
  const clamp = Math.max(0, Math.min(100, score));
  const angle = useMemo(() => (clamp / 100) * 180, [clamp]);
  const color = clamp < 40 ? "text-green-300" : clamp < 70 ? "text-yellow-300" : "text-red-300";

  return (
    <div className="glass rounded-xl p-6 flex flex-col items-center">
      <div className="relative w-56 h-28 overflow-hidden">
        <div
          className="absolute left-1/2 bottom-0 w-0.5 h-24 bg-indigo-300 origin-bottom"
          style={{ transform: `rotate(${angle - 90}deg)` }}
        />
        <div className="absolute inset-0 rounded-t-full bg-gradient-to-r from-green-500/30 via-yellow-500/30 to-red-500/30" />
        <div className="absolute inset-0 border-t border-indigo-400/30 rounded-t-full" />
      </div>
      <div className={`mt-4 text-3xl font-semibold ${color}`}>{clamp.toFixed(1)}%</div>
      <div className="text-slate-300">Risk Score</div>
    </div>
  );
}
