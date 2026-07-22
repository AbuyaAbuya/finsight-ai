function formatMoney(value) {
  const n = Number(value) || 0;
  const abs = Math.abs(n).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return n < 0 ? `(${abs})` : abs;
}

function LineItem({ label, amount, indent = false }) {
  return (
    <div className={`flex items-center justify-between py-2 ${indent ? "pl-6" : ""}`}>
      <span className="text-slate-700">{label}</span>
      <span className="tabular-nums text-slate-700">{formatMoney(amount)}</span>
    </div>
  );
}

function SubtotalRow({ label, amount, tone = "default" }) {
  const toneClasses = {
    default: "border-slate-300 text-slate-800",
    final: "border-slate-800 text-slate-900 bg-slate-50",
  };

  return (
    <div
      className={`flex items-center justify-between py-3 px-4 -mx-4 rounded-lg border-t-2 font-semibold ${toneClasses[tone]}`}
    >
      <span>{label}</span>
      <span className="tabular-nums">{formatMoney(amount)}</span>
    </div>
  );
}

function StatementOfEquityView({ data }) {
  if (!data) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
        No equity activity matches the current filters.
      </div>
    );
  }

  const {
    opening_balance: openingBalance,
    net_income: netIncome,
    dividends_for_period: dividendsForPeriod,
    share_issued: shareIssued,
    closing_balance: closingBalance,
    implied_closing: impliedClosing,
  } = data;

  const isReconciled = Math.abs(impliedClosing - closingBalance) < 0.01;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200 p-5 flex items-center justify-between">
        <div>
          <div className="text-sm text-slate-500">Reconciliation Check</div>
          <div className="text-slate-700 mt-1">
            Opening ({formatMoney(openingBalance)}) + Net Income − Dividends +
            Share Issued vs Closing ({formatMoney(closingBalance)})
          </div>
        </div>
        <div
          className={`font-semibold ${
            isReconciled ? "text-emerald-600" : "text-rose-600"
          }`}
        >
          {isReconciled ? "Reconciled ✓" : "Not Reconciled ⚠"}
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-1">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400 mb-3">
          Statement of Changes in Equity
        </h3>

        <LineItem label="Balance at the Beginning of the Period" amount={openingBalance} />
        <LineItem label="Total Income for the Period" amount={netIncome} indent />
        <LineItem
          label="Dividends Paid in the Period"
          amount={-dividendsForPeriod}
          indent
        />
        <LineItem label="Issue of Share Capital" amount={shareIssued} indent />
        <SubtotalRow
          label="Balance at the End of the Period"
          amount={closingBalance}
          tone="final"
        />
      </div>
    </div>
  );
}

export default StatementOfEquityView;
