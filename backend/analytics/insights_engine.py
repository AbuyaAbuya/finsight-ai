from backend.analytics.recommendation_engine import RecommendationEngine


class InsightsEngine:

    def generate(
        self,
        revenue_trend,
        expense_trend,
        kpis,
    ):

        # -----------------------------------------------------
        # Extract KPI Values
        # -----------------------------------------------------

        total_revenue = kpis["revenue"]["value"]
        total_expenses = kpis["expenses"]["value"]
        total_profit = kpis["profit"]["value"]
        total_cash = kpis["cash"]["value"]

        # -----------------------------------------------------
        # Revenue
        # -----------------------------------------------------

        peak_revenue = max(
            revenue_trend,
            key=lambda x: x["revenue"],
        )

        revenue_insight = {
            "title": "Revenue",
            "status": "positive",
            "message": (
                f"Revenue totalled {total_revenue:,.0f}. "
                f"The highest revenue was recorded in "
                f"{peak_revenue['month']} "
                f"({peak_revenue['revenue']:,.0f})."
            ),
        }

        # -----------------------------------------------------
        # Expenses
        # -----------------------------------------------------

        peak_expense = max(
            expense_trend,
            key=lambda x: x["expenses"],
        )

        months_above = []

        for revenue, expense in zip(
            revenue_trend,
            expense_trend,
        ):

            if expense["expenses"] > revenue["revenue"]:
                months_above.append(revenue["month"])

        if months_above:

            expense_status = "warning"

            expense_message = (
                f"Operating expenses exceeded revenue during "
                f"{', '.join(months_above)}. "
                f"The highest operating expenses occurred in "
                f"{peak_expense['month']}."
            )

        else:

            expense_status = "positive"

            expense_message = (
                "Revenue remained above operating expenses throughout the selected period."
            )

        expense_insight = {
            "title": "Expenses",
            "status": expense_status,
            "message": expense_message,
        }

        # -----------------------------------------------------
        # Profitability
        # -----------------------------------------------------

        if total_revenue != 0:
            margin = (total_profit / total_revenue) * 100
        else:
            margin = 0

        if margin >= 20:
            status = "positive"
        elif margin >= 10:
            status = "warning"
        else:
            status = "negative"

        profit_insight = {
            "title": "Profitability",
            "status": status,
            "message": (
                f"Net profit amounted to "
                f"{total_profit:,.0f} "
                f"representing a "
                f"{margin:.1f}% profit margin."
            ),
        }

        # -----------------------------------------------------
        # Cash
        # -----------------------------------------------------

        if total_cash < 0:

            cash_status = "negative"

            cash_message = (
                f"Cash & Cash Equivalents closed at "
                f"{total_cash:,.0f}. "
                f"This requires immediate liquidity review."
            )

        else:

            cash_status = "positive"

            cash_message = (
                f"Cash & Cash Equivalents closed at "
                f"{total_cash:,.0f}."
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