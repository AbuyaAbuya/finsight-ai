function formatMoney(value) {
    const n = Number(value) || 0;
    const abs = Math.abs(n).toLocaleString(undefined, { maximumFractionDigits: 0 });
    return n < 0 ? `(${abs})` : abs;
}

function CategoryRollups({ rollups }) {
    if (!rollups || rollups.length === 0) return null;

    const maxAbsVariance = Math.max(...rollups.map((r) => Math.abs(r.variance)), 1);

    return (
        <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="text-lg font-semibold text-slate-800">Category Rollups</h3>
            <p className="text-sm text-slate-500 mb-5">
                Where the variance is concentrated, largest first
            </p>

            <div className="space-y-4">
                {rollups.map((r, idx) => (
                    <div key={idx}>
                        <div className="flex items-center justify-between mb-1">
                            <span className="font-medium text-slate-700 text-sm">
                                {r.category}
                            </span>
                            <span
                                className={`font-semibold text-sm ${
                                    r.favorable ? "text-emerald-600" : "text-rose-600"
                                }`}
                            >
                                {formatMoney(r.variance)}
                            </span>
                        </div>

                        <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                            <div
                                className={`h-full rounded-full ${
                                    r.favorable ? "bg-emerald-500" : "bg-rose-500"
                                }`}
                                style={{
                                    width: `${(Math.abs(r.variance) / maxAbsVariance) * 100}%`,
                                }}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CategoryRollups;
