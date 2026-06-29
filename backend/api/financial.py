from fastapi import APIRouter

from backend.services.financial_service import FinancialService

router = APIRouter(
    prefix="/api/financial",
    tags=["Financial Reporting"],
)


# ==========================================================
# Trial Balance
# ==========================================================

@router.get("/trial-balance")
def trial_balance(
    year: int | None = None,
    quarter: str | None = None,
    month: str | None = None,
    country: str | None = None,
):

    service = FinancialService()

    try:

        df = service.trial_balance(
            year,
            quarter,
            month,
            country,
        )

        return df.to_dict(orient="records")

    finally:

        service.close()


# ==========================================================
# Income Statement
# ==========================================================

@router.get("/income-statement")
def income_statement(
    year: int | None = None,
    quarter: str | None = None,
    month: str | None = None,
    country: str | None = None,
):

    service = FinancialService()

    try:

        df = service.income_statement(
            year,
            quarter,
            month,
            country,
        )

        return df.to_dict(orient="records")

    finally:

        service.close()


# ==========================================================
# Balance Sheet
# ==========================================================

@router.get("/balance-sheet")
def balance_sheet(
    year: int | None = None,
    quarter: str | None = None,
    month: str | None = None,
    country: str | None = None,
):

    service = FinancialService()

    try:

        df = service.balance_sheet(
            year,
            quarter,
            month,
            country,
        )

        return df.to_dict(orient="records")

    finally:

        service.close()


# ==========================================================
# KPI SUMMARY
# ==========================================================

@router.get("/kpis")
def kpis(
    year: int | None = None,
    quarter: str | None = None,
    month: str | None = None,
    country: str | None = None,
):

    service = FinancialService()

    try:

        df = service.kpis(
            year,
            quarter,
            month,
            country,
        )

        return df.to_dict(orient="records")[0]

    finally:

        service.close()


# ==========================================================
# Filters
# ==========================================================

@router.get("/filters")
def filters():

    service = FinancialService()

    try:

        return {

            "years": service.years().to_dict(orient="records"),

            "quarters": service.quarters().to_dict(orient="records"),

            "months": service.months().to_dict(orient="records"),

            "countries": service.countries().to_dict(orient="records"),

        }

    finally:

        service.close()


# ==========================================================
# Cash Flow
# ==========================================================

@router.get("/cash-flow")
def cash_flow():

    return []


# ==========================================================
# Statement of Equity
# ==========================================================

@router.get("/statement-of-equity")
def statement_of_equity():

    return []