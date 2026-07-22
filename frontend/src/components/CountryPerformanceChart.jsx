import {
    ResponsiveContainer,
    ScatterChart,
    Scatter,
    XAxis,
    YAxis,
    ZAxis,
    CartesianGrid,
    Tooltip,
    ReferenceLine,
    Cell,
    LabelList,
} from "recharts";

function formatNumber(value) {
    return Number(value).toLocaleString();
}

function CustomTooltip({ active, payload }) {
    if (!active || !payload || payload.length === 0) return null;

    const d = payload[0].payload;

    return (
        <div className="bg-white border border-slate-200 rounded-lg shadow-lg p-4 text-sm">
            <div className="font-semibold text-slate-800 mb-2">{d.country}</div>
            <div className="text-slate-600">Revenue: {formatNumber(d.revenue)}</div>
            <div className="text-slate-600">Expenses: {formatNumber(d.expenses)}</div>
            <div className={d.profit >= 0 ? "text-emerald-600" : "text-rose-600"}>
                Net Profit: {formatNumber(d.profit)}
            </div>
            <div className="text-slate-500 mt-1">
                Margin: {d.margin.toFixed(1)}%
            </div>
        </div>
    );
}

function CountryPerformanceChart({ data }) {

    if (!data || data.length === 0) {
        return null;
    }

    const chartData = data.map((d) => ({
        ...d,
        margin: d.revenue !== 0 ? (d.profit / d.revenue) * 100 : 0,
        bubbleSize: Math.max(Math.abs(d.profit), d.revenue * 0.02),
    }));

    return (
        <div className="bg-white rounded-xl shadow p-6">

            <div className="mb-6">
                <h2 className="text-xl font-semibold text-slate-800">
                    Performance by Country
                </h2>

                <p className="text-sm text-slate-500">
                    Revenue vs Net Margin — bubble size reflects profit magnitude.
                    Markets below the line are operating at a loss.
                </p>
            </div>

            <ResponsiveContainer width="100%" height={420}>
                <ScatterChart margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />

                    <XAxis
                        type="number"
                        dataKey="revenue"
                        name="Revenue"
                        tickFormatter={formatNumber}
                        tick={{ fill: "#64748b", fontSize: 12 }}
                        label={{
                            value: "Revenue",
                            position: "insideBottom",
                            offset: -10,
                            fill: "#94a3b8",
                            fontSize: 12,
                        }}
                    />

                    <YAxis
                        type="number"
                        dataKey="margin"
                        name="Net Margin"
                        tickFormatter={(v) => `${v}%`}
                        tick={{ fill: "#64748b", fontSize: 12 }}
                        label={{
                            value: "Net Margin %",
                            angle: -90,
                            position: "insideLeft",
                            fill: "#94a3b8",
                            fontSize: 12,
                        }}
                    />

                    <ZAxis dataKey="bubbleSize" range={[400, 2200]} />

                    <ReferenceLine
                        y={0}
                        stroke="#cbd5e1"
                        strokeDasharray="4 4"
                        label={{
                            value: "Break-even",
                            position: "right",
                            fill: "#94a3b8",
                            fontSize: 11,
                        }}
                    />

                    <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: "3 3" }} />

                    <Scatter data={chartData} fillOpacity={0.85}>
                        {chartData.map((entry, index) => (
                            <Cell
                                key={`country-cell-${index}`}
                                fill={entry.profit >= 0 ? "#10b981" : "#dc2626"}
                            />
                        ))}
                        <LabelList
                            dataKey="country"
                            position="top"
                            style={{ fill: "#334155", fontSize: 12, fontWeight: 600 }}
                        />
                    </Scatter>
                </ScatterChart>
            </ResponsiveContainer>

        </div>
    );
}

export default CountryPerformanceChart;
