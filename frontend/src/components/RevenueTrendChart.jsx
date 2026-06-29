import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

function RevenueTrendChart({ data }) {
    return (
        <div className="bg-white rounded-xl shadow p-6">

            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-xl font-semibold text-slate-800">
                        Revenue Trend
                    </h2>

                    <p className="text-sm text-slate-500">
                        Monthly Revenue
                    </p>
                </div>
            </div>

            <ResponsiveContainer
                width="100%"
                height={350}
            >
                <LineChart
                    data={data}
                    margin={{
                        top: 10,
                        right: 20,
                        left: 20,
                        bottom: 10,
                    }}
                >

                    <CartesianGrid
                        strokeDasharray="3 3"
                    />

                    <XAxis
                        dataKey="month"
                    />

                    <YAxis
                        tickFormatter={(value) =>
                            Number(value).toLocaleString()
                        }
                    />

                    <Tooltip
                        formatter={(value) =>
                            Number(value).toLocaleString()
                        }
                    />

                    <Line
                        type="monotone"
                        dataKey="revenue"
                        stroke="#2563eb"
                        strokeWidth={3}
                        dot={{
                            r: 4,
                        }}
                        activeDot={{
                            r: 7,
                        }}
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>
    );
}

export default RevenueTrendChart;