import {
    TrendingUp,
    TrendingDown,
    Wallet,
} from "lucide-react";

function FinancialDrivers({

    revenueDrivers,

    expenseDrivers,

    cashBreakdown,

}) {

    function currency(value) {

        return Number(value).toLocaleString();

    }

    return (

        <div className="bg-white rounded-2xl shadow-lg border border-slate-200">

            {/* Header */}

            <div className="border-b border-slate-200 px-8 py-6">

                <h2 className="text-2xl font-bold text-slate-800">

                    Financial Intelligence

                </h2>

                <p className="text-slate-500 mt-1">

                    Key drivers behind financial performance

                </p>

            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 p-8">

                {/* Revenue */}

                <div>

                    <div className="flex items-center gap-3 mb-5">

                        <TrendingUp
                            className="text-emerald-600"
                        />

                        <h3 className="font-bold text-lg">

                            Revenue Drivers

                        </h3>

                    </div>

                    {revenueDrivers.map((driver, index) => (

                        <div

                            key={index}

                            className="mb-5"

                        >

                            <div className="flex justify-between">

                                <span className="font-medium">

                                    {driver.account}

                                </span>

                                <span className="font-semibold">

                                    {driver.percent}%

                                </span>

                            </div>

                            <div className="w-full bg-slate-200 rounded-full h-2 mt-2">

                                <div

                                    className="bg-emerald-500 h-2 rounded-full"

                                    style={{
                                        width: `${driver.percent}%`,
                                    }}

                                />

                            </div>

                            <div className="text-sm text-slate-500 mt-1">

                                KES {currency(driver.amount)}

                            </div>

                        </div>

                    ))}

                </div>

                {/* Expenses */}

                <div>

                    <div className="flex items-center gap-3 mb-5">

                        <TrendingDown
                            className="text-red-600"
                        />

                        <h3 className="font-bold text-lg">

                            Expense Drivers

                        </h3>

                    </div>

                    {expenseDrivers.map((driver, index) => (

                        <div

                            key={index}

                            className="mb-5"

                        >

                            <div className="flex justify-between">

                                <span className="font-medium">

                                    {driver.account}

                                </span>

                                <span className="font-semibold">

                                    {driver.percent}%

                                </span>

                            </div>

                            <div className="w-full bg-slate-200 rounded-full h-2 mt-2">

                                <div

                                    className="bg-red-500 h-2 rounded-full"

                                    style={{
                                        width: `${driver.percent}%`,
                                    }}

                                />

                            </div>

                            <div className="text-sm text-slate-500 mt-1">

                                KES {currency(driver.amount)}

                            </div>

                        </div>

                    ))}

                </div>

                {/* Cash */}

                <div>

                    <div className="flex items-center gap-3 mb-5">

                        <Wallet
                            className="text-blue-600"
                        />

                        <h3 className="font-bold text-lg">

                            Cash Composition

                        </h3>

                    </div>

                    {cashBreakdown.map((cash, index) => (

                        <div

                            key={index}

                            className="flex justify-between items-center py-4 border-b border-slate-100"

                        >

                            <span className="font-medium">

                                {cash.account}

                            </span>

                            <span className="font-bold text-blue-700">

                                KES {currency(cash.amount)}

                            </span>

                        </div>

                    ))}

                </div>

            </div>

        </div>

    );

}

export default FinancialDrivers;