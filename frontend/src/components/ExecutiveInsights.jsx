import {
    Brain,
    TrendingUp,
    TrendingDown,
    Wallet,
    BadgeDollarSign,
    Lightbulb,
    CheckCircle2,
    AlertTriangle,
    XCircle,
} from "lucide-react";

function ExecutiveInsights({ insights }) {

    if (!insights) return null;

    const { sections, recommendation } = insights;

    function getIcon(title) {

        switch (title) {

            case "Revenue":
                return (
                    <TrendingUp
                        size={22}
                        className="text-emerald-600"
                    />
                );

            case "Expenses":
                return (
                    <TrendingDown
                        size={22}
                        className="text-amber-600"
                    />
                );

            case "Profitability":
                return (
                    <BadgeDollarSign
                        size={22}
                        className="text-blue-600"
                    />
                );

            case "Cash Position":
                return (
                    <Wallet
                        size={22}
                        className="text-cyan-600"
                    />
                );

            default:
                return (
                    <Brain
                        size={22}
                    />
                );

        }

    }

    function getStatusStyle(status) {

        switch (status) {

            case "positive":

                return {

                    bg: "bg-emerald-50",

                    border: "border-emerald-200",

                    badge: (
                        <CheckCircle2
                            size={18}
                            className="text-emerald-600"
                        />
                    ),

                };

            case "warning":

                return {

                    bg: "bg-amber-50",

                    border: "border-amber-200",

                    badge: (
                        <AlertTriangle
                            size={18}
                            className="text-amber-600"
                        />
                    ),

                };

            default:

                return {

                    bg: "bg-red-50",

                    border: "border-red-200",

                    badge: (
                        <XCircle
                            size={18}
                            className="text-red-600"
                        />
                    ),

                };

        }

    }

    return (

        <div className="rounded-2xl bg-white shadow-lg border border-slate-200 overflow-hidden">

            {/* Header */}

            <div className="bg-gradient-to-r from-indigo-700 to-blue-700 px-8 py-6">

                <div className="flex items-center gap-4">

                    <div className="h-14 w-14 rounded-xl bg-white/20 flex items-center justify-center">

                        <Brain
                            size={30}
                            className="text-white"
                        />

                    </div>

                    <div>

                        <h2 className="text-2xl font-bold text-white">

                            Executive Insights

                        </h2>

                        <p className="text-blue-100">

                            Financial Intelligence Summary

                        </p>

                    </div>

                </div>

            </div>

            {/* Insight Cards */}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-8">

                {sections.map((section, index) => {

                    const style = getStatusStyle(section.status);

                    return (

                        <div

                            key={index}

                            className={`${style.bg} ${style.border} border rounded-xl p-6 transition hover:shadow-md`}

                        >

                            <div className="flex items-center justify-between mb-5">

                                <div className="flex items-center gap-3">

                                    {getIcon(section.title)}

                                    <h3 className="font-bold text-lg text-slate-800">

                                        {section.title}

                                    </h3>

                                </div>

                                {style.badge}

                            </div>

                            <p className="text-slate-700 leading-7">

                                {section.message}

                            </p>

                        </div>

                    );

                })}

            </div>

            {/* Recommendation */}

            <div className="border-t border-slate-200 bg-slate-50 px-8 py-8">

                <div className="flex items-start gap-5">

                    <div className="h-14 w-14 rounded-xl bg-amber-100 flex items-center justify-center">

                        <Lightbulb

                            size={28}

                            className="text-amber-600"

                        />

                    </div>

                    <div className="flex-1">

                        <h3 className="text-xl font-bold text-slate-800">

                            {recommendation.title}

                        </h3>

                        <p className="mt-3 text-slate-700 leading-8">

                            {recommendation.message}

                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default ExecutiveInsights;