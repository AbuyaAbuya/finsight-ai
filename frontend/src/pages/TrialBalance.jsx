import { useEffect, useMemo, useState } from "react";
import {
  Search,
  Download,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

import api from "../services/api";

import FilterBar from "../components/FilterBar";
import TrialBalanceTable from "../components/TrialBalanceTable";

import useFilters from "../hooks/useFilters";

const EMPTY_FILTERS = {
  years: [],
  quarters: [],
  months: [],
  countries: [],
};

function formatMoney(value) {
  const n = Number(value) || 0;

  return n.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function downloadCsv(rows) {
  const headers = [
    "Report",
    "Class",
    "Subclass",
    "Subclass2",
    "Account Key",
    "Account",
    "Debit",
    "Credit",
  ];

  const lines = [
    headers.join(","),
    ...rows.map((r) =>
      [
        r.report,
        r.class,
        r.subclass,
        r.subclass2,
        r.account_key,
        r.account,
        Number(r.debit || 0).toFixed(2),
        Number(r.credit || 0).toFixed(2),
      ]
        .map((v) => `"${String(v ?? "").replace(/"/g, '""')}"`)
        .join(",")
    ),
  ];

  const blob = new Blob([lines.join("\n")], {
    type: "text/csv;charset=utf-8;",
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.setAttribute("download", "trial-balance.csv");

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}

function TrialBalance() {
  const [rows, setRows] = useState([]);
  const [filterOptions, setFilterOptions] = useState(EMPTY_FILTERS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  const {
    year,
    quarter,
    month,
    country,
  } = useFilters();

  // ------------------------------------------------------------
  // Load filter options once
  // ------------------------------------------------------------

  useEffect(() => {
    loadFilterOptions();
  }, []);

  async function loadFilterOptions() {
    try {
      const { data } = await api.get("/api/financial/filters");

      setFilterOptions({
        years: (data.years || []).map((r) => r.year),
        quarters: (data.quarters || []).map((r) => r.quarter),
        months: (data.months || []).map((r) => r.month),
        countries: (data.countries || []).map((r) => r.country),
      });
    } catch (err) {
      console.error(err);
    }
  }

  // ------------------------------------------------------------
  // Load trial balance whenever filters change
  // ------------------------------------------------------------

  useEffect(() => {
    loadTrialBalance();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [year, quarter, month, country]);

  async function loadTrialBalance() {
    setLoading(true);
    setError(null);

    try {
      const { data } = await api.get("/api/financial/trial-balance", {
        params: {
          year: year || undefined,
          quarter: quarter || undefined,
          month: month || undefined,
          country: country || undefined,
        },
      });

      setRows(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load the trial balance. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  // ------------------------------------------------------------
  // Client-side search
  // ------------------------------------------------------------

  const filteredRows = useMemo(() => {
    if (!search.trim()) return rows;

    const q = search.trim().toLowerCase();

    return rows.filter((r) =>
      [r.account, r.class, r.subclass, r.subclass2, r.account_key]
        .filter(Boolean)
        .some((field) => String(field).toLowerCase().includes(q))
    );
  }, [rows, search]);

  // ------------------------------------------------------------
  // Totals & balance check
  // ------------------------------------------------------------

  const totals = useMemo(() => {
    const totalDebit = filteredRows.reduce(
      (sum, r) => sum + Number(r.debit || 0),
      0
    );

    const totalCredit = filteredRows.reduce(
      (sum, r) => sum + Number(r.credit || 0),
      0
    );

    const isBalanced = Math.abs(totalDebit - totalCredit) < 0.01;

    return { totalDebit, totalCredit, isBalanced };
  }, [filteredRows]);

  return (
    <div className="space-y-8">

      {/* Header */}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

        <div>
          <h1 className="text-3xl font-bold text-slate-800">
            Trial Balance
          </h1>

          <p className="text-slate-500 mt-2">
            Full General Ledger summary of debit and credit balances by account.
          </p>
        </div>

        <button
          onClick={() => downloadCsv(filteredRows)}
          disabled={filteredRows.length === 0}
          className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold px-5 py-3 rounded-xl shadow transition self-start"
        >
          <Download size={18} />
          Export CSV
        </button>

      </div>

      {/* Filters */}

      <FilterBar filters={filterOptions} />

      {/* Search + Balance Summary */}

      <div className="bg-white rounded-xl shadow p-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">

        <div className="flex items-center gap-3 bg-slate-100 rounded-xl px-5 py-3 w-full max-w-md">
          <Search size={18} className="text-slate-500" />

          <input
            type="text"
            placeholder="Search by account, class or subclass..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-transparent outline-none w-full text-sm text-slate-700"
          />
        </div>

        <div className="flex items-center gap-6 text-sm">

          <div className="text-slate-600">
            <span className="font-medium">Total Debit:</span>{" "}
            {formatMoney(totals.totalDebit)}
          </div>

          <div className="text-slate-600">
            <span className="font-medium">Total Credit:</span>{" "}
            {formatMoney(totals.totalCredit)}
          </div>

          <div
            className={`flex items-center gap-2 font-semibold ${totals.isBalanced ? "text-emerald-600" : "text-rose-600"
              }`}
          >
            {totals.isBalanced ? (
              <>
                <CheckCircle2 size={18} />
                Balanced
              </>
            ) : (
              <>
                <AlertTriangle size={18} />
                Out of Balance
              </>
            )}
          </div>

        </div>

      </div>

      {/* Table */}

      {loading ? (
        <div className="text-xl font-semibold text-slate-500">
          Loading Trial Balance...
        </div>
      ) : error ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 rounded-xl p-6">
          {error}
        </div>
      ) : (
        <TrialBalanceTable rows={filteredRows} />
      )}

    </div>
  );
}

export default TrialBalance;
