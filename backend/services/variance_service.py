from backend.services.budget_service import BudgetService, CREDIT_NORMAL_ACCOUNTS

# Category groupings for the rollup view. Each category is internally
# consistent in one sense (all its accounts roll into one line item on
# the Income Statement) but NOT always uniform in normal-balance type
# (Revenue mixes Sales, credit-normal, with Sales Return, a debit-normal
# contra account) -- so category totals are built from each account's
# own "adjusted_variance" (positive = favorable), not a naive sum of
# raw variances, to avoid Sales Return's favorable-when-lower direction
# being counted the wrong way.
CATEGORIES = {
    "Revenue": ["Sales", "Sales Return"],
    "Cost of Sales": ["Cost of Sales"],
    "Operating Expenses": [
        "Staff Costs", "Commissions", "Advertisements", "Travel",
        "Entertainment", "Office Supplies", "Professional Services",
        "Telephone", "Utilities", "Other Expenses",
    ],
    "Depreciation & Amortization": ["Equipment", "Amortization of Intangible Assets"],
    "Non-Operating": [
        "Interest Income", "Dividend Income",
        "Gain/Loss on Sales of Asset", "Exchange Loss/Gain",
    ],
    "Interest & Tax": ["Interest Expense", "Taxation"],
}

ACCOUNT_TO_CATEGORY = {
    account: category
    for category, accounts in CATEGORIES.items()
    for account in accounts
}


