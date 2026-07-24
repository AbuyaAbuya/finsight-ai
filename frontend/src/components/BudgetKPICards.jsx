import { Wallet, Receipt, PiggyBank, Gauge } from "lucide-react";

function formatMoney(value) {
  const n = Number(value) || 0;
  return n.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

function Card({ icon: Icon, iconBg, iconColor, label, value, sub, subColor }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500 font-medium">{label}</p>
        <div className={`${iconBg} h-11 w-11 rounded-xl flex items-center justify-center`}>
          <Icon className={iconColor} size={22} />
        </div>
      </div>
      <h2 className="text-3xl font-bold text-slate-900 mt-3">{value}</h2>
      {sub && <p className={`text-sm mt-2 font-medium ${subColor || "text-slate-500"}`}>{sub}</p>}
    </div>
  );
}

function BudgetKPICards({ totalBudget, totalActual }) {
  const remaining = totalBudget - totalActual;
  const utilization = totalBudget ? (totalActual / totalBudget) * 100 : 0;
  const overBudget = totalActual > totalBudget;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <Card
        icon={Wallet}
        iconBg="bg-slate-100"
        iconColor="text-slate-600"
        label="Total Budget"
        value={formatMoney(totalBudget)}
      />

      <Card
        icon={Receipt}
        iconBg="bg-rose-50"
        iconColor="text-rose-600"
        label="Actual Spend"
        value={formatMoney(totalActual)}
      />

      <Card
        icon={PiggyBank}
        iconBg={remaining >= 0 ? "bg-emerald-50" : "bg-rose-50"}
        iconColor={remaining >= 0 ? "text-emerald-600" : "text-rose-600"}
        label="Remaining Budget"
        value={formatMoney(remaining)}
        sub={remaining >= 0 ? "Under budget" : "Over budget"}
        subColor={remaining >= 0 ? "text-emerald-600" : "text-rose-600"}
      />

      <Card
        icon={Gauge}
        iconBg={overBudget ? "bg-rose-50" : "bg-emerald-50"}
        iconColor={overBudget ? "text-rose-600" : "text-emerald-600"}
        label="Budget Utilization"
        value={`${utilization.toFixed(1)}%`}
        sub={overBudget ? "Over Budget" : "Within Budget"}
        subColor={overBudget ? "text-rose-600" : "text-emerald-600"}
      />
    </div>
  );
}

export default BudgetKPICards;
