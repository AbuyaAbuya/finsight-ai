import {
    ResponsiveContainer,
    ComposedChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ReferenceLine,
} from "recharts";

function formatNumber(value) {
    return Number(value).toLocaleString();
}

function ForecastChart({ data, transitionLabel }) {
    if (!data || data.length === 0) return null;

    return (
        <div className="bg-white rounded-xl shadow p-6">
            <div className="mb-6">
                <h2 className="text-xl font-semibold text-slate-800">
                    Revenue, Expenses & Profit Forecast
                </h2>
                <p className="text-sm text-slate-500">
                    Solid lines are historical actuals; dashed lines are the
                    projected forecast
                </p>
            </div>

            <ResponsiveContainer width="100%" height={380}>
                <ComposedChart data={data} margin={{ top: 10, right: 20, left: 20, bottom: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />

                    <XAxis dataKey="label" tick={{ fill: "#64748b", fontSize: 11 }} />

                    <YAxis tickFormatter={formatNumber} tick={{ fill: "#64748b", fontSize: 12 }} />

                    <Tooltip formatter={formatNumber} />

                    <Legend
                        wrapperStyle={{ paddingTop: 16 }}
                        formatter={(value) => (
                            <span className="text-slate-600 text-sm">{value}</span>
                        )}
                    />

                    {transitionLabel && (
                        <ReferenceLine
                            x={transitionLabel}
                            stroke="#94a3b8"
                            strokeDasharray="2 2"
                            label={{ value: "Forecast starts", position: "top", fill: "#94a3b8", fontSize: 11 }}
                        />
                    )}

                    <Line
                        type="monotone"
                        dataKey="actualRevenue"
                        name="Revenue (Actual)"
                        stroke="#10b981"
                        strokeWidth={2.5}
                        dot={false}
                        connectNulls={false}
                    />
                    <Line
                        type="monotone"
                        dataKey="forecastRevenue"
                        name="Revenue (Forecast)"
                        stroke="#10b981"
                        strokeWidth={2.5}
                        strokeDasharray="6 4"
                        dot={false}
                        connectNulls={false}
                    />

                    <Line
                        type="monotone"
                        dataKey="actualExpenses"
                        name="Expenses (Actual)"
                        stroke="#f87171"
                        strokeWidth={2.5}
                        dot={false}
                        connectNulls={false}
                    />
                    <Line
                        type="monotone"
                        dataKey="forecastExpenses"
                        name="Expenses (Forecast)"
                        stroke="#f87171"
                        strokeWidth={2.5}
                        strokeDasharray="6 4"
                        dot={false}
                        connectNulls={false}
                    />

                    <Line
                        type="monotone"
                        dataKey="actualProfit"
                        name="Net Profit (Actual)"
                        stroke="#4f46e5"
                        strokeWidth={2.5}
                        dot={false}
                        connectNulls={false}
                    />
                    <Line
                        type="monotone"
                        dataKey="forecastProfit"
                        name="Net Profit (Forecast)"
                        stroke="#4f46e5"
                        strokeWidth={2.5}
                        strokeDasharray="6 4"
                        dot={false}
                        connectNulls={false}
                    />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
}

export default ForecastChart;
