function BudgetProgress({ totalBudget, totalActual }) {
  const pct = totalBudget ? Math.min((totalActual / totalBudget) * 100, 100) : 0;
  const overBudget = totalActual > totalBudget;

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-600">
          Budget Utilization
        </h3>
        <span
          className={`text-sm font-bold ${
            overBudget ? "text-rose-600" : "text-emerald-600"
          }`}
        >
          {totalBudget ? ((totalActual / totalBudget) * 100).toFixed(0) : 0}%
        </span>
      </div>

      <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${
            overBudget ? "bg-rose-500" : "bg-emerald-500"
          }`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export default BudgetProgress;
