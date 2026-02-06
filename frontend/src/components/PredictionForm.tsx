"use client";
import { useState } from "react";
import axios from "axios";
import { RiskGauge } from "@/components/RiskGauge";

const TOOLTIP: Record<string, string> = {
  lead_time: "Days between booking date and arrival date",
  room_type_reserved: "Selected room category at booking time",
  avg_price_per_room: "Average price per night for the room",
  no_of_special_requests: "Number of special requests such as high floor",
};

const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function PredictionForm() {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ risk_score: number; prediction: string } | null>(null);

  const [form, setForm] = useState({
    no_of_adults: 2,
    no_of_children: 0,
    no_of_weekend_nights: 1,
    no_of_week_nights: 2,
    type_of_meal_plan: "Meal Plan 1",
    required_car_parking_space: 0,
    room_type_reserved: "Room_Type 1",
    lead_time: 30,
    arrival_year: 2018,
    arrival_month: 8,
    arrival_date: 12,
    market_segment_type: "Online",
    repeated_guest: 0,
    no_of_previous_cancellations: 0,
    no_of_previous_bookings_not_canceled: 0,
    avg_price_per_room: 100,
    no_of_special_requests: 0,
  });

  async function submit() {
    setLoading(true);
    try {
      const res = await axios.post(`${api}/predict`, form);
      setResult({ risk_score: res.data.risk_score, prediction: res.data.prediction });
    } catch (e) {
      console.error(e);
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  function Field({
    name,
    children,
  }: {
    name: keyof typeof form;
    children: React.ReactNode;
  }) {
    return (
      <div className="mb-4">
        <div className="flex items-center justify-between">
          <label className="text-slate-200">{name}</label>
          {TOOLTIP[name] && <span className="tooltip">{TOOLTIP[name]}</span>}
        </div>
        {children}
      </div>
    );
  }

  const steps = [
    <>
      <Field name="lead_time">
        <input
          type="number"
          className="glass w-full rounded px-3 py-2"
          value={form.lead_time}
          onChange={(e) => setForm({ ...form, lead_time: Number(e.target.value) })}
        />
      </Field>
      <Field name="avg_price_per_room">
        <input
          type="number"
          className="glass w-full rounded px-3 py-2"
          value={form.avg_price_per_room}
          onChange={(e) => setForm({ ...form, avg_price_per_room: Number(e.target.value) })}
        />
      </Field>
    </>,
    <>
      <Field name="room_type_reserved">
        <select
          className="glass w-full rounded px-3 py-2"
          value={form.room_type_reserved}
          onChange={(e) => setForm({ ...form, room_type_reserved: e.target.value })}
        >
          {["Room_Type 1", "Room_Type 2", "Room_Type 3", "Room_Type 4", "Room_Type 5", "Room_Type 6", "Room_Type 7"].map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </Field>
      <Field name="type_of_meal_plan">
        <select
          className="glass w-full rounded px-3 py-2"
          value={form.type_of_meal_plan}
          onChange={(e) => setForm({ ...form, type_of_meal_plan: e.target.value })}
        >
          {["Meal Plan 1", "Meal Plan 2", "Meal Plan 3", "Not Selected"].map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </Field>
    </>,
    <>
      <Field name="no_of_special_requests">
        <input
          type="number"
          className="glass w-full rounded px-3 py-2"
          value={form.no_of_special_requests}
          onChange={(e) => setForm({ ...form, no_of_special_requests: Number(e.target.value) })}
        />
      </Field>
      <Field name="market_segment_type">
        <select
          className="glass w-full rounded px-3 py-2"
          value={form.market_segment_type}
          onChange={(e) => setForm({ ...form, market_segment_type: e.target.value })}
        >
          {["Aviation", "Complementary", "Corporate", "Offline", "Online"].map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </Field>
    </>,
  ];

  return (
    <div className="glass rounded-xl p-6">
      <div className="text-indigo-200 font-semibold mb-4">Prediction Form</div>
      {steps[step]}
      <div className="mt-4 flex justify-between">
        <button
          className="glass px-4 py-2 rounded border border-indigo-400/30"
          disabled={step === 0}
          onClick={() => setStep((s) => Math.max(0, s - 1))}
        >
          Back
        </button>
        {step < steps.length - 1 ? (
          <button
            className="glass px-4 py-2 rounded border border-indigo-400/30"
            onClick={() => setStep((s) => Math.min(steps.length - 1, s + 1))}
          >
            Next
          </button>
        ) : (
          <button
            className="glass px-4 py-2 rounded border border-indigo-400/30"
            onClick={submit}
            disabled={loading}
          >
            {loading ? "Predicting..." : "Predict"}
          </button>
        )}
      </div>
      {result && (
        <div className="mt-6 grid md:grid-cols-2 gap-4">
          <RiskGauge score={result.risk_score} />
          <div className="glass rounded-xl p-6">
            <div className="text-slate-300">Prediction</div>
            <div className="text-2xl font-semibold text-indigo-200">{result.prediction}</div>
          </div>
        </div>
      )}
    </div>
  );
}
