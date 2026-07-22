import { useEffect, useState } from "react";

import api from "../services/api";

import FilterBar from "../components/FilterBar";
import RatiosView from "../components/RatiosView";

import useFilters from "../hooks/useFilters";

const EMPTY_FILTERS = {
  years: [],
  quarters: [],
  months: [],
  countries: [],
};

function FinancialRatios() {
  const [ratios, setRatios] = useState(null);
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
    loadRatios();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [year, quarter, month, country]);

  async function loadRatios() {
    setLoading(true);
    setError(null);

    try {
      const { data } = await api.get("/api/financial/ratios", {
        params: {
          year: year || undefined,
          quarter: quarter || undefined,
          month: month || undefined,
          country: country || undefined,
        },
      });

      setRatios(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load financial ratios. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">
          Financial Ratios
        </h1>
        <p className="text-slate-500 mt-2">
          Liquidity, profitability, leverage, and efficiency ratios for the
          selected reporting period.
        </p>
      </div>

      <FilterBar filters={filterOptions} />

      {loading ? (
        <div className="text-xl font-semibold text-slate-500">
          Loading Financial Ratios...
        </div>
      ) : error ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 rounded-xl p-6">
          {error}
        </div>
      ) : (
        <RatiosView ratios={ratios} />
      )}
    </div>
  );
}

export default FinancialRatios;
