import duckdb

DB_PATH = "database/finsight.duckdb"


class FinancialService:

    def __init__(self):
        self.conn = duckdb.connect(DB_PATH)

    # ==========================================================
    # Build WHERE Clause
    # ==========================================================

    def build_where(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        clauses = []
        params = []

        if year:
            clauses.append("year = ?")
            params.append(year)

        if quarter:
            clauses.append("quarter = ?")
            params.append(quarter)

        if month:
            clauses.append("month = ?")
            params.append(month)

        if country:
            clauses.append("country = ?")
            params.append(country)

        where = ""

        if clauses:
            where = " WHERE " + " AND ".join(clauses)

        return where, params

    # ==========================================================
    # TRIAL BALANCE
    # ==========================================================

    def trial_balance(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        query = f"""

        SELECT

            report,

            class,

            subclass,

            subclass2,

            account_key,

            account,

            CASE WHEN SUM(debit) - SUM(credit) >= 0
                 THEN SUM(debit) - SUM(credit)
                 ELSE 0
            END AS debit,

            CASE WHEN SUM(debit) - SUM(credit) < 0
                 THEN SUM(credit) - SUM(debit)
                 ELSE 0
            END AS credit

        FROM FinancialReportingMart

        {where}

        GROUP BY

            report,
            class,
            subclass,
            subclass2,
            account_key,
            account

        HAVING

            SUM(debit) - SUM(credit) <> 0

        ORDER BY

            report,
            class,
            subclass,
            account_key

        """

        return self.conn.execute(
            query,
            params,
        ).fetchdf()

    # ==========================================================
    # INCOME STATEMENT
    # ==========================================================

    def income_statement(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        query = f"""

        SELECT

            subclass,

            subclass2,

            account,

            subaccount,

            SUM(balance) AS balance

        FROM FinancialReportingMart

        {where}

        {"AND" if where else "WHERE"}

        report='Profit and Loss'

        GROUP BY

            subclass,
            subclass2,
            account,
            subaccount

        ORDER BY

            subclass,
            subclass2,
            account,
            subaccount

        """

        return self.conn.execute(
            query,
            params,
        ).fetchdf()
    # ==========================================================
    # BALANCE SHEET
    # ==========================================================

    def balance_sheet(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        # A Balance Sheet is a point-in-time snapshot of cumulative
        # balances, not a period-activity report like the Income
        # Statement. Filtering by "year = ?" would only sum that year's
        # movements and silently drop prior years' accumulated balances,
        # understating every account. So when a year is selected, we
        # filter "year <= ?" (cumulative through that year) instead of
        # an exact match. If a quarter or month is also selected within
        # that year, we further restrict to that point within the year,
        # while still including all prior years in full.

        clauses = []
        params = []

        if year:
            if month:
                clauses.append(
                    """
                    (year < ? OR (year = ? AND month_number <= (
                        SELECT MIN(month_number)
                        FROM FinancialReportingMart
                        WHERE month = ?
                    )))
                    """
                )
                params.extend([year, year, month])
            elif quarter:
                clauses.append(
                    """
                    (year < ? OR (year = ? AND
                        CAST(TRIM(REPLACE(quarter, 'Qtr', '')) AS INTEGER)
                        <= CAST(TRIM(REPLACE(?, 'Qtr', '')) AS INTEGER)
                    ))
                    """
                )
                params.extend([year, year, quarter])
            else:
                clauses.append("year <= ?")
                params.append(year)
        elif quarter:
            # Quarter without a year is ambiguous for a cumulative
            # snapshot (which year's Q1?), so fall back to an exact
            # match rather than guessing.
            clauses.append("quarter = ?")
            params.append(quarter)
        elif month:
            clauses.append("month = ?")
            params.append(month)

        if country:
            clauses.append("country = ?")
            params.append(country)

        where = ""

        if clauses:
            where = " WHERE " + " AND ".join(clauses)

        query = f"""

        SELECT

            subclass,

            subclass2,

            account,

            subaccount,

            SUM(balance) AS balance

        FROM FinancialReportingMart

        {where}

        {"AND" if where else "WHERE"}

        report='Balance Sheet'

        GROUP BY

            subclass,
            subclass2,
            account,
            subaccount

        ORDER BY

            subclass,
            subclass2,
            account,
            subaccount

        """

        return self.conn.execute(
            query,
            params,
        ).fetchdf()

    # ==========================================================
    # KPI SUMMARY
    # ==========================================================

    def kpis(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        query = f"""

        SELECT

            COUNT(*) AS rows,

            COUNT(DISTINCT account_key) AS accounts,

            SUM(debit) AS debit,

            SUM(credit) AS credit,

            SUM(transactions) AS transactions

        FROM FinancialReportingMart

        {where}

        """

        return self.conn.execute(
            query,
            params,
        ).fetchdf()

    # ==========================================================
    # YEARS
    # ==========================================================

    def years(self):

        return self.conn.execute("""

            SELECT DISTINCT

                year

            FROM FinancialReportingMart

            ORDER BY year

        """).fetchdf()

    # ==========================================================
    # QUARTERS
    # ==========================================================

    def quarters(self):

        return self.conn.execute("""

            SELECT DISTINCT

                quarter

            FROM FinancialReportingMart

            ORDER BY quarter

        """).fetchdf()

    # ==========================================================
    # MONTHS
    # ==========================================================

    def months(self):

        return self.conn.execute("""

            SELECT DISTINCT

                month,
                month_number

            FROM FinancialReportingMart

            ORDER BY month_number

        """).fetchdf()

    # ==========================================================
    # COUNTRIES
    # ==========================================================

    def countries(self):

        return self.conn.execute("""

            SELECT DISTINCT

                country

            FROM FinancialReportingMart

            ORDER BY country

        """).fetchdf()

    # ==========================================================
    # CASH FLOW STATEMENT
    # ==========================================================

    def cash_flow(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        # -------------------------------------------------------
        # Flow line items: exact-period match (like Income
        # Statement) -- this period's operating/investing/
        # financing activity, not cumulative.
        # -------------------------------------------------------

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        flow_query = f"""

        SELECT

            COALESCE(SUM(profit_before_tax), 0)             AS profit_before_tax,
            COALESCE(SUM(depreciation_amortization), 0)      AS depreciation_amortization,
            COALESCE(SUM(non_operating_removed), 0)          AS non_operating_removed,
            COALESCE(SUM(interest_expense_addback), 0)       AS interest_expense_addback,
            COALESCE(SUM(receivables_change), 0)             AS receivables_change,
            COALESCE(SUM(inventory_change), 0)               AS inventory_change,
            COALESCE(SUM(payables_change), 0)                AS payables_change,
            COALESCE(SUM(interest_paid), 0)                  AS interest_paid,
            COALESCE(SUM(tax_paid), 0)                       AS tax_paid,
            COALESCE(SUM(purchase_equipment), 0)             AS purchase_equipment,
            COALESCE(SUM(proceeds_from_sale_of_asset), 0)    AS proceeds_from_sale_of_asset,
            COALESCE(SUM(investments_purchase), 0)           AS investments_purchase,
            COALESCE(SUM(interest_received), 0)              AS interest_received,
            COALESCE(SUM(dividends_received), 0)             AS dividends_received,
            COALESCE(SUM(exchange_gain_loss_cash), 0)        AS exchange_gain_loss_cash,
            COALESCE(SUM(share_capital_issued), 0)           AS share_capital_issued,
            COALESCE(SUM(new_loan_proceeds), 0)              AS new_loan_proceeds,
            COALESCE(SUM(dividends_paid_cash), 0)            AS dividends_paid_cash

        FROM CashFlowStatement

        {where}

        """

        flow = self.conn.execute(flow_query, params).fetchdf().iloc[0].to_dict()

        # -------------------------------------------------------
        # Opening / Closing cash: cumulative-to-date, same logic
        # as the Balance Sheet (a point-in-time snapshot, not a
        # period activity), reusing FinancialReportingMart's cash
        # accounts (10, 20).
        # -------------------------------------------------------

        def cumulative_cash_clause(upper_bound_exclusive):
            clauses = ["account IN ('Cash & Cash Equivalents')"]
            cum_params = []

            if year:
                if month:
                    cmp_op = "<" if upper_bound_exclusive else "<="
                    clauses.append(
                        f"""
                        (year < ? OR (year = ? AND month_number {cmp_op} (
                            SELECT MIN(month_number) FROM FinancialReportingMart
                            WHERE month = ?
                        )))
                        """
                    )
                    cum_params.extend([year, year, month])
                elif quarter:
                    cmp_op = "<" if upper_bound_exclusive else "<="
                    clauses.append(
                        f"""
                        (year < ? OR (year = ? AND
                            CAST(TRIM(REPLACE(quarter, 'Qtr', '')) AS INTEGER)
                            {cmp_op} CAST(TRIM(REPLACE(?, 'Qtr', '')) AS INTEGER)
                        ))
                        """
                    )
                    cum_params.extend([year, year, quarter])
                else:
                    cmp_op = "<" if upper_bound_exclusive else "<="
                    clauses.append(f"year {cmp_op} ?")
                    cum_params.append(year)

            if country:
                clauses.append("country = ?")
                cum_params.append(country)

            return " WHERE " + " AND ".join(clauses), cum_params

        # Opening cash: strictly before the selected year (or 0 if the
        # selected year is the first year of data / no year selected
        # means "all periods", so opening cash is 0).
        if year:
            open_where, open_params = cumulative_cash_clause(upper_bound_exclusive=True)
            opening_cash = self.conn.execute(
                f"SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart {open_where}",
                open_params,
            ).fetchone()[0]

            close_where, close_params = cumulative_cash_clause(upper_bound_exclusive=False)
            closing_cash = self.conn.execute(
                f"SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart {close_where}",
                close_params,
            ).fetchone()[0]
        else:
            opening_cash = 0
            fallback_clauses = ["account = 'Cash & Cash Equivalents'"]
            country_params = []

            # Quarter/month without a year is ambiguous for a true
            # cumulative snapshot (which year's Q1?), so fall back to
            # an exact match on whatever was given, same as the
            # Balance Sheet does -- rather than silently ignoring the
            # filter, which would understate/overstate the result.
            if quarter:
                fallback_clauses.append("quarter = ?")
                country_params.append(quarter)
            elif month:
                fallback_clauses.append("month = ?")
                country_params.append(month)

            if country:
                fallback_clauses.append("country = ?")
                country_params.append(country)

            country_clause = " WHERE " + " AND ".join(fallback_clauses)

            closing_cash = self.conn.execute(
                f"SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart {country_clause}",
                country_params,
            ).fetchone()[0]

        net_operating = (
            flow["profit_before_tax"]
            + flow["depreciation_amortization"]
            + flow["non_operating_removed"]
            + flow["interest_expense_addback"]
            + flow["receivables_change"]
            + flow["inventory_change"]
            + flow["payables_change"]
            + flow["interest_paid"]
            + flow["tax_paid"]
        )

        net_investing = (
            flow["purchase_equipment"]
            + flow["proceeds_from_sale_of_asset"]
            + flow["investments_purchase"]
            + flow["interest_received"]
            + flow["dividends_received"]
            + flow["exchange_gain_loss_cash"]
        )

        net_financing = (
            flow["share_capital_issued"]
            + flow["new_loan_proceeds"]
            + flow["dividends_paid_cash"]
        )

        net_change = net_operating + net_investing + net_financing

        return {
            **flow,
            "net_operating": net_operating,
            "net_investing": net_investing,
            "net_financing": net_financing,
            "net_change": net_change,
            "opening_cash": float(opening_cash),
            "closing_cash": float(closing_cash),
        }

    # ==========================================================
    # STATEMENT OF EQUITY
    # ==========================================================

    def statement_of_equity(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        # -------------------------------------------------------
        # Period movement: exact-period match (like Income
        # Statement / Cash Flow) -- this period's Net Income,
        # Dividends, and Share Issuance.
        # -------------------------------------------------------

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        flow_query = f"""

        SELECT

            COALESCE(SUM(net_income), 0)            AS net_income,
            COALESCE(SUM(dividends_for_period), 0)  AS dividends_for_period,
            COALESCE(SUM(share_issued), 0)           AS share_issued

        FROM StatementOfEquity

        {where}

        """

        flow = self.conn.execute(flow_query, params).fetchdf().iloc[0].to_dict()

        # -------------------------------------------------------
        # Opening / Closing equity: cumulative-to-date, same
        # cumulative logic as the Balance Sheet -- a point-in-time
        # snapshot, not a period activity. Uses FinancialReportingMart's
        # equity accounts (Share Capital, Share Premium, Retained
        # Earnings, Dividends paid).
        # -------------------------------------------------------

        def cumulative_equity_clause(upper_bound_exclusive):
            clauses = ["subclass = 'Owners Equity'"]
            cum_params = []

            if year:
                if month:
                    cmp_op = "<" if upper_bound_exclusive else "<="
                    clauses.append(
                        f"""
                        (year < ? OR (year = ? AND month_number {cmp_op} (
                            SELECT MIN(month_number) FROM FinancialReportingMart
                            WHERE month = ?
                        )))
                        """
                    )
                    cum_params.extend([year, year, month])
                elif quarter:
                    cmp_op = "<" if upper_bound_exclusive else "<="
                    clauses.append(
                        f"""
                        (year < ? OR (year = ? AND
                            CAST(TRIM(REPLACE(quarter, 'Qtr', '')) AS INTEGER)
                            {cmp_op} CAST(TRIM(REPLACE(?, 'Qtr', '')) AS INTEGER)
                        ))
                        """
                    )
                    cum_params.extend([year, year, quarter])
                else:
                    cmp_op = "<" if upper_bound_exclusive else "<="
                    clauses.append(f"year {cmp_op} ?")
                    cum_params.append(year)

            if country:
                clauses.append("country = ?")
                cum_params.append(country)

            return " WHERE " + " AND ".join(clauses), cum_params

        if year:
            open_where, open_params = cumulative_equity_clause(upper_bound_exclusive=True)
            opening_balance = -self.conn.execute(
                f"SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart {open_where}",
                open_params,
            ).fetchone()[0]

            close_where, close_params = cumulative_equity_clause(upper_bound_exclusive=False)
            closing_balance = -self.conn.execute(
                f"SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart {close_where}",
                close_params,
            ).fetchone()[0]
        else:
            opening_balance = 0
            fallback_clauses = ["subclass = 'Owners Equity'"]
            country_params = []

            if quarter:
                fallback_clauses.append("quarter = ?")
                country_params.append(quarter)
            elif month:
                fallback_clauses.append("month = ?")
                country_params.append(month)

            if country:
                fallback_clauses.append("country = ?")
                country_params.append(country)

            country_clause = " WHERE " + " AND ".join(fallback_clauses)

            closing_balance = -self.conn.execute(
                f"SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart {country_clause}",
                country_params,
            ).fetchone()[0]

        implied_closing = (
            opening_balance
            + flow["net_income"]
            - flow["dividends_for_period"]
            + flow["share_issued"]
        )

        return {
            **flow,
            "opening_balance": float(opening_balance),
            "closing_balance": float(closing_balance),
            "implied_closing": float(implied_closing),
        }

    # ==========================================================
    # FINANCIAL RATIOS
    # ==========================================================

    def _ratios_cumulative_where(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):
        # Balance Sheet figures (Assets/Liabilities/Equity) are
        # point-in-time balances, so they need cumulative-to-date
        # filtering -- same validated pattern used in balance_sheet(),
        # cash_flow(), and statement_of_equity().

        clauses = []
        params = []

        if year:
            if month:
                clauses.append(
                    """
                    (year < ? OR (year = ? AND month_number <= (
                        SELECT MIN(month_number) FROM FinancialReportingMart
                        WHERE month = ?
                    )))
                    """
                )
                params.extend([year, year, month])
            elif quarter:
                clauses.append(
                    """
                    (year < ? OR (year = ? AND
                        CAST(TRIM(REPLACE(quarter, 'Qtr', '')) AS INTEGER)
                        <= CAST(TRIM(REPLACE(?, 'Qtr', '')) AS INTEGER)
                    ))
                    """
                )
                params.extend([year, year, quarter])
            else:
                clauses.append("year <= ?")
                params.append(year)
        elif quarter:
            clauses.append("quarter = ?")
            params.append(quarter)
        elif month:
            clauses.append("month = ?")
            params.append(month)

        if country:
            clauses.append("country = ?")
            params.append(country)

        where = ""

        if clauses:
            where = " WHERE " + " AND ".join(clauses)

        return where, params

    def financial_ratios(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        # -------------------------------------------------------
        # Balance Sheet figures: cumulative-to-date (point-in-time)
        # -------------------------------------------------------

        cum_where, cum_params = self._ratios_cumulative_where(
            year,
            quarter,
            month,
            country,
        )

        bs_row = self.conn.execute(
            f"""
            SELECT

                SUM(CASE WHEN account='Cash & Cash Equivalents' THEN balance ELSE 0 END) AS cash,
                SUM(CASE WHEN account='Receivables' THEN balance ELSE 0 END) AS receivables,
                SUM(CASE WHEN account='Inventory' THEN balance ELSE 0 END) AS inventory,
                SUM(CASE WHEN subclass2='Current Assets' THEN balance ELSE 0 END) AS current_assets,
                SUM(CASE WHEN subclass2='Non-Current Assets' THEN balance ELSE 0 END) AS non_current_assets,
                -SUM(CASE WHEN subclass2='Current Liabilities' THEN balance ELSE 0 END) AS current_liabilities,
                -SUM(CASE WHEN subclass2='Long Term Liabilities' THEN balance ELSE 0 END) AS long_term_liabilities,
                -SUM(CASE WHEN subclass2='Share Capital' THEN balance ELSE 0 END) AS share_capital,
                -SUM(CASE WHEN subclass2='Retained Earnings' AND account<>'Dividends paid'
                    THEN balance ELSE 0 END) AS retained_earnings,
                SUM(CASE WHEN account='Dividends paid' THEN balance ELSE 0 END) AS dividends_paid

            FROM FinancialReportingMart

            {cum_where}

            {"AND" if cum_where else "WHERE"} report='Balance Sheet'

            """,
            cum_params,
        ).fetchone()

        (
            cash,
            receivables,
            inventory,
            current_assets,
            non_current_assets,
            current_liabilities,
            long_term_liabilities,
            share_capital,
            retained_earnings,
            dividends_paid,
        ) = [float(v or 0) for v in bs_row]

        total_assets = current_assets + non_current_assets
        total_liabilities = current_liabilities + long_term_liabilities
        total_equity = share_capital + retained_earnings - dividends_paid

        # -------------------------------------------------------
        # P&L figures: exact-period match (period activity, same
        # as Income Statement)
        # -------------------------------------------------------

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        pl_row = self.conn.execute(
            f"""
            SELECT

                -SUM(CASE WHEN account='Sales' THEN balance ELSE 0 END) AS gross_sales,
                SUM(CASE WHEN account='Sales Return' THEN balance ELSE 0 END) AS sales_returns,
                SUM(CASE WHEN account='Cost of Sales' THEN balance ELSE 0 END) AS cost_of_sales,
                SUM(CASE WHEN subclass2 IN ('Sales & Distribution','Marketing','Administration')
                    THEN balance ELSE 0 END) AS operating_expenses,
                SUM(CASE WHEN subclass2 IN ('Depreciation','Amortization')
                    THEN balance ELSE 0 END) AS depreciation_amortization,
                -SUM(CASE WHEN subclass2 IN ('Interest Income','Dividend Income',
                    'Gain/Loss on Sales of Asset','Exchange Loss/Gain')
                    THEN balance ELSE 0 END) AS non_operating_income,
                SUM(CASE WHEN subclass2='Interest Expense' THEN balance ELSE 0 END) AS interest_expense,
                SUM(CASE WHEN subclass2='Taxation' THEN balance ELSE 0 END) AS taxation

            FROM FinancialReportingMart

            {where}

            {"AND" if where else "WHERE"} report='Profit and Loss'

            """,
            params,
        ).fetchone()

        (
            gross_sales,
            sales_returns,
            cost_of_sales,
            operating_expenses,
            depreciation_amortization,
            non_operating_income,
            interest_expense,
            taxation,
        ) = [float(v or 0) for v in pl_row]

        net_revenue = gross_sales - sales_returns
        gross_profit = net_revenue - cost_of_sales
        operating_profit = gross_profit - operating_expenses - depreciation_amortization
        profit_before_tax = operating_profit + non_operating_income - interest_expense
        net_profit = profit_before_tax - taxation

        # -------------------------------------------------------
        # Ratios (None when the denominator is zero, rather than
        # dividing by zero or showing a misleading 0%/0x)
        # -------------------------------------------------------

        def safe_div(numerator, denominator):
            if not denominator:
                return None
            return numerator / denominator

        return {

            "inputs": {
                "cash": cash,
                "receivables": receivables,
                "inventory": inventory,
                "current_assets": current_assets,
                "non_current_assets": non_current_assets,
                "total_assets": total_assets,
                "current_liabilities": current_liabilities,
                "long_term_liabilities": long_term_liabilities,
                "total_liabilities": total_liabilities,
                "total_equity": total_equity,
                "net_revenue": net_revenue,
                "gross_profit": gross_profit,
                "operating_profit": operating_profit,
                "net_profit": net_profit,
                "cost_of_sales": cost_of_sales,
            },

            "liquidity": {
                "current_ratio": safe_div(current_assets, current_liabilities),
                "quick_ratio": safe_div(current_assets - inventory, current_liabilities),
                "cash_ratio": safe_div(cash, current_liabilities),
            },

            "profitability": {
                "gross_margin": safe_div(gross_profit, net_revenue),
                "operating_margin": safe_div(operating_profit, net_revenue),
                "net_margin": safe_div(net_profit, net_revenue),
                "return_on_assets": safe_div(net_profit, total_assets),
                "return_on_equity": safe_div(net_profit, total_equity),
            },

            "leverage": {
                "debt_to_equity": safe_div(total_liabilities, total_equity),
                "debt_ratio": safe_div(total_liabilities, total_assets),
                "equity_ratio": safe_div(total_equity, total_assets),
            },

            "efficiency": {
                "asset_turnover": safe_div(net_revenue, total_assets),
                "inventory_turnover": safe_div(cost_of_sales, inventory),
                "receivables_turnover": safe_div(net_revenue, receivables),
            },

        }

    # ==========================================================
    # REPORTING PERIOD
    # ==========================================================

    def latest_reporting_period(self):

        return self.conn.execute("""

            SELECT

                year,
                quarter,
                month

            FROM FinancialReportingMart

            ORDER BY

                year DESC,
                month_number DESC

            LIMIT 1

        """).fetchone()

    # ==========================================================
    # CLOSE CONNECTION
    # ==========================================================

    def close(self):
        self.conn.close()