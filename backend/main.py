from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.dashboard import router as dashboard_router
from backend.api.financial import router as financial_router
from backend.api.budget import router as budget_router
from backend.api.variance import router as variance_router
from backend.api.forecast import router as forecast_router

app = FastAPI(
    title="FinSight AI API",
    version="1.0.0",
    description="Enterprise FP&A Analytics API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://finsight-ai-ebon-tau.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(financial_router)
app.include_router(budget_router)
app.include_router(variance_router)
app.include_router(forecast_router)


@app.get("/")
def root():
    return {
        "application": "FinSight AI",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }