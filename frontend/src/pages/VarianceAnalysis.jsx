import { useEffect, useState } from "react";

import api from "../services/api";

import VarianceTrendChart from "../components/VarianceTrendChart";
import RecurringOffenders from "../components/RecurringOffenders";
import CategoryRollups from "../components/CategoryRollups";
import VarianceNarrative from "../components/VarianceNarrative";

function VarianceAnalysis() {
  const [years, setYears] = useState([]);
  const [countries, setCountries] = useState([]);

  const [year, setYear] = useState(null);
  const [country, setCountry] = useState("");

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadFilterOptions();
  }, []);

  async function loadFilterOptions() {
    try {
      const { data } = await api.get("/api/financial/filters");

      const existingYears = (data.years || []).map((r) => r.year);
      const maxYear = existingYears.length ? Math.max(...existingYears) : new Date().getFullYear();

      setYears(existingYears);
      setCountries((data.countries || []).map((r) => r.country));
      setYear(maxYear);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (year) loadVariance();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [year, country]);

  async function loadVariance() {
    setLoading(true);
    setError(null);

    try {
      const { data } = await api.get("/api/variance", {
        params: {
          year,
          country: country || undefined,
        },
      });

      setData(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load variance analysis. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Variance Analysis</h1>
        <p className="text-slate-500 mt-2">
          Why are we off plan, and is it getting better or worse?
        </p>
      </div>

      <div className="bg-white rounded-xl shadow p-5 flex flex-wrap items-center gap-4">
        <select
          value={year || ""}
          onChange={(e) => setYear(Number(e.target.value))}
          className="border border-slate-200 rounded-lg px-4 py-2 text-sm"
        >
          {years.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>

        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="border border-slate-200 rounded-lg px-4 py-2 text-sm"
        >
          <option value="">All Countries</option>
          {countries.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="text-xl font-semibold text-slate-500">
          Loading Variance Analysis...
        </div>
      ) : error ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 rounded-xl p-6">
          {error}
        </div>
      ) : data && data.has_baseline === false ? (
        <div className="bg-amber-50 border border-amber-200 text-amber-800 rounded-xl p-6">
          <p className="font-semibold mb-1">No budget baseline available for {year}</p>
          <p className="text-sm">
            {year} has no prior year of actuals to build a budget from, so
            there's no meaningful plan to compare against. Variance analysis
            needs at least one year of history before it — try a later year,
            or set a Budget for {year} manually first.
          </p>
        </div>
      ) : (
        <>
          <VarianceNarrative narrative={data?.narrative} />

          <VarianceTrendChart data={data?.monthly_trend} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <RecurringOffenders offenders={data?.recurring_offenders} />
            <CategoryRollups rollups={data?.category_rollups} />
          </div>
        </>
      )}
    </div>
  );
}

export default VarianceAnalysis;
