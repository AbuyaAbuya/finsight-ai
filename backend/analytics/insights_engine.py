from backend.analytics.recommendation_engine import RecommendationEngine


class InsightsEngine:

    def generate(
        self,
        revenue_trend,
        expense_trend,
        profit_trend,
        expense_drivers,
        country_performance,
        kpis,
    ):

        # -----------------------------------------------------
        # Extract KPI Values (used for decision logic only --
        # never restated verbatim, since they're already on the
        # KPI cards)
        # -----------------------------------------------------

        total_revenue = kpis["revenue"]["value"]
        total_profit = kpis["profit"]["value"]
        total_cash = kpis["cash"]["value"]

        top_expense_driver = expense_drivers[0] if expense_drivers else None

        # -----------------------------------------------------
        # Revenue -- identify the pattern (peak vs trough) and
        # advise on what to do about it, rather than restating
        # the total already shown on the KPI card.
        # -----------------------------------------------------

        if revenue_trend:

            peak_revenue = max(revenue_trend, key=lambda x: x["revenue"])
            trough_revenue = min(revenue_trend, key=lambda x: x["revenue"])

            if len(revenue_trend) > 1 and peak_revenue["month"] != trough_revenue["month"]:

                spread = (
                    (peak_revenue["revenue"] - trough_revenue["revenue"])
                    / abs(trough_revenue["revenue"])
                    * 100
                    if trough_revenue["revenue"] != 0
                    else 0
                )

                if spread >= 30:
                    revenue_status = "warning"
                    revenue_message = (
                        f"Revenue swung sharply between {trough_revenue['month']} and "
                        f"{peak_revenue['month']} ({spread:.0f}% spread) — investigate what "
                        f"drove {peak_revenue['month']}'s strength and see if it can be "
                        f"replicated ahead of the next {trough_revenue['month']}-like period."
                    )
                else:
                    revenue_status = "positive"
                    revenue_message = (
                        f"Revenue held fairly steady across the period, with "
                        f"{peak_revenue['month']} slightly ahead — a stable base to plan "
                        f"next period's targets from."
                    )
            else:
                revenue_status = "positive"
                revenue_message = (
                    "Only one period of data is in view — select a wider range to "
                    "see revenue trend patterns."
                )

        else:
            revenue_status = "warning"
            revenue_message = "No revenue activity in the selected period."

        revenue_insight = {
            "title": "Revenue",
            "status": revenue_status,
            "message": revenue_message,
        }

        # -----------------------------------------------------
        # Expenses -- name the specific top cost driver so the
        # advice is actionable, not just "expenses were high."
        # -----------------------------------------------------

        months_above = []

        for revenue, expense in zip(revenue_trend, expense_trend):
            if expense["expenses"] > revenue["revenue"]:
                months_above.append(revenue["month"])

        if months_above and top_expense_driver:

            expense_status = "warning"
            expense_message = (
                f"Expenses outpaced revenue in {', '.join(months_above)} — start the "
                f"review with {top_expense_driver['account']}, the single largest cost "
                f"driver at {top_expense_driver['percent']:.0f}% of total expenses "
                f"({top_expense_driver['amount']:,.0f})."
            )

        elif months_above:

            expense_status = "warning"
            expense_message = (
                f"Expenses outpaced revenue in {', '.join(months_above)} — a closer "
                f"cost review is worth prioritizing before the next period."
            )

        elif top_expense_driver:

            expense_status = "positive"
            expense_message = (
                f"Revenue covered operating expenses throughout the period. "
                f"{top_expense_driver['account']} remains the largest cost driver at "
                f"{top_expense_driver['percent']:.0f}% of the total — worth monitoring "
                f"as the business scales."
            )

        else:

            expense_status = "positive"
            expense_message = "No expense activity in the selected period."

        expense_insight = {
            "title": "Expenses",
            "status": expense_status,
            "message": expense_message,
        }

        # -----------------------------------------------------
        # Profitability -- advise based on margin tier, naming
        # the top cost driver as the lever to pull rather than
        # just restating the margin percentage.
        # -----------------------------------------------------

        margin = (total_profit / total_revenue * 100) if total_revenue else 0
        driver_name = top_expense_driver["account"] if top_expense_driver else "top costs"

        if margin >= 20:
            profit_status = "positive"
            profit_message = (
                "Margin is healthy — a good window to reinvest surplus into growth "
                "initiatives or build a larger cash buffer for slower periods."
            )
        elif margin >= 10:
            profit_status = "warning"
            profit_message = (
                f"Margin is moderate — targeted efficiency gains in {driver_name} "
                f"could meaningfully improve profitability without cutting into growth."
            )
        elif margin >= 0:
            profit_status = "warning"
            profit_message = (
                f"Margin is thin — review pricing or renegotiate terms on "
                f"{driver_name} before committing to further expansion."
            )
        else:
            profit_status = "negative"
            profit_message = (
                f"The period ran at a loss — {driver_name} is the largest lever "
                f"available for an immediate cost review."
            )

        # Use profit_trend (consistent with the Net Profit KPI) to
        # flag the weakest month specifically, if there's a genuine
        # loss-making month worth calling out.
        if profit_trend:
            worst_month = min(profit_trend, key=lambda x: x["profit"])
            if worst_month["profit"] < 0:
                profit_message += f" {worst_month['month']} was the weakest month."

        profit_insight = {
            "title": "Profitability",
            "status": profit_status,
            "message": profit_message,
        }

        # -----------------------------------------------------
        # Cash -- advise based on position and runway relative
        # to expenses, not just restating the closing balance.
        # -----------------------------------------------------

        total_expenses_for_runway = kpis["expenses"]["value"]
        monthly_expense_run_rate = (
            total_expenses_for_runway / len(expense_trend) if expense_trend else 0
        )
        months_of_runway = (
            total_cash / monthly_expense_run_rate if monthly_expense_run_rate else None
        )

        if total_cash < 0:
            cash_status = "negative"
            cash_message = (
                "Cash position is negative — pause discretionary spend and "
                "accelerate receivable collections immediately."
            )
        elif months_of_runway is not None and months_of_runway < 1:
            cash_status = "warning"
            cash_message = (
                f"Cash covers under a month of current spend (~{months_of_runway:.1f} "
                f"months) — build a buffer before taking on new commitments."
            )
        elif months_of_runway is not None and months_of_runway < 3:
            cash_status = "warning"
            cash_message = (
                f"Cash reserves cover roughly {months_of_runway:.1f} months of "
                f"spend — comfortable for now, but worth strengthening before "
                f"any major outlay."
            )
        else:
            cash_status = "positive"
            cash_message = (
                "Cash reserves are strong relative to current spend — a "
                "reasonable window to invest in growth or pay down higher-cost "
                "liabilities."
            )

        cash_insight = {
            "title": "Cash Position",
            "status": cash_status,
            "message": cash_message,
        }

        # -----------------------------------------------------
        # Recommendation
        # -----------------------------------------------------

        recommendation = RecommendationEngine().generate(
            kpis,
            revenue_trend,
            expense_trend,
            expense_drivers,
            country_performance,
        )

        return {

            "sections": [
                revenue_insight,
                expense_insight,
                profit_insight,
                cash_insight,
            ],

            "recommendation": recommendation,

        }
