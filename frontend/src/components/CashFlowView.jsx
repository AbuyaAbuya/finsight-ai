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

function CashFlowView({ data }) {
  if (!data) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
        No cash flow activity matches the current filters.
      </div>
    );
  }

  const {
    profit_before_tax: profitBeforeTax,
    depreciation_amortization: depreciationAmortization,
    non_operating_removed: nonOperatingRemoved,
    interest_expense_addback: interestExpenseAddback,
    receivables_change: receivablesChange,
    inventory_change: inventoryChange,
    payables_change: payablesChange,
    interest_paid: interestPaid,
    tax_paid: taxPaid,
    purchase_equipment: purchaseEquipment,
    proceeds_from_sale_of_asset: proceedsFromSaleOfAsset,
    investments_purchase: investmentsPurchase,
    interest_received: interestReceived,
    dividends_received: dividendsReceived,
    exchange_gain_loss_cash: exchangeGainLossCash,
    share_capital_issued: shareCapitalIssued,
    new_loan_proceeds: newLoanProceeds,
    dividends_paid_cash: dividendsPaidCash,
    net_operating: netOperating,
    net_investing: netInvesting,
    net_financing: netFinancing,
    net_change: netChange,
    opening_cash: openingCash,
    closing_cash: closingCash,
  } = data;

  const operatingBeforeInterestTax =
    profitBeforeTax +
    depreciationAmortization +
    nonOperatingRemoved +
    interestExpenseAddback +
    receivablesChange +
    inventoryChange +
    payablesChange;

  const impliedClosing = openingCash + netChange;
  const isReconciled = Math.abs(impliedClosing - closingCash) < 0.01;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200 p-5 flex items-center justify-between">
        <div>
          <div className="text-sm text-slate-500">Reconciliation Check</div>
          <div className="text-slate-700 mt-1">
            Opening ({formatMoney(openingCash)}) + Net Change (
            {formatMoney(netChange)}) vs Closing ({formatMoney(closingCash)})
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

      <Section title="Cash Flows from Operating Activities">
        <LineItem label="Profit Before Tax" amount={profitBeforeTax} />
        <LineItem
          label="Add: Depreciation & Amortization"
          amount={depreciationAmortization}
          indent
        />
        <LineItem
          label="Remove: Non-Operating Income/(Loss)"
          amount={nonOperatingRemoved}
          indent
        />
        <LineItem
          label="Add: Interest Expense"
          amount={interestExpenseAddback}
          indent
        />
        <LineItem
          label="(Increase)/Decrease in Receivables"
          amount={receivablesChange}
          indent
        />
        <LineItem
          label="(Increase)/Decrease in Inventory"
          amount={inventoryChange}
          indent
        />
        <LineItem
          label="Increase/(Decrease) in Payables"
          amount={payablesChange}
          indent
        />
        <SubtotalRow
          label="Cash from Operations before Interest & Tax"
          amount={operatingBeforeInterestTax}
        />
        <LineItem label="Interest Paid" amount={interestPaid} />
        <LineItem label="Tax Paid" amount={taxPaid} />
        <SubtotalRow
          label="Net Cash from Operating Activities"
          amount={netOperating}
          tone="section"
        />
      </Section>

      <Section title="Cash Flows from Investing Activities">
        <LineItem label="Purchase of Equipment" amount={purchaseEquipment} />
        <LineItem
          label="Proceeds from Sale of Asset"
          amount={proceedsFromSaleOfAsset}
        />
        <LineItem label="Purchase of Investments" amount={investmentsPurchase} />
        <LineItem label="Interest Received" amount={interestReceived} />
        <LineItem label="Dividends Received" amount={dividendsReceived} />
        <LineItem
          label="Exchange Gain/(Loss) - Cash Effect"
          amount={exchangeGainLossCash}
        />
        <SubtotalRow
          label="Net Cash from Investing Activities"
          amount={netInvesting}
          tone="section"
        />
      </Section>

      <Section title="Cash Flows from Financing Activities">
        <LineItem label="Proceeds from Share Issue" amount={shareCapitalIssued} />
        <LineItem label="Proceeds from New Loan" amount={newLoanProceeds} />
        <LineItem label="Dividends Paid" amount={dividendsPaidCash} />
        <SubtotalRow
          label="Net Cash from Financing Activities"
          amount={netFinancing}
          tone="section"
        />
      </Section>

      <Section title="Net Change in Cash">
        <LineItem label="Opening Cash Balance" amount={openingCash} />
        <LineItem label="Net Change in Cash" amount={netChange} />
        <SubtotalRow label="Closing Cash Balance" amount={closingCash} tone="final" />
      </Section>
    </div>
  );
}

export default CashFlowView;
