// Dividends paid is a contra-equity account (debit-normal) even though it
// shares "Retained Earnings" as its subclass2 grouping with the credit-normal
// Retained Earnings account itself — so it needs an explicit exception
// rather than a blanket flip-by-subclass rule.
const CONTRA_EQUITY_ACCOUNTS = new Set(["Dividends paid"]);

function displayAmount(row) {
  const raw = Number(row.balance) || 0;

  if (row.subclass === "Assets") return raw;

  // Liabilities and Owners Equity are credit-normal, stored negative.
  if (CONTRA_EQUITY_ACCOUNTS.has(row.account)) return raw;

  return -raw;
}

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
    section: "border-blue-200 text-blue-700 bg-blue-50",
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

function groupBy(rows, key) {
  const out = {};
  for (const row of rows) {
    const k = row[key] || "Other";
    if (!out[k]) out[k] = [];
    out[k].push(row);
  }
  return out;
}

function BalanceSheetView({ rows }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
        No balance sheet activity matches the current filters.
      </div>
    );
  }

  const bySubclass = groupBy(rows, "subclass");

  const assetRows = bySubclass["Assets"] || [];
  const liabilityRows = bySubclass["Liabilities"] || [];
  const equityRows = bySubclass["Owners Equity"] || [];

  const byAssetType = groupBy(assetRows, "subclass2");
  const currentAssets = byAssetType["Current Assets"] || [];
  const nonCurrentAssets = byAssetType["Non-Current Assets"] || [];

  const byLiabilityType = groupBy(liabilityRows, "subclass2");
  const currentLiabilities = byLiabilityType["Current Liabilities"] || [];
  const longTermLiabilities = byLiabilityType["Long Term Liabilities"] || [];

  const byEquityType = groupBy(equityRows, "subclass2");
  const shareCapital = byEquityType["Share Capital"] || [];
  const sharePremium = byEquityType["Share Premium"] || [];
  const retainedEarningsRows = (byEquityType["Retained Earnings"] || []).filter(
    (r) => !CONTRA_EQUITY_ACCOUNTS.has(r.account)
  );
  const dividendsRows = (byEquityType["Retained Earnings"] || []).filter((r) =>
    CONTRA_EQUITY_ACCOUNTS.has(r.account)
  );

  const sum = (arr) => arr.reduce((s, r) => s + displayAmount(r), 0);

  const totalCurrentAssets = sum(currentAssets);
  const totalNonCurrentAssets = sum(nonCurrentAssets);
  const totalAssets = totalCurrentAssets + totalNonCurrentAssets;

  const totalCurrentLiabilities = sum(currentLiabilities);
  const totalLongTermLiabilities = sum(longTermLiabilities);
  const totalLiabilities = totalCurrentLiabilities + totalLongTermLiabilities;

  const totalShareCapital = sum(shareCapital) + sum(sharePremium);
  const totalRetainedEarnings = sum(retainedEarningsRows);
  const totalDividends = dividendsRows.reduce(
    (s, r) => s + displayAmount(r),
    0
  );
  const totalEquity = totalShareCapital + totalRetainedEarnings - totalDividends;

  const totalLiabilitiesAndEquity = totalLiabilities + totalEquity;
  const isBalanced = Math.abs(totalAssets - totalLiabilitiesAndEquity) < 0.01;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200 p-5 flex items-center justify-between">
        <div>
          <div className="text-sm text-slate-500">Accounting Equation Check</div>
          <div className="text-slate-700 mt-1">
            Assets ({formatMoney(totalAssets)}) vs Liabilities + Equity (
            {formatMoney(totalLiabilitiesAndEquity)})
          </div>
        </div>
        <div
          className={`font-semibold ${
            isBalanced ? "text-emerald-600" : "text-rose-600"
          }`}
        >
          {isBalanced ? "Balanced ✓" : "Out of Balance ⚠"}
        </div>
      </div>

      <Section title="Current Assets">
        {currentAssets.map((r, i) => (
          <LineItem key={`ca-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        <SubtotalRow label="Total Current Assets" amount={totalCurrentAssets} />
      </Section>

      <Section title="Non-Current Assets">
        {nonCurrentAssets.map((r, i) => (
          <LineItem key={`nca-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        <SubtotalRow
          label="Total Non-Current Assets"
          amount={totalNonCurrentAssets}
        />
        <SubtotalRow label="Total Assets" amount={totalAssets} tone="section" />
      </Section>

      <Section title="Current Liabilities">
        {currentLiabilities.map((r, i) => (
          <LineItem key={`cl-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        <SubtotalRow
          label="Total Current Liabilities"
          amount={totalCurrentLiabilities}
        />
      </Section>

      <Section title="Long Term Liabilities">
        {longTermLiabilities.map((r, i) => (
          <LineItem key={`ltl-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        <SubtotalRow
          label="Total Long Term Liabilities"
          amount={totalLongTermLiabilities}
        />
        <SubtotalRow label="Total Liabilities" amount={totalLiabilities} />
      </Section>

      <Section title="Owners Equity">
        {shareCapital.map((r, i) => (
          <LineItem key={`sc-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        {sharePremium.map((r, i) => (
          <LineItem key={`sp-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        {retainedEarningsRows.map((r, i) => (
          <LineItem key={`re-${i}`} label={r.account} amount={displayAmount(r)} />
        ))}
        {dividendsRows.map((r, i) => (
          <LineItem
            key={`div-${i}`}
            label={r.account}
            amount={-displayAmount(r)}
            indent
          />
        ))}
        <SubtotalRow label="Total Owners Equity" amount={totalEquity} />
        <SubtotalRow
          label="Total Liabilities & Equity"
          amount={totalLiabilitiesAndEquity}
          tone="final"
        />
      </Section>
    </div>
  );
}

export { displayAmount };
export default BalanceSheetView;
