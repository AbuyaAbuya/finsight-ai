from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.budget_service import BudgetService

router = APIRouter(
    prefix="/api/budget",
    tags=["Budget"],
)


class BudgetLineUpdate(BaseModel):
    year: int
    month: str
    country: str | None = None
    account: str
    budget_amount: float


class BudgetGenerateRequest(BaseModel):
    year: int
    country: str | None = None
    growth_rate: float = 0.0


# ==========================================================
# Get Budget vs Actual
# ==========================================================

@router.get("")
def get_budget(
    year: int,
    country: str | None = None,
):

    service = BudgetService()

    try:

        return service.get_budget_vs_actual(
            year,
            country,
        )

    finally:

        service.close()


# ==========================================================
# Regenerate Baseline
# ==========================================================

@router.post("/generate")
def generate_baseline(request: BudgetGenerateRequest):

    service = BudgetService()

    try:

        rows = service.generate_baseline(
            request.year,
            request.country,
            request.growth_rate,
        )

        return {"rows_generated": rows}

    finally:

        service.close()


# ==========================================================
# Update a Single Budget Line
# ==========================================================

@router.put("")
def update_budget_line(update: BudgetLineUpdate):

    service = BudgetService()

    try:

        service.update_budget_line(
            update.year,
            update.month,
            update.country,
            update.account,
            update.budget_amount,
        )

        return {"status": "ok"}

    finally:

        service.close()
