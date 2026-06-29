class VarianceEngine:
    """
    Performs variance analysis on GL accounts.
    """

    def analyse_accounts(self, current, previous):

        previous_lookup = {
            row["account"]: row["amount"]
            for row in previous
        }

        results = []

        for row in current:

            account = row["account"]

            current_amount = row["amount"]

            previous_amount = previous_lookup.get(
                account,
                0,
            )

            variance = current_amount - previous_amount

            percent = 0

            if previous_amount != 0:

                percent = (
                    variance / previous_amount
                ) * 100

            results.append({

                "account": account,

                "current": current_amount,

                "previous": previous_amount,

                "variance": variance,

                "percent": round(percent, 1),

            })

        results.sort(

            key=lambda x: abs(x["variance"]),

            reverse=True,

        )

        return results