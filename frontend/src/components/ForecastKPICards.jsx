import { CircleDollarSign, Landmark, DollarSign, TrendingUp } from "lucide-react";

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

function ForecastKPICards({ forecastRevenue, forecastExpenses, baseRevenue }) {
  const forecastProfit = forecastRevenue - forecastExpenses;
  const revenueGrowth = baseRevenue ? ((forecastRevenue - baseRevenue) / baseRevenue) * 100 : 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      <Card
        icon={CircleDollarSign}
        iconBg="bg-emerald-50"
        iconColor="text-emerald-600"
        label="Forecasted Annual Revenue"
        value={formatMoney(forecastRevenue)}
      />

      <Card
        icon={Landmark}
        iconBg="bg-rose-50"
        iconColor="text-rose-600"
        label="Forecasted Annual Expenses"
        value={formatMoney(forecastExpenses)}
      />

      <Card
        icon={DollarSign}
        iconBg={forecastProfit >= 0 ? "bg-indigo-50" : "bg-rose-50"}
        iconColor={forecastProfit >= 0 ? "text-indigo-600" : "text-rose-600"}
        label="Forecasted Net Profit"
        value={formatMoney(forecastProfit)}
      />

      <Card
        icon={TrendingUp}
        iconBg={revenueGrowth >= 0 ? "bg-emerald-50" : "bg-rose-50"}
        iconColor={revenueGrowth >= 0 ? "text-emerald-600" : "text-rose-600"}
        label="Forecasted Revenue Growth"
        value={`${revenueGrowth >= 0 ? "+" : ""}${revenueGrowth.toFixed(1)}%`}
        sub="vs most recent actual year"
      />
    </div>
  );
}

export default ForecastKPICards;
