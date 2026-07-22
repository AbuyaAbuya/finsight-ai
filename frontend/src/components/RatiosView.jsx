function formatRatio(value, suffix = "x") {
    if (value === null || value === undefined) return "N/A";
    return `${Number(value).toFixed(2)}${suffix}`;
}

function formatPercent(value) {
    if (value === null || value === undefined) return "N/A";
    return `${(Number(value) * 100).toFixed(1)}%`;
}

const TIER_STYLES = {
    good: "bg-emerald-50 text-emerald-700 border-emerald-200",
    fair: "bg-amber-50 text-amber-700 border-amber-200",
    weak: "bg-rose-50 text-rose-700 border-rose-200",
    neutral: "bg-slate-50 text-slate-500 border-slate-200",
};

function tierBadge(tier, label) {
    return (
        <span
            className={`text-xs font-semibold px-2 py-1 rounded-full border ${TIER_STYLES[tier]}`}
        >
            {label}
        </span>
    );
}

function tierFromThresholds(value, good, fair) {
    if (value === null || value === undefined) return "neutral";
    if (value >= good) return "good";
    if (value >= fair) return "fair";
    return "weak";
}

function RatioTile({ label, value, tier, tierLabel, description }) {
    return (
        <div className="border border-slate-200 rounded-xl p-5">
            <div className="flex items-start justify-between gap-3">
                <div>
                    <div className="text-sm text-slate-500">{label}</div>
                    <div className="text-2xl font-bold text-slate-800 mt-1">
                        {value}
                    </div>
                </div>
                {tierBadge(tier, tierLabel)}
            </div>
            <p className="text-xs text-slate-500 mt-3">{description}</p>
        </div>
    );
}

function Section({ title, subtitle, children }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
            <p className="text-sm text-slate-500 mb-5">{subtitle}</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">{children}</div>
        </div>
    );
}

