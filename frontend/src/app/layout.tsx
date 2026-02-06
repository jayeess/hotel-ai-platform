"use client";
import "@/app/globals.css";
import { ReactNode, useEffect, useState } from "react";
import clsx from "clsx";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <Header />
        <main className="container mx-auto px-4 py-6">{children}</main>
      </body>
    </html>
  );
}

function Header() {
  const [dark, setDark] = useState(true);
  useEffect(() => {
    const saved = typeof window !== "undefined" ? localStorage.getItem("theme") : null;
    if (saved) setDark(saved === "dark");
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  return (
    <div className="gradient-ring">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-500/30 ring-1 ring-indigo-400/40" />
          <span className="text-lg font-semibold text-indigo-200">Hotel AI</span>
        </div>
        <div className="flex items-center gap-3">
          <a href="/" className="text-slate-300 hover:text-white">Dashboard</a>
          <a href="/prediction" className="text-slate-300 hover:text-white">Prediction</a>
          <a href="/forecast" className="text-slate-300 hover:text-white">Forecast</a>
          <a href="/history" className="text-slate-300 hover:text-white">History</a>
          <button
            onClick={() => {
              const next = !dark;
              setDark(next);
              localStorage.setItem("theme", next ? "dark" : "light");
            }}
            className={clsx(
              "glass px-3 py-1 rounded-md text-sm",
              "border-indigo-400/20 hover:border-indigo-400/40"
            )}
          >
            {dark ? "Dark" : "Light"}
          </button>
        </div>
      </div>
    </div>
  );
}
