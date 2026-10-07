from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import Depends, FastAPI, HTTPException

from .dependencies import check_header_token
from .exception_handlers import exception_handler
from .routers import test_router


####################################################
# App
####################################################
app = FastAPI()
app.add_exception_handler(HTTPException, exception_handler)


####################################################
# Routers
####################################################
app.include_router(
    test_router.router,
    prefix="/test",
    tags=["test-tag"],
    dependencies=[Depends(check_header_token)],
    responses={418: {"description": "I'm a teapot"}},
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


# ToDo: Unify response structure: {success: bool, message: str (Description of result), data: Any}