import { useEffect, useState } from "react";
import { Download } from "lucide-react";

import api from "../services/api";

import FilterBar from "../components/FilterBar";
import CashFlowView from "../components/CashFlowView";

import useFilters from "../hooks/useFilters";

const EMPTY_FILTERS = {
  years: [],
  quarters: [],
  months: [],
  countries: [],
};

function downloadCsv(data) {
  if (!data) return;

  const lines = [
    "Line Item,Amount",
    ...Object.entries(data).map(
      ([key, value]) => `"${key}","${Number(value).toFixed(2)}"`
    ),
  ];

  const blob = new Blob([lines.join("\n")], {
    type: "text/csv;charset=utf-8;",
  });

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.setAttribute("download", "cash-flow-statement.csv");

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}

function CashFlow() {
  const [data, setData] = useState(null);
  const [filterOptions, setFilterOptions] = useState(EMPTY_FILTERS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { year, quarter, month, country } = useFilters();

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

  useEffect(() => {
    loadCashFlow();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [year, quarter, month, country]);

  async function loadCashFlow() {
    setLoading(true);
    setError(null);

    try {
      const { data } = await api.get("/api/financial/cash-flow", {
        params: {
          year: year || undefined,
          quarter: quarter || undefined,
          month: month || undefined,
          country: country || undefined,
        },
      });

      setData(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load the cash flow statement. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">
            Cash Flow Statement
          </h1>
          <p className="text-slate-500 mt-2">
            Operating, Investing, and Financing activities (indirect
            method).
          </p>
        </div>

        <button
          onClick={() => downloadCsv(data)}
          disabled={!data}
          className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold px-5 py-3 rounded-xl shadow transition self-start"
        >
          <Download size={18} />
          Export CSV
        </button>
      </div>

      <FilterBar filters={filterOptions} />

      {loading ? (
        <div className="text-xl font-semibold text-slate-500">
          Loading Cash Flow Statement...
        </div>
      ) : error ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 rounded-xl p-6">
          {error}
        </div>
      ) : (
        <CashFlowView data={data} />
      )}
    </div>
  );
}

export default CashFlow;
