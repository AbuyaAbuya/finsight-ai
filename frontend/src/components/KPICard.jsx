import {
  TrendingUp,
  TrendingDown,
  Minus,
  DollarSign,
  Wallet,
  Landmark,
  CircleDollarSign,
} from "lucide-react";

function KPICard({ title, kpi }) {
  const config = {
    Revenue: {
      icon: CircleDollarSign,
      color: "text-emerald-600",
      bg: "bg-emerald-50",
    },

    Expenses: {
      icon: Landmark,
      color: "text-rose-600",
      bg: "bg-rose-50",
    },

    "Net Profit": {
      icon: DollarSign,
      color: "text-indigo-600",
      bg: "bg-indigo-50",
    },

    Cash: {
      icon: Wallet,
      color: "text-sky-600",
      bg: "bg-sky-50",
    },
  };

  const item = config[title];
  const Icon = item.icon;
  const hasComparison = kpi.direction === "up" || kpi.direction === "down";
  const trend = kpi.recentTrend;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition-all duration-300 p-6">

      <div className="flex items-start justify-between">

        <div>

          <p className="text-sm text-slate-500 font-medium">
            {title}
          </p>

          <h2 className="text-4xl font-bold text-slate-900 mt-3">
            {Number(kpi.value).toLocaleString()}
          </h2>

        </div>

        <div className={`${item.bg} h-14 w-14 rounded-xl flex items-center justify-center`}>
          <Icon className={item.color} size={28} />
        </div>

      </div>

      <div className="mt-6 flex items-center justify-between">

        {hasComparison ? (
          <div
            className={`flex items-center gap-2 text-sm font-semibold ${
              kpi.direction === "up"
                ? "text-emerald-600"
                : "text-rose-600"
            }`}
          >
            {kpi.direction === "up" ? (
              <TrendingUp size={18} />
            ) : (
              <TrendingDown size={18} />
            )}

            {kpi.change}%
          </div>
        ) : trend ? (
          <div
            className={`flex items-center gap-2 text-sm font-semibold ${
              trend.direction === "up"
                ? "text-emerald-600"
                : trend.direction === "down"
                ? "text-rose-600"
                : "text-slate-400"
            }`}
          >
            {trend.direction === "up" ? (
              <TrendingUp size={18} />
            ) : trend.direction === "down" ? (
              <TrendingDown size={18} />
            ) : (
              <Minus size={18} />
            )}

            {trend.change_pct}%
          </div>
        ) : (
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-400">
            <Minus size={18} />
            No comparison
          </div>
        )}

        <span className="text-xs text-slate-400">
          {trend ? `${trend.prior_year} vs ${trend.latest_year}` : kpi.comparison}
        </span>

      </div>

      <div className="mt-3">

        <p className="text-sm text-slate-500">
          {!hasComparison && trend ? trend.insight : kpi.message}
        </p>

      </div>

    </div>
  );
}

export default KPICard;