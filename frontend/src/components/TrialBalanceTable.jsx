import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

function formatMoney(value) {
  const n = Number(value) || 0;

  return n.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function ReportSection({ report, rows }) {
  const [open, setOpen] = useState(true);

  const subtotalDebit = rows.reduce((sum, r) => sum + Number(r.debit || 0), 0);
  const subtotalCredit = rows.reduce((sum, r) => sum + Number(r.credit || 0), 0);

  return (
    <div className="border border-slate-200 rounded-xl overflow-hidden">

      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between bg-slate-50 hover:bg-slate-100 transition px-5 py-4 text-left"
      >
        <div className="flex items-center gap-2">
          {open ? (
            <ChevronDown size={18} className="text-slate-500" />
          ) : (
            <ChevronRight size={18} className="text-slate-500" />
          )}

          <span className="font-semibold text-slate-800">
            {report}
          </span>

          <span className="text-xs text-slate-400 font-medium">
            ({rows.length} account{rows.length === 1 ? "" : "s"})
          </span>
        </div>

        <div className="flex items-center gap-6 text-sm font-medium text-slate-600">
          <span>Debit: {formatMoney(subtotalDebit)}</span>
          <span>Credit: {formatMoney(subtotalCredit)}</span>
        </div>
      </button>

      {open && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 text-xs uppercase tracking-wide">
                <th className="text-left font-medium px-5 py-3">Class</th>
                <th className="text-left font-medium px-5 py-3">Subclass</th>
                <th className="text-left font-medium px-5 py-3">Account Key</th>
                <th className="text-left font-medium px-5 py-3">Account</th>
                <th className="text-right font-medium px-5 py-3">Debit</th>
                <th className="text-right font-medium px-5 py-3">Credit</th>
              </tr>
            </thead>

            <tbody>
              {rows.map((row, idx) => (
                <tr
                  key={`${row.account_key}-${idx}`}
                  className="border-b border-slate-100 last:border-0 hover:bg-slate-50 transition"
                >
                  <td className="px-5 py-3 text-slate-600">{row.class}</td>
                  <td className="px-5 py-3 text-slate-600">{row.subclass}</td>
                  <td className="px-5 py-3 text-slate-500 font-mono text-xs">{row.account_key}</td>
                  <td className="px-5 py-3 text-slate-800 font-medium">{row.account}</td>
                  <td className="px-5 py-3 text-right text-slate-700 tabular-nums">
                    {Number(row.debit) ? formatMoney(row.debit) : "—"}
                  </td>
                  <td className="px-5 py-3 text-right text-slate-700 tabular-nums">
                    {Number(row.credit) ? formatMoney(row.credit) : "—"}
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

function TrialBalanceTable({ rows }) {
  const grouped = [];
  const index = new Map();

  for (const row of rows) {
    if (!index.has(row.report)) {
      index.set(row.report, []);
      grouped.push({ report: row.report, rows: index.get(row.report) });
    }

    index.get(row.report).push(row);
  }

  if (grouped.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
        No accounts match the current filters.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {grouped.map((group) => (
        <ReportSection
          key={group.report}
          report={group.report}
          rows={group.rows}
        />
      ))}
    </div>
  );
}

export default TrialBalanceTable;
