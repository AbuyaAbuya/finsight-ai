class RecommendationEngine:

    def generate(
        self,
        kpis,
        revenue_trend,
        expense_trend,
    ):

        issues = []

        # --------------------------------------------------
        # Extract KPI Values
        # --------------------------------------------------

        cash = kpis["cash"]["value"]
        profit = kpis["profit"]["value"]

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

            issues.append({
                "priority": 90,
                "title": "Net Loss",
                "message":
                    "The company reported a net loss. "
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

            issues.append({

                "priority": 80,

                "title": "Expense Overrun",

                "message":
                    f"Operating expenses exceeded revenue during "
                    f"{', '.join(bad_months)}.",

            })

        # --------------------------------------------------
        # Healthy
        # --------------------------------------------------

        if not issues:

            issues.append({

                "priority": 1,

                "title": "Healthy Performance",

                "message":
                    "No significant financial risks were detected.",

            })

        issues.sort(
            key=lambda x: x["priority"],
            reverse=True,
        )

        return issues[0]