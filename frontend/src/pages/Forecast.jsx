import { useEffect, useMemo, useState } from "react";

import api from "../services/api";

import ForecastKPICards from "../components/ForecastKPICards";
import ForecastChart from "../components/ForecastChart";
import ForecastAssumptions from "../components/ForecastAssumptions";

const REVENUE_ACCOUNTS = ["Sales"];
const SALES_RETURN_ACCOUNT = "Sales Return";
const EXPENSE_ACCOUNTS = [
  "Cost of Sales", "Staff Costs", "Commissions", "Advertisements", "Travel",
  "Entertainment", "Office Supplies", "Professional Services", "Telephone",
  "Utilities", "Other Expenses", "Equipment", "Amortization of Intangible Assets",
  "Interest Expense", "Taxation",
];
const NON_OPERATING_ACCOUNTS = [
  "Interest Income", "Dividend Income", "Gain/Loss on Sales of Asset", "Exchange Loss/Gain",
];

function sumByAccounts(rows, accounts, valueKey) {
  return rows
    .filter((r) => accounts.includes(r.account))
    .reduce((s, r) => s + (r[valueKey] || 0), 0);
}

function Forecast() {
  const [years, setYears] = useState([]);
  const [countries, setCountries] = useState([]);

  const [year, setYear] = useState(null);
  const [country, setCountry] = useState("");
  const [growthOverride, setGrowthOverride] = useState("");

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

      setYears([...existingYears, maxYear + 1]);
      setCountries((data.countries || []).map((r) => r.country));
      setYear(maxYear + 1);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (year) loadForecast();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [year, country]);

  async function loadForecast() {
    setLoading(true);
    setError(null);

    try {
      const params = {
        year,
        country: country || undefined,
      };

      if (growthOverride !== "") {
        params.growth_rate_override = Number(growthOverride) / 100;
      }

      const { data } = await api.get("/api/forecast", { params });

      setData(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load the forecast. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  // Aggregate per-month Revenue/Expenses/Profit for both historical
  // and forecast rows, then merge into one continuous chart dataset.
  const chartData = useMemo(() => {
    if (!data || !data.has_history) return [];

    const byMonth = (rows, monthNumber) => rows.filter((r) => r.month_number === monthNumber);

    const historical = [];
    for (let m = 1; m <= 12; m++) {
      const rows = byMonth(data.historical, m);
      const revenue = sumByAccounts(rows, REVENUE_ACCOUNTS, "actual") - sumByAccounts(rows, [SALES_RETURN_ACCOUNT], "actual");
      const expenses = sumByAccounts(rows, EXPENSE_ACCOUNTS, "actual");
      const nonOperating = sumByAccounts(rows, NON_OPERATING_ACCOUNTS, "actual");
      historical.push({
        label: `${rows[0]?.month || m} '${String(data.base_year).slice(-2)}`,
        actualRevenue: revenue,
        actualExpenses: expenses,
        actualProfit: revenue - expenses + nonOperating,
        forecastRevenue: null,
        forecastExpenses: null,
        forecastProfit: null,
      });
    }

    const forecast = [];
    for (let m = 1; m <= 12; m++) {
      const rows = byMonth(data.forecast, m);
      const revenue = sumByAccounts(rows, REVENUE_ACCOUNTS, "forecast") - sumByAccounts(rows, [SALES_RETURN_ACCOUNT], "forecast");
      const expenses = sumByAccounts(rows, EXPENSE_ACCOUNTS, "forecast");
      const nonOperating = sumByAccounts(rows, NON_OPERATING_ACCOUNTS, "forecast");
      forecast.push({
        label: `${rows[0]?.month || m} '${String(year).slice(-2)}`,
        actualRevenue: null,
        actualExpenses: null,
        actualProfit: null,
        forecastRevenue: revenue,
        forecastExpenses: expenses,
        forecastProfit: revenue - expenses + nonOperating,
      });
    }

    // Connect the dashed forecast line to the last solid actual point,
    // so there's no visual gap at the transition.
    if (historical.length && forecast.length) {
      forecast[0] = {
        ...forecast[0],
        // keep forecast[0] as-is; instead duplicate last historical
        // point's actual values into the forecast fields so recharts
        // draws a continuous line from that point.
      };
      const last = historical[historical.length - 1];
      historical[historical.length - 1] = {
        ...last,
        forecastRevenue: last.actualRevenue,
        forecastExpenses: last.actualExpenses,
        forecastProfit: last.actualProfit,
      };
    }

    return [...historical, ...forecast];
  }, [data, year]);

  const { forecastAnnualRevenue, forecastAnnualExpenses, baseAnnualRevenue } = useMemo(() => {
    if (!data || !data.has_history) {
      return { forecastAnnualRevenue: 0, forecastAnnualExpenses: 0, baseAnnualRevenue: 0 };
    }

    const forecastRevenue =
      sumByAccounts(data.forecast, REVENUE_ACCOUNTS, "forecast") -
      sumByAccounts(data.forecast, [SALES_RETURN_ACCOUNT], "forecast");
    const forecastExpenses = sumByAccounts(data.forecast, EXPENSE_ACCOUNTS, "forecast");
    const baseRevenue =
      sumByAccounts(data.historical, REVENUE_ACCOUNTS, "actual") -
      sumByAccounts(data.historical, [SALES_RETURN_ACCOUNT], "actual");

    return {
      forecastAnnualRevenue: forecastRevenue,
      forecastAnnualExpenses: forecastExpenses,
      baseAnnualRevenue: baseRevenue,
    };
  }, [data]);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Forecast</h1>
        <p className="text-slate-500 mt-2">
          Projected performance based on historical trend and seasonality.
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

        <div className="flex-1" />

        <div className="flex items-center gap-2">
          <label className="text-sm text-slate-500">Override Growth %</label>
          <input
            type="number"
            step="1"
            placeholder="auto"
            value={growthOverride}
            onChange={(e) => setGrowthOverride(e.target.value)}
            onBlur={loadForecast}
            className="w-24 border border-slate-200 rounded-lg px-3 py-2 text-sm"
          />
        </div>
      </div>

      {loading ? (
        <div className="text-xl font-semibold text-slate-500">
          Loading Forecast...
        </div>
      ) : error ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 rounded-xl p-6">
          {error}
        </div>
      ) : data && data.has_history === false ? (
        <div className="bg-amber-50 border border-amber-200 text-amber-800 rounded-xl p-6">
          <p className="font-semibold mb-1">No historical data available for {year - 1}</p>
          <p className="text-sm">
            A forecast for {year} needs at least one year of prior actuals to
            project from. Try a different year.
          </p>
        </div>
      ) : (
        <>
          <ForecastKPICards
            forecastRevenue={forecastAnnualRevenue}
            forecastExpenses={forecastAnnualExpenses}
            baseRevenue={baseAnnualRevenue}
          />

          <ForecastChart data={chartData} />

          <ForecastAssumptions
            assumptions={data?.assumptions}
            baseYear={data?.base_year}
            growthOverride={growthOverride !== "" ? Number(growthOverride) : null}
          />
        </>
      )}
    </div>
  );
}

export default Forecast;
