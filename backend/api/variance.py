from fastapi import APIRouter

from backend.services.variance_service import VarianceAnalysisService

router = APIRouter(
    prefix="/api/variance",
    tags=["Variance Analysis"],
)


@router.get("")
def get_variance_analysis(
    year: int,
    country: str | None = None,
):

    service = VarianceAnalysisService()

    try:

        return service.get_variance_analysis(
            year,
            country,
        )

    finally:

        service.close()
