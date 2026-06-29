import {
    ResponsiveContainer,
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

function ExpenseTrendChart({ data }) {

    return (

        <div className="bg-white rounded-xl shadow p-6">

            <div className="flex items-center justify-between mb-6">

                <div>

                    <h2 className="text-xl font-semibold text-slate-800">
                        Expense Trend
                    </h2>

                    <p className="text-sm text-slate-500">
                        Monthly Operating Expenses
                    </p>

                </div>

            </div>

            <ResponsiveContainer
                width="100%"
                height={350}
            >

                <AreaChart
                    data={data}
                    margin={{
                        top: 10,
                        right: 20,
                        left: 20,
                        bottom: 10,
                    }}
                >

                    <CartesianGrid strokeDasharray="3 3" />

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

                    <Area
                        type="monotone"
                        dataKey="expenses"
                        stroke="#dc2626"
                        fill="#fecaca"
                        strokeWidth={3}
                    />

                </AreaChart>

            </ResponsiveContainer>

        </div>

    );

}

export default ExpenseTrendChart;