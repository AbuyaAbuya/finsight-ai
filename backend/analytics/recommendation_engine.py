class RecommendationEngine:

    def generate(
        self,
        kpis,
        revenue_trend,
        expense_trend,
        expense_drivers=None,
        country_performance=None,
    ):

        issues = []

        # --------------------------------------------------
        # Extract KPI Values
        # --------------------------------------------------

        cash = kpis["cash"]["value"]
        profit = kpis["profit"]["value"]

        top_expense_driver = expense_drivers[0] if expense_drivers else None

        # --------------------------------------------------
        # Cash
        # --------------------------------------------------

        if cash < 0:

            issues.append({
                "priority": 100,
                "title": "Negative Cash Position",
                "message":
                    "Cash & Cash Equivalents are negative. "
                    "Review liquidity immediately and accelerate receivable collections.",
            })

        # --------------------------------------------------
        # Profit
        # --------------------------------------------------

        if profit < 0:

            driver_note = (
                f" Start with {top_expense_driver['account']}, the largest single "
                f"cost driver."
                if top_expense_driver
                else ""
            )

            issues.append({
                "priority": 90,
                "title": "Net Loss",
                "message":
                    f"The company reported a net loss.{driver_note} "
                    "Review revenue generation and operating costs.",
            })

        # --------------------------------------------------
        # Expense Analysis
        # --------------------------------------------------

        bad_months = []

        for revenue, expense in zip(
            revenue_trend,
            expense_trend,
        ):

            if expense["expenses"] > revenue["revenue"]:

                bad_months.append(
                    revenue["month"]
                )

        if bad_months:

            driver_note = (
                f" {top_expense_driver['account']} is the largest cost driver "
                f"({top_expense_driver['percent']:.0f}% of total expenses) and the "
                f"best place to start."
                if top_expense_driver
                else ""
            )

            issues.append({

                "priority": 80,

                "title": "Expense Overrun",

                "message":
                    f"Operating expenses exceeded revenue during "
                    f"{', '.join(bad_months)}.{driver_note}",

            })

        # --------------------------------------------------
        # Country concentration / underperformance
        # --------------------------------------------------

        if country_performance and len(country_performance) > 1:

            losing_countries = [
                c for c in country_performance if c["profit"] < 0
            ]

            if losing_countries:

                worst = min(losing_countries, key=lambda c: c["profit"])

                issues.append({
                    "priority": 70,
                    "title": "Underperforming Market",
                    "message": (
                        f"{worst['country']} is operating at a loss "
                        f"({worst['profit']:,.0f}) while other markets remain "
                        f"profitable — worth a focused review of pricing or cost "
                        f"structure there specifically."
                    ),
                })

            else:

                best = max(country_performance, key=lambda c: c["profit"])
                total_profit = sum(c["profit"] for c in country_performance)

                if total_profit > 0 and best["profit"] / total_profit > 0.5:
                    issues.append({
                        "priority": 60,
                        "title": "Concentration Risk",
                        "message": (
                            f"{best['country']} drives over half of total profit — "
                            f"consider whether growth investment in other markets "
                            f"would reduce reliance on a single region."
                        ),
                    })

        # --------------------------------------------------
        # Healthy
        # --------------------------------------------------

        if not issues:

            issues.append({

                "priority": 1,

                "title": "Healthy Performance",

                "message":
                    "No significant financial risks were detected. Current cost "
                    "and cash discipline appears sustainable — a reasonable window "
                    "to invest in growth initiatives.",

            })

        issues.sort(
            key=lambda x: x["priority"],
            reverse=True,
        )

        return issues[0]
