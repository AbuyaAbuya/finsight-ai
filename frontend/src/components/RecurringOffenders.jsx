import { AlertTriangle } from "lucide-react";

function formatMoney(value) {
    const n = Number(value) || 0;
    const abs = Math.abs(n).toLocaleString(undefined, { maximumFractionDigits: 0 });
    return n < 0 ? `(${abs})` : abs;
}

function RecurringOffenders({ offenders }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="text-lg font-semibold text-slate-800">Recurring Offenders</h3>
            <p className="text-sm text-slate-500 mb-5">
                Accounts unfavorable for 3 or more consecutive months
            </p>

            {(!offenders || offenders.length === 0) ? (
                <div className="text-sm text-slate-500 py-6 text-center">
                    No account has been unfavorable for 3+ consecutive months.
                </div>
            ) : (
                <div className="space-y-3">
                    {offenders.map((o, idx) => (
                        <div
                            key={idx}
                            className="flex items-center justify-between border border-rose-100 bg-rose-50 rounded-lg px-4 py-3"
                        >
                            <div className="flex items-center gap-3">
                                <AlertTriangle size={18} className="text-rose-600 shrink-0" />
                                <div>
                                    <div className="font-medium text-slate-800">{o.account}</div>
                                    <div className="text-xs text-slate-500">
                                        {o.consecutive_months} consecutive months
                                    </div>
                                </div>
                            </div>
                            <div className="text-rose-600 font-semibold tabular-nums">
                                {formatMoney(o.total_unfavorable_variance)}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default RecurringOffenders;