function RatiosView({ ratios }) {
    if (!ratios) {
        return (
            <div className="bg-white rounded-xl border border-slate-200 p-10 text-center text-slate-500">
                No data available for the selected filters.
            </div>
        );
    }

    const { liquidity, profitability, leverage, efficiency } = ratios;

    const currentTier = tierFromThresholds(liquidity.current_ratio, 2, 1);
    const quickTier = tierFromThresholds(liquidity.quick_ratio, 1, 0.5);
    const cashTier = tierFromThresholds(liquidity.cash_ratio, 0.5, 0.2);

    const grossMarginTier = tierFromThresholds(profitability.gross_margin, 0.4, 0.2);
    const netMarginTier = tierFromThresholds(profitability.net_margin, 0.15, 0.05);
    const roeTier = tierFromThresholds(profitability.return_on_equity, 0.15, 0.08);

    const assetTurnoverTier = tierFromThresholds(efficiency.asset_turnover, 1, 0.5);
    const inventoryTurnoverTier = tierFromThresholds(efficiency.inventory_turnover, 6, 3);
    const receivablesTurnoverTier = tierFromThresholds(efficiency.receivables_turnover, 8, 4);

    // Leverage isn't "good/bad" in the same directional sense as the
    // others -- lower is safer but not automatically better -- so it
    // gets a distinct Low/Moderate/High framing instead of Good/Fair/Weak.
    const debtToEquityLevel =
        leverage.debt_to_equity === null
            ? { tier: "neutral", label: "N/A" }
            : leverage.debt_to_equity <= 0.5
            ? { tier: "good", label: "Low" }
            : leverage.debt_to_equity <= 1.5
            ? { tier: "fair", label: "Moderate" }
            : { tier: "weak", label: "High" };

    return (
        <div className="space-y-6">

            <Section
                title="Liquidity"
                subtitle="Ability to cover short-term obligations"
            >
                <RatioTile
                    label="Current Ratio"
                    value={formatRatio(liquidity.current_ratio)}
                    tier={currentTier}
                    tierLabel={currentTier === "good" ? "Strong" : currentTier === "fair" ? "Adequate" : "Weak"}
                    description="Current assets relative to current liabilities. Above 2x is comfortably covered."
                />
                <RatioTile
                    label="Quick Ratio"
                    value={formatRatio(liquidity.quick_ratio)}
                    tier={quickTier}
                    tierLabel={quickTier === "good" ? "Strong" : quickTier === "fair" ? "Adequate" : "Weak"}
                    description="Current assets excluding inventory, relative to current liabilities."
                />
                <RatioTile
                    label="Cash Ratio"
                    value={formatRatio(liquidity.cash_ratio)}
                    tier={cashTier}
                    tierLabel={cashTier === "good" ? "Strong" : cashTier === "fair" ? "Adequate" : "Weak"}
                    description="Cash alone relative to current liabilities -- the most conservative liquidity measure."
                />
            </Section>

            <Section
                title="Profitability"
                subtitle="How efficiently revenue converts to profit"
            >
                <RatioTile
                    label="Gross Margin"
                    value={formatPercent(profitability.gross_margin)}
                    tier={grossMarginTier}
                    tierLabel={grossMarginTier === "good" ? "Strong" : grossMarginTier === "fair" ? "Adequate" : "Thin"}
                    description="Revenue remaining after direct cost of sales."
                />
                <RatioTile
                    label="Net Margin"
                    value={formatPercent(profitability.net_margin)}
                    tier={netMarginTier}
                    tierLabel={netMarginTier === "good" ? "Strong" : netMarginTier === "fair" ? "Adequate" : "Thin"}
                    description="Revenue remaining after all expenses, interest, and tax."
                />
                <RatioTile
                    label="Return on Equity"
                    value={formatPercent(profitability.return_on_equity)}
                    tier={roeTier}
                    tierLabel={roeTier === "good" ? "Strong" : roeTier === "fair" ? "Adequate" : "Weak"}
                    description="Net profit relative to shareholder equity."
                />
                <RatioTile
                    label="Operating Margin"
                    value={formatPercent(profitability.operating_margin)}
                    tier="neutral"
                    tierLabel="Info"
                    description="Profit from core operations before non-operating items, interest, and tax."
                />
                <RatioTile
                    label="Return on Assets"
                    value={formatPercent(profitability.return_on_assets)}
                    tier="neutral"
                    tierLabel="Info"
                    description="Net profit relative to total assets deployed."
                />
            </Section>

            <Section
                title="Leverage"
                subtitle="How the business is financed -- debt vs equity"
            >
                <RatioTile
                    label="Debt-to-Equity"
                    value={formatRatio(leverage.debt_to_equity)}
                    tier={debtToEquityLevel.tier}
                    tierLabel={debtToEquityLevel.label}
                    description="Total liabilities relative to shareholder equity. Lower means less reliance on debt financing."
                />
                <RatioTile
                    label="Debt Ratio"
                    value={formatPercent(leverage.debt_ratio)}
                    tier="neutral"
                    tierLabel="Info"
                    description="Share of total assets financed by liabilities rather than equity."
                />
                <RatioTile
                    label="Equity Ratio"
                    value={formatPercent(leverage.equity_ratio)}
                    tier="neutral"
                    tierLabel="Info"
                    description="Share of total assets financed by shareholder equity."
                />
            </Section>

            <Section
                title="Efficiency"
                subtitle="How productively assets and working capital are used"
            >
                <RatioTile
                    label="Asset Turnover"
                    value={formatRatio(efficiency.asset_turnover)}
                    tier={assetTurnoverTier}
                    tierLabel={assetTurnoverTier === "good" ? "Strong" : assetTurnoverTier === "fair" ? "Adequate" : "Weak"}
                    description="Revenue generated per dollar of total assets."
                />
                <RatioTile
                    label="Inventory Turnover"
                    value={formatRatio(efficiency.inventory_turnover)}
                    tier={inventoryTurnoverTier}
                    tierLabel={inventoryTurnoverTier === "good" ? "Strong" : inventoryTurnoverTier === "fair" ? "Adequate" : "Slow"}
                    description="How many times inventory is sold and replaced over the period."
                />
                <RatioTile
                    label="Receivables Turnover"
                    value={formatRatio(efficiency.receivables_turnover)}
                    tier={receivablesTurnoverTier}
                    tierLabel={receivablesTurnoverTier === "good" ? "Strong" : receivablesTurnoverTier === "fair" ? "Adequate" : "Slow"}
                    description="How many times receivables are collected over the period."
                />
            </Section>

        </div>
    );
}

export default RatiosView;
