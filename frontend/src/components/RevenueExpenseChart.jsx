import {
    ResponsiveContainer,
    ComposedChart,
    Bar,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
} from "recharts";

function formatNumber(value) {
    return Number(value).toLocaleString();
}

function RevenueExpenseChart({ data }) {
    return (
        <div className="bg-white rounded-xl shadow p-6">

            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-xl font-semibold text-slate-800">
                        Revenue vs Expenses
                    </h2>

                    <p className="text-sm text-slate-500">
                        Monthly Revenue, Operating Expenses, and Net Profit
                    </p>
                </div>
            </div>

            <ResponsiveContainer width="100%" height={380}>
                <ComposedChart
                    data={data}
                    margin={{
                        top: 10,
                        right: 20,
                        left: 20,
                        bottom: 10,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />

                    <XAxis dataKey="month" tick={{ fill: "#64748b", fontSize: 12 }} />

                    <YAxis
                        tickFormatter={formatNumber}
                        tick={{ fill: "#64748b", fontSize: 12 }}
                    />

                    <Tooltip formatter={formatNumber} />

                    <Legend
                        wrapperStyle={{ paddingTop: 16 }}
                        formatter={(value) => (
                            <span className="text-slate-600 text-sm">{value}</span>
                        )}
                    />

                    <Bar
                        dataKey="revenue"
                        name="Revenue"
                        fill="#10b981"
                        radius={[4, 4, 0, 0]}
                        barSize={18}
                    />

                    <Bar
                        dataKey="expenses"
                        name="Expenses"
                        fill="#f87171"
                        radius={[4, 4, 0, 0]}
                        barSize={18}
                    />

                    <Line
                        type="monotone"
                        dataKey="profit"
                        name="Net Profit"
                        stroke="#4f46e5"
                        strokeWidth={3}
                        dot={{ r: 4 }}
                        activeDot={{ r: 7 }}
                    />
                </ComposedChart>
            </ResponsiveContainer>

        </div>
    );
}

export default RevenueExpenseChart;
