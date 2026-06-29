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

            SUM(debit) AS debit,

            SUM(credit) AS credit

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

            SUM(debit) <> 0
            OR
            SUM(credit) <> 0

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