import { useState } from "react";
import { ChevronDown, ChevronRight, Info } from "lucide-react";

function ForecastAssumptions({ assumptions, baseYear, growthOverride }) {
  const [open, setOpen] = useState(false);

  if (!assumptions || assumptions.length === 0) return null;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6">
      <div className="flex items-start gap-3">
        <Info size={18} className="text-slate-400 mt-0.5 shrink-0" />
        <p className="text-sm text-slate-600">
          Method: each account's forecasted annual total is its {baseYear}{" "}
          actual, grown by{" "}
          {growthOverride !== null && growthOverride !== undefined
            ? `a fixed ${growthOverride}% (overriding the historical rate)`
            : "its own historical average year-over-year growth rate"}
          , then spread across months using that account's typical seasonal
          pattern (not spread evenly).
        </p>
      </div>

      <button
        onClick={() => setOpen(!open)}
        className="mt-4 flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700"
      >
        {open ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        {open ? "Hide" : "Show"} growth rate assumption by account
      </button>

      {open && (
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 text-xs uppercase tracking-wide">
                <th className="text-left font-medium py-2">Account</th>
                <th className="text-right font-medium py-2">{baseYear} Actual</th>
                <th className="text-right font-medium py-2">Growth Rate</th>
                <th className="text-right font-medium py-2">Forecast Annual</th>
              </tr>
            </thead>
            <tbody>
              {assumptions.map((a, idx) => (
                <tr key={idx} className="border-b border-slate-100 last:border-0">
                  <td className="py-2 text-slate-700">{a.account}</td>
                  <td className="py-2 text-right tabular-nums text-slate-600">
                    {a.base_annual.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                  </td>
                  <td
                    className={`py-2 text-right tabular-nums font-medium ${
                      a.growth_rate >= 0 ? "text-emerald-600" : "text-rose-600"
                    }`}
                  >
                    {a.growth_rate >= 0 ? "+" : ""}
                    {a.growth_rate}%
                  </td>
                  <td className="py-2 text-right tabular-nums text-slate-700">
                    {a.forecast_annual.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ForecastAssumptions;
