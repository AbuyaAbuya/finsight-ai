// Accounts that are credit-normal (Revenue / Income / net Gains).
// These are stored as negative balances in the corrected ledger
// (credit = increase), so they need to be sign-flipped for display.
// Everything else (Cost of Sales, Operating Expenses, Depreciation &
// Amortization, Interest Expense, Taxation, Sales Return) is debit-normal
// and already displays correctly with its stored sign.
const CREDIT_NORMAL_ACCOUNTS = new Set([
  "Sales",
  "Interest Income",
  "Dividend Income",
  "Gain/Loss on Sales of Asset",
  "Exchange Loss/Gain",
]);

function displayAmount(row) {
  const raw = Number(row.balance) || 0;
  return CREDIT_NORMAL_ACCOUNTS.has(row.account) ? -raw : raw;
}

function formatMoney(value) {
  const n = Number(value) || 0;
  const abs = Math.abs(n).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return n < 0 ? `(${abs})` : abs;
}

function LineItem({ label, amount, indent = false, muted = false }) {
  return (
    <div
      className={`flex items-center justify-between py-2 ${
        indent ? "pl-6" : ""
      }`}
    >
      <span className={muted ? "text-slate-500" : "text-slate-700"}>
        {label}
      </span>
      <span className="tabular-nums text-slate-700">{formatMoney(amount)}</span>
    </div>
  );
}

function SubtotalRow({ label, amount, tone = "default" }) {
  const toneClasses = {
    default: "border-slate-300 text-slate-800",
    gross: "border-blue-200 text-blue-700 bg-blue-50",
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

function Section({ title, children }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-1">
      <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400 mb-3">
        {title}
      </h3>
      {children}
    </div>
  );
}

function IncomeStatementView({ rows }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
        No profit and loss activity matches the current filters.
      </div>
    );
  }

  const bySubclass2 = {};
  for (const row of rows) {
    const key = row.subclass2 || "Other";
    if (!bySubclass2[key]) bySubclass2[key] = [];
    bySubclass2[key].push(row);
  }

  const salesRows = (bySubclass2["Sales"] || []).filter(
    (r) => r.account === "Sales"
  );
  const salesReturnRows = (bySubclass2["Sales"] || []).filter(
    (r) => r.account === "Sales Return"
  );
  const costOfSalesRows = bySubclass2["Cost of Sales"] || [];

  const operatingExpenseRows = [
    ...(bySubclass2["Sales & Distribution"] || []),
    ...(bySubclass2["Marketing"] || []),
    ...(bySubclass2["Administration"] || []),
  ];

  const depreciationAmortizationRows = [
    ...(bySubclass2["Depreciation"] || []),
    ...(bySubclass2["Amortization"] || []),
  ];

  const nonOperatingRows = [
    ...(bySubclass2["Interest Income"] || []),
    ...(bySubclass2["Dividend Income"] || []),
    ...(bySubclass2["Gain/Loss on Sales of Asset"] || []),
    ...(bySubclass2["Exchange Loss/Gain"] || []),
  ];

  const interestExpenseRows = bySubclass2["Interest Expense"] || [];
  const taxationRows = bySubclass2["Taxation"] || [];

  const sum = (arr) => arr.reduce((s, r) => s + displayAmount(r), 0);

  const grossSales = sum(salesRows);
  const salesReturns = sum(salesReturnRows);
  const netRevenue = grossSales - salesReturns;

  const costOfSales = sum(costOfSalesRows);
  const grossProfit = netRevenue - costOfSales;

  const operatingExpenses = sum(operatingExpenseRows);
  const depreciationAmortization = sum(depreciationAmortizationRows);
  const operatingProfit =
    grossProfit - operatingExpenses - depreciationAmortization;

  const nonOperatingIncome = sum(nonOperatingRows);
  const profitBeforeInterestTax = operatingProfit + nonOperatingIncome;

  const interestExpense = sum(interestExpenseRows);
  const profitBeforeTax = profitBeforeInterestTax - interestExpense;

  const taxation = sum(taxationRows);
  const netProfit = profitBeforeTax - taxation;

  const netMargin = netRevenue !== 0 ? (netProfit / netRevenue) * 100 : 0;
  const grossMargin = netRevenue !== 0 ? (grossProfit / netRevenue) * 100 : 0;

  return (
    <div className="space-y-6">
      <Section title="Revenue">
        {salesRows.map((r, i) => (
          <LineItem key={`sales-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        {salesReturnRows.map((r, i) => (
          <LineItem
            key={`sret-${i}`}
            label={r.account}
            amount={-displayAmount(r)}
            indent
            muted
          />
        ))}
        <SubtotalRow label="Net Revenue" amount={netRevenue} />
      </Section>

      <Section title="Cost of Sales">
        {costOfSalesRows.map((r, i) => (
          <LineItem key={`cos-${i}`} label={r.account} amount={-displayAmount(r)} />
        ))}
        <SubtotalRow label="Gross Profit" amount={grossProfit} tone="gross" />
      </Section>

      <Section title="Operating Expenses">
        {operatingExpenseRows.map((r, i) => (
          <LineItem
            key={`opex-${i}`}
            label={r.account}
            amount={-displayAmount(r)}
          />
        ))}
        {depreciationAmortizationRows.map((r, i) => (
          <LineItem
            key={`da-${i}`}
            label={r.account}
            amount={-displayAmount(r)}
          />
        ))}
        <SubtotalRow label="Operating Profit (EBIT)" amount={operatingProfit} />
      </Section>

      <Section title="Non-Operating Income / (Loss)">
        {nonOperatingRows.map((r, i) => (
          <LineItem key={`nonop-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        <SubtotalRow
          label="Profit Before Interest & Tax"
          amount={profitBeforeInterestTax}
        />
      </Section>

      <Section title="Interest & Tax">
        {interestExpenseRows.map((r, i) => (
          <LineItem key={`int-${i}`} label={r.account} amount={-displayAmount(r)} />
        ))}
        <LineItem label="Profit Before Tax" amount={profitBeforeTax} muted />
        {taxationRows.map((r, i) => (
          <LineItem key={`tax-${i}`} label={r.account} amount={-displayAmount(r)} />
        ))}
        <SubtotalRow label="Net Profit" amount={netProfit} tone="final" />
      </Section>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <div className="text-sm text-slate-500">Gross Margin</div>
          <div className="text-2xl font-bold text-slate-800 mt-1">
            {grossMargin.toFixed(1)}%
          </div>
        </div>
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <div className="text-sm text-slate-500">Net Margin</div>
          <div className="text-2xl font-bold text-slate-800 mt-1">
            {netMargin.toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  );
}

export { displayAmount };
export default IncomeStatementView;
