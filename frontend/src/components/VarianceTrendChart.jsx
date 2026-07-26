import {
    ResponsiveContainer,
    ComposedChart,
    Bar,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ReferenceLine,
    Cell,
} from "recharts";

function VarianceTrendChart({ data }) {
    if (!data || data.length === 0) return null;

    return (
        <div className="bg-white rounded-xl shadow p-6">
            <div className="mb-6">
                <h2 className="text-xl font-semibold text-slate-800">
                    Variance Trend
                </h2>
                <p className="text-sm text-slate-500">
                    Overall favorable/(unfavorable) variance as a % of budget, by month
                </p>
            </div>

            <ResponsiveContainer width="100%" height={320}>
                <ComposedChart data={data} margin={{ top: 10, right: 20, left: 20, bottom: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />

                    <XAxis dataKey="month" tick={{ fill: "#64748b", fontSize: 12 }} />

                    <YAxis
                        tickFormatter={(v) => `${v}%`}
                        tick={{ fill: "#64748b", fontSize: 12 }}
                    />

                    <ReferenceLine y={0} stroke="#94a3b8" />

                    <Tooltip formatter={(v) => `${v}%`} />

                    <Bar dataKey="variance_pct" name="Variance %" radius={[4, 4, 0, 0]} barSize={22}>
                        {data.map((entry, index) => (
                            <Cell
                                key={`var-cell-${index}`}
                                fill={entry.variance_pct >= 0 ? "#10b981" : "#dc2626"}
                            />
                        ))}
                    </Bar>

                    <Line
                        type="monotone"
                        dataKey="variance_pct"
                        stroke="#4f46e5"
                        strokeWidth={2}
                        dot={false}
                        legendType="none"
                    />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
}

export default VarianceTrendChart;
