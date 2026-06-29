import { useEffect, useState } from "react";

import api from "../services/api";
import KPICard from "../components/KPICard";

function Dashboard() {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const response = await api.get("/api/dashboard/kpis");
      setKpis(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="text-xl font-semibold">
        Loading dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-8">

      <div>
        <h1 className="text-3xl font-bold text-slate-800">
          Executive Dashboard
        </h1>

        <p className="text-slate-500 mt-2">
          Live financial data from DuckDB
        </p>
      </div>

      <div className="grid grid-cols-4 gap-6">

        <KPICard
          title="Revenue"
          value={Number(kpis.revenue).toLocaleString()}
        />

        <KPICard
          title="Expenses"
          value={Number(kpis.expenses).toLocaleString()}
        />

        <KPICard
          title="Net Profit"
          value={Number(kpis.profit).toLocaleString()}
        />

        <KPICard
          title="Cash"
          value={Number(kpis.cash).toLocaleString()}
        />

      </div>

      <div className="bg-white rounded-xl shadow p-8 h-96 flex items-center justify-center">
        <h2 className="text-slate-400 text-xl">
          Charts will connect here next
        </h2>
      </div>

    </div>
  );
}

export default Dashboard;