import { useEffect, useMemo, useState } from "react";
import { RefreshCw, Download } from "lucide-react";

import api from "../services/api";

import BudgetKPICards from "../components/BudgetKPICards";
import BudgetProgress from "../components/BudgetProgress";
import BudgetTable from "../components/BudgetTable";
import BudgetChart from "../components/BudgetChart";

// Accounts treated as "spend" for the KPI cards and utilization
// progress bar -- excludes revenue and non-operating income, since
// "budget utilization" is a spend-control concept, not a revenue one.
const EXPENSE_ACCOUNTS = [
  "Cost of Sales",
  "Staff Costs",
  "Commissions",
  "Advertisements",
  "Travel",
  "Entertainment",
  "Office Supplies",
  "Professional Services",
  "Telephone",
  "Utilities",
  "Other Expenses",
  "Equipment",
  "Amortization of Intangible Assets",
  "Interest Expense",
  "Taxation",
];

const CREDIT_NORMAL_ACCOUNTS = [
  "Sales",
  "Interest Income",
  "Dividend Income",
  "Gain/Loss on Sales of Asset",
  "Exchange Loss/Gain",
];

function downloadCsv(rows) {
  const headers = ["Account", "Budget", "Actual", "Variance", "Variance %", "Status"];

  const lines = [
    headers.join(","),
    ...rows.map((r) =>
      [
        r.account,
        r.budget.toFixed(2),
        r.actual.toFixed(2),
        r.variance.toFixed(2),
        r.variance_pct === null ? "" : r.variance_pct,
        r.favorable ? "Within Budget" : "Over Budget",
      ]
        .map((v) => `"${String(v ?? "").replace(/"/g, '""')}"`)
        .join(",")
    ),
  ];

  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.setAttribute("download", "budget-vs-actual.csv");

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}

function Budget() {
  const [years, setYears] = useState([]);
  const [countries, setCountries] = useState([]);

  const [year, setYear] = useState(null);
  const [country, setCountry] = useState("");
  const [month, setMonth] = useState("");

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [growthRate, setGrowthRate] = useState(0);
  const [regenerating, setRegenerating] = useState(false);

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
    if (year) loadBudget();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [year, country]);

  async function loadBudget() {
    setLoading(true);
    setError(null);

    try {
      const { data } = await api.get("/api/budget", {
        params: {
          year,
          country: country || undefined,
        },
      });

      setRows(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load the budget. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleRegenerate() {
    setRegenerating(true);

    try {
      await api.post("/api/budget/generate", {
        year,
        country: country || null,
        growth_rate: Number(growthRate) / 100,
      });

      await loadBudget();
    } catch (err) {
      console.error(err);
      setError("Failed to regenerate the baseline budget.");
    } finally {
      setRegenerating(false);
    }
  }

  async function handleUpdateBudget(account, newBudgetAmount) {
    if (!month) return;

    try {
      await api.put("/api/budget", {
        year,
        month,
        country: country || null,
        account,
        budget_amount: newBudgetAmount,
      });

      await loadBudget();
    } catch (err) {
      console.error(err);
      setError("Failed to save the budget line.");
    }
  }

  // Group rows by account: either the single selected month, or
  // summed across the whole year for an annual view.
  const displayRows = useMemo(() => {
    if (!rows.length) return [];

    if (month) {
      return rows.filter((r) => r.month === month);
    }

    const byAccount = {};

    for (const r of rows) {
      if (!byAccount[r.account]) {
        byAccount[r.account] = {
          account: r.account,
          budget: 0,
          actual: 0,
        };
      }

      byAccount[r.account].budget += r.budget;
      byAccount[r.account].actual += r.actual;
    }

    return Object.values(byAccount).map((r) => {
      const variance = r.actual - r.budget;
      const creditNormal = CREDIT_NORMAL_ACCOUNTS.includes(r.account);

      const favorable = creditNormal ? variance >= 0 : variance <= 0;
      const variance_pct = r.budget ? (variance / Math.abs(r.budget)) * 100 : null;

      return {
        ...r,
        variance,
        variance_pct: variance_pct !== null ? Math.round(variance_pct * 10) / 10 : null,
        favorable,
      };
    });
  }, [rows, month]);

  const monthOptions = useMemo(() => {
    const seen = new Map();
    for (const r of rows) {
      if (!seen.has(r.month_number)) seen.set(r.month_number, r.month);
    }
    return [...seen.entries()].sort((a, b) => a[0] - b[0]).map(([, m]) => m);
  }, [rows]);

  // KPI totals: expense accounts only (spend control, not revenue).
  const { totalBudget, totalActual } = useMemo(() => {
    const spendRows = displayRows.filter((r) => EXPENSE_ACCOUNTS.includes(r.account));
    return {
      totalBudget: spendRows.reduce((s, r) => s + r.budget, 0),
      totalActual: spendRows.reduce((s, r) => s + r.actual, 0),
    };
  }, [displayRows]);

  // Top 10 by absolute variance -- the biggest deviations from plan,
  // not just the biggest expense lines (that's already covered by the
  // Dashboard's Expense Drivers panel).
  const top10Variance = useMemo(() => {
    return [...displayRows]
      .sort((a, b) => Math.abs(b.variance) - Math.abs(a.variance))
      .slice(0, 10);
  }, [displayRows]);

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Budget</h1>
          <p className="text-slate-500 mt-2">
            Are we spending according to plan?
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => downloadCsv(displayRows)}
            disabled={displayRows.length === 0}
            className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:bg-slate-50 disabled:opacity-40 text-slate-700 font-semibold px-4 py-2 rounded-lg transition text-sm"
          >
            <Download size={16} />
            Export
          </button>

          <button
            onClick={handleRegenerate}
            disabled={regenerating}
            className="inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-900 disabled:opacity-50 text-white font-semibold px-4 py-2 rounded-lg transition text-sm"
          >
            <RefreshCw size={16} className={regenerating ? "animate-spin" : ""} />
            Regenerate Budget
          </button>
        </div>
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

        <select
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          className="border border-slate-200 rounded-lg px-4 py-2 text-sm"
        >
          <option value="">All Months (annual total)</option>
          {monthOptions.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>

        <div className="flex-1" />

        <div className="flex items-center gap-2">
          <label className="text-sm text-slate-500">Growth %</label>
          <input
            type="number"
            step="1"
            value={growthRate}
            onChange={(e) => setGrowthRate(e.target.value)}
            className="w-20 border border-slate-200 rounded-lg px-3 py-2 text-sm"
          />
        </div>
      </div>

      {!month && (
        <div className="bg-blue-50 border border-blue-200 text-blue-700 rounded-xl p-4 text-sm">
          Showing annual totals across all months. Select a specific month
          above to edit individual budget lines.
        </div>
      )}

      {loading ? (
        <div className="text-xl font-semibold text-slate-500">
          Loading Budget...
        </div>
      ) : error ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 rounded-xl p-6">
          {error}
        </div>
      ) : (
        <>
          <BudgetKPICards totalBudget={totalBudget} totalActual={totalActual} />

          <BudgetTable
            rows={displayRows}
            editable={!!month}
            onUpdateBudget={handleUpdateBudget}
          />

          <BudgetChart
            rows={top10Variance}
            title="Top 10 Variances"
            subtitle="Largest deviations between budget and actual, by absolute size"
          />

          <BudgetProgress totalBudget={totalBudget} totalActual={totalActual} />
        </>
      )}
    </div>
  );
}

export default Budget;
