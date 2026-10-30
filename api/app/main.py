from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends

from .dependencies import get_user_db
from .exception_handlers import exception_handler
from .routers import asset_router

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

####################################################
# App
####################################################
app = FastAPI()
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


####################################################
# Health Check
####################################################
@app.get("/")
async def root():
    return {
            "success": True,
            "message": "healthy"
    }
