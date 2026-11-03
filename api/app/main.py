from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends

from shared.database.models.api_response import ApiErrorResponse
from .dependencies import get_user_db
from .exception_handlers import exception_handler
from .routers import asset_router, price_history_router



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
app.add_exception_handler(HTTPException, exception_handler)

####################################################
# Routers
####################################################

app.include_router(
    asset_router.router,
    prefix="/assets",
    tags=["Assets"],
    dependencies=[Depends(get_user_db)],
)

app.include_router(
    price_history_router.router,
    prefix="/price_history",
    tags=["Pricce History"],
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
