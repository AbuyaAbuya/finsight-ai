import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
} from "recharts";

function formatNumber(value) {
    return Number(value).toLocaleString();
}

function BudgetChart({ rows, title = "Budget vs Actual", subtitle = "Planned vs actual spend and revenue by account" }) {
    if (!rows || rows.length === 0) return null;

    const data = rows.map((r) => ({
        account: r.account,
        Budget: r.budget,
        Actual: r.actual,
    }));

    return (
        <div className="bg-white rounded-xl shadow p-6">
            <div className="mb-6">
                <h2 className="text-xl font-semibold text-slate-800">
                    {title}
                </h2>
                <p className="text-sm text-slate-500">
                    {subtitle}
                </p>
            </div>

            <ResponsiveContainer width="100%" height={Math.max(320, data.length * 36)}>
                <BarChart
                    data={data}
                    layout="vertical"
                    margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />

                    <XAxis
                        type="number"
                        tickFormatter={formatNumber}
                        tick={{ fill: "#64748b", fontSize: 12 }}
                    />

                    <YAxis
                        type="category"
                        dataKey="account"
                        width={150}
                        tick={{ fill: "#334155", fontSize: 12 }}
                    />

                    <Tooltip formatter={formatNumber} />

                    <Legend
                        wrapperStyle={{ paddingTop: 12 }}
                        formatter={(value) => (
                            <span className="text-slate-600 text-sm">{value}</span>
                        )}
                    />

                    <Bar dataKey="Budget" fill="#94a3b8" radius={[0, 4, 4, 0]} barSize={10} />
                    <Bar dataKey="Actual" fill="#4f46e5" radius={[0, 4, 4, 0]} barSize={10} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}

export default BudgetChart;
