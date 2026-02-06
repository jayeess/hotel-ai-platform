export default function Dashboard() {
  return (
    <div className="grid md:grid-cols-2 gap-6">
      <section className="glass rounded-xl p-6">
        <h2 className="text-xl font-semibold text-indigo-200">Welcome</h2>
        <p className="text-slate-300 mt-2">
          Explore predictions and 12-week forecasts. Use the top navigation to access pages.
        </p>
      </section>
      <section className="glass rounded-xl p-6">
        <h2 className="text-xl font-semibold text-indigo-200">Quick Links</h2>
        <div className="mt-4 flex flex-wrap gap-3">
          <a href="/prediction" className="glass px-4 py-2 rounded border border-indigo-400/30">Prediction</a>
          <a href="/forecast" className="glass px-4 py-2 rounded border border-indigo-400/30">Forecast</a>
          <a href="/history" className="glass px-4 py-2 rounded border border-indigo-400/30">History</a>
        </div>
      </section>
    </div>
  );
}
