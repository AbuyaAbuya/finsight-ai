import { useState } from "react";
import { Pencil, Check, X, CheckCircle2, AlertTriangle } from "lucide-react";

function formatMoney(value) {
  const n = Number(value) || 0;
  const abs = Math.abs(n).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return n < 0 ? `(${abs})` : abs;
}

function EditableBudgetCell({ value, editable, onSave }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);

  if (!editable) {
    return <span className="tabular-nums text-slate-700">{formatMoney(value)}</span>;
  }

  if (!editing) {
    return (
      <button
        onClick={() => {
          setDraft(value);
          setEditing(true);
        }}
        className="group inline-flex items-center gap-2 tabular-nums text-slate-700 hover:text-blue-600"
      >
        {formatMoney(value)}
        <Pencil
          size={13}
          className="opacity-0 group-hover:opacity-60 transition-opacity"
        />
      </button>
    );
  }

  return (
    <div className="inline-flex items-center gap-1">
      <input
        type="number"
        step="0.01"
        autoFocus
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            onSave(Number(draft));
            setEditing(false);
          } else if (e.key === "Escape") {
            setEditing(false);
          }
        }}
        className="w-28 text-right border border-blue-300 rounded px-2 py-1 text-sm outline-none focus:ring-2 focus:ring-blue-200"
      />
      <button
        onClick={() => {
          onSave(Number(draft));
          setEditing(false);
        }}
        className="text-emerald-600 hover:text-emerald-700"
      >
        <Check size={16} />
      </button>
      <button
        onClick={() => setEditing(false)}
        className="text-slate-400 hover:text-slate-600"
      >
        <X size={16} />
      </button>
    </div>
  );
}

function BudgetTable({ rows, editable, onUpdateBudget }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
        No budget data for the selected filters.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500 text-xs uppercase tracking-wide bg-slate-50">
              <th className="text-left font-medium px-5 py-3">Account</th>
              <th className="text-right font-medium px-5 py-3">Budget</th>
              <th className="text-right font-medium px-5 py-3">Actual</th>
              <th className="text-right font-medium px-5 py-3">Variance</th>
              <th className="text-right font-medium px-5 py-3">Variance %</th>
              <th className="text-center font-medium px-5 py-3">Status</th>
            </tr>
          </thead>

          <tbody>
            {rows.map((row, idx) => (
              <tr
                key={`${row.account}-${idx}`}
                className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition"
              >
                <td className="px-5 py-3 text-slate-800 font-medium">
                  {row.account}
                </td>

                <td className="px-5 py-3 text-right">
                  <EditableBudgetCell
                    value={row.budget}
                    editable={editable}
                    onSave={(newValue) => onUpdateBudget(row.account, newValue)}
                  />
                </td>

                <td className="px-5 py-3 text-right tabular-nums text-slate-700">
                  {formatMoney(row.actual)}
                </td>

                <td
                  className={`px-5 py-3 text-right tabular-nums font-medium ${
                    row.favorable ? "text-emerald-600" : "text-rose-600"
                  }`}
                >
                  {formatMoney(row.variance)}
                </td>

                <td
                  className={`px-5 py-3 text-right tabular-nums ${
                    row.favorable ? "text-emerald-600" : "text-rose-600"
                  }`}
                >
                  {row.variance_pct === null ? "—" : `${row.variance_pct > 0 ? "+" : ""}${row.variance_pct}%`}
                </td>

                <td className="px-5 py-3">
                  <div className="flex justify-center">
                    {row.favorable ? (
                      <CheckCircle2 size={18} className="text-emerald-600" />
                    ) : (
                      <AlertTriangle size={18} className="text-rose-600" />
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default BudgetTable;