class VarianceAnalysisService:

    def __init__(self):
        self.budget_service = BudgetService()

    def get_variance_analysis(self, year, country=None):

        rows = self.budget_service.get_budget_vs_actual(year, country)

        # If every budget line is 0, there's no real baseline to compare
        # against (e.g. the first year in the dataset, with no prior
        # year's actuals to build a budget from). In that case, a %
        # variance is meaningless (division by a zero budget), while
        # the dollar variance would just equal the raw actual amount --
        # not a genuine deviation from any plan. Surface this clearly
        # instead of showing an inconsistent partial view.
        total_budget_magnitude = sum(abs(r["budget"]) for r in rows)

        if total_budget_magnitude == 0:
            return {
                "has_baseline": False,
                "monthly_trend": [],
                "recurring_offenders": [],
                "category_rollups": [],
                "narrative": [],
            }

        for r in rows:
            credit_normal = r["account"] in CREDIT_NORMAL_ACCOUNTS
            # Positive adjusted_variance always means favorable,
            # regardless of the account's own normal-balance direction.
            r["adjusted_variance"] = r["variance"] if credit_normal else -r["variance"]
            r["category"] = ACCOUNT_TO_CATEGORY.get(r["account"], "Other")

        monthly_trend = self._monthly_trend(rows)
        recurring_offenders = self._recurring_offenders(rows)
        category_rollups = self._category_rollups(rows)
        narrative = self._build_narrative(monthly_trend, recurring_offenders, category_rollups)

        return {
            "has_baseline": True,
            "monthly_trend": monthly_trend,
            "recurring_offenders": recurring_offenders,
            "category_rollups": category_rollups,
            "narrative": narrative,
        }

    # ==========================================================
    # 1. VARIANCE TREND OVER TIME
    # ==========================================================

    def _monthly_trend(self, rows):

        months = sorted(set((r["month_number"], r["month"]) for r in rows))
        trend = []

        for month_number, month in months:
            month_rows = [r for r in rows if r["month_number"] == month_number]

            total_budget_magnitude = sum(abs(r["budget"]) for r in month_rows)
            total_adjusted_variance = sum(r["adjusted_variance"] for r in month_rows)

            variance_pct = (
                (total_adjusted_variance / total_budget_magnitude * 100)
                if total_budget_magnitude
                else 0
            )

            trend.append({
                "month": month,
                "month_number": month_number,
                "adjusted_variance": round(total_adjusted_variance, 2),
                "variance_pct": round(variance_pct, 1),
            })

        return trend

    # ==========================================================
    # 2. RECURRING OFFENDERS
    # ==========================================================

    def _recurring_offenders(self, rows):

        by_account = {}
        for r in rows:
            by_account.setdefault(r["account"], []).append(r)

        offenders = []

        for account, acc_rows in by_account.items():
            acc_rows_sorted = sorted(acc_rows, key=lambda x: x["month_number"])

            max_streak = 0
            current_streak = 0
            streak_variance = 0
            best_streak_variance = 0

            for r in acc_rows_sorted:
                if r["adjusted_variance"] < 0:
                    current_streak += 1
                    streak_variance += r["adjusted_variance"]

                    if current_streak > max_streak:
                        max_streak = current_streak
                        best_streak_variance = streak_variance
                else:
                    current_streak = 0
                    streak_variance = 0

            if max_streak >= 3:
                offenders.append({
                    "account": account,
                    "consecutive_months": max_streak,
                    "total_unfavorable_variance": round(best_streak_variance, 2),
                })

        offenders.sort(key=lambda x: x["total_unfavorable_variance"])

        return offenders[:5]

    # ==========================================================
    # 3. CATEGORY ROLLUPS
    # ==========================================================

    def _category_rollups(self, rows):

        rollups = []

        for category in CATEGORIES:
            cat_rows = [r for r in rows if r["category"] == category]

            if not cat_rows:
                continue

            total_budget = sum(r["budget"] for r in cat_rows)
            total_actual = sum(r["actual"] for r in cat_rows)
            total_adjusted_variance = sum(r["adjusted_variance"] for r in cat_rows)

            rollups.append({
                "category": category,
                "budget": round(total_budget, 2),
                "actual": round(total_actual, 2),
                "variance": round(total_actual - total_budget, 2),
                "favorable": total_adjusted_variance >= 0,
            })

        rollups.sort(key=lambda x: abs(x["variance"]), reverse=True)

        return rollups

    # ==========================================================
    # 4. NARRATIVE
    # ==========================================================

    def _build_narrative(self, monthly_trend, recurring_offenders, category_rollups):

        insights = []

        if len(monthly_trend) >= 2:
            midpoint = len(monthly_trend) // 2
            first_half = monthly_trend[:midpoint]
            second_half = monthly_trend[midpoint:]

            avg_first = sum(m["variance_pct"] for m in first_half) / len(first_half)
            avg_second = sum(m["variance_pct"] for m in second_half) / len(second_half)

            if avg_second < avg_first - 2:
                insights.append(
                    f"Overall variance has been widening — the second half of the "
                    f"year averaged {avg_second:.1f}% vs {avg_first:.1f}% in the "
                    f"first half. Worth checking whether this is a structural "
                    f"shift or a temporary spike."
                )
            elif avg_second > avg_first + 2:
                insights.append(
                    f"Overall variance has been improving — the second half of "
                    f"the year averaged {avg_second:.1f}% vs {avg_first:.1f}% in "
                    f"the first half."
                )
            else:
                insights.append(
                    "Overall variance has stayed fairly consistent across the "
                    "year, with no clear improving or worsening trend."
                )

        if recurring_offenders:
            worst = recurring_offenders[0]
            insights.append(
                f"{worst['account']} has been unfavorable for "
                f"{worst['consecutive_months']} consecutive months, the longest "
                f"recurring pattern this year — this looks structural rather "
                f"than a one-off and is worth a dedicated review."
            )
        else:
            insights.append(
                "No account has been unfavorable for 3 or more consecutive "
                "months — deviations so far look like isolated events rather "
                "than a persistent pattern."
            )

        if category_rollups:
            worst_cat = category_rollups[0]
            direction = "under" if worst_cat["favorable"] else "over"
            insights.append(
                f"{worst_cat['category']} carries the largest variance this "
                f"year ({worst_cat['variance']:,.0f}, running {direction} plan) "
                f"— start any deeper investigation there."
            )

        return insights

    def close(self):
        self.budget_service.close()
