from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from shared.database.models.api_response import ApiErrorResponse
from .dependencies import get_user_db
from .exception_handlers import exception_handler
from .routers import asset_router, price_history_router, portfolio_router



load_dotenv(Path(__file__).resolve().parent.parent / ".env")

####################################################
# App
####################################################
app = FastAPI(
    responses={
        400: {"model": ApiErrorResponse},
        404: {"model": ApiErrorResponse},
        422: {"model": ApiErrorResponse},
        500: {"model": ApiErrorResponse},
    }
)

# Exception Handler
app.add_exception_handler(HTTPException, exception_handler)

# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####################################################
# Routers
####################################################

app.include_router(
    asset_router.router,
    prefix="/assets",
    tags=["Asset"],
    dependencies=[Depends(get_user_db)],
)

app.include_router(
    price_history_router.router,
    prefix="/price_history",
    tags=["Pricce History"],
    dependencies=[Depends(get_user_db)],
)

app.include_router(
    portfolio_router.router,
    prefix="/portfolios",
    tags=["Portfolio"],
    dependencies=[Depends(get_user_db)],
)

####################################################
# Health Check
####################################################
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "healthy"
    }
