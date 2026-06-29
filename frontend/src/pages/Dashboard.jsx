import { useEffect, useState } from "react";

import api from "../services/api";

import KPICard from "../components/KPICard";
import FilterBar from "../components/FilterBar";
import RevenueTrendChart from "../components/RevenueTrendChart";
import ExpenseTrendChart from "../components/ExpenseTrendChart";
import ExecutiveInsights from "../components/ExecutiveInsights";
import FinancialDrivers from "../components/FinancialDrivers";

import useFilters from "../hooks/useFilters";

function Dashboard() {

    const [dashboard, setDashboard] = useState(null);
    const [loading, setLoading] = useState(true);

    const {
        year,
        quarter,
        month,
        country,
    } = useFilters();

    useEffect(() => {
        loadDashboard();
    }, [year, quarter, month, country]);

    async function loadDashboard() {

        setLoading(true);

        try {

            const { data } = await api.get(
                "/api/dashboard",
                {
                    params: {
                        year: year || undefined,
                        quarter: quarter || undefined,
                        month: month || undefined,
                        country: country || undefined,
                    },
                }
            );

            setDashboard(data);

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }

    }

    if (loading || !dashboard) {

        return (
            <div className="text-xl font-semibold">
                Loading Dashboard...
            </div>
        );

    }

    const {

        kpis,

        filters,

        revenueTrend,

        expenseTrend,

        insights,

        revenueDrivers,

        expenseDrivers,

        cashBreakdown,

    } = dashboard;

    return (

        <div className="space-y-8">

            {/* Header */}

            <div>

                <h1 className="text-3xl font-bold text-slate-800">
                    Executive Dashboard
                </h1>

                <p className="text-slate-500 mt-2">
                    Enterprise Financial Planning & Analysis Platform
                </p>

            </div>

            {/* Filters */}

            <FilterBar filters={filters} />

            {/* KPI Cards */}

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-7">

                <KPICard
                    title="Revenue"
                    kpi={kpis.revenue}
                />

                <KPICard
                    title="Expenses"
                    kpi={kpis.expenses}
                />

                <KPICard
                    title="Net Profit"
                    kpi={kpis.profit}
                />

                <KPICard
                    title="Cash"
                    kpi={kpis.cash}
                />

            </div>

            {/* Charts */}

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-7">

                <RevenueTrendChart
                    data={revenueTrend}
                />

                <ExpenseTrendChart
                    data={expenseTrend}
                />

            </div>

            {/* Executive Insights */}

            <ExecutiveInsights
                insights={insights}
            />

            {/* Financial Intelligence */}

            <FinancialDrivers
                revenueDrivers={revenueDrivers}
                expenseDrivers={expenseDrivers}
                cashBreakdown={cashBreakdown}
            />

        </div>

    );

}

export default Dashboard;