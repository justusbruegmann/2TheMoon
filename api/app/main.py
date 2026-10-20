from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI, HTTPException

from .exception_handlers import exception_handler


####################################################
# App
####################################################
app = FastAPI()
app.add_exception_handler(HTTPException, exception_handler)


####################################################
# Routers
####################################################


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