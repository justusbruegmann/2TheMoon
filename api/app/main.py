from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config.exception_handlers import exception_handler
from shared.database.models.api_response import ApiErrorResponse
from .config.fastapi import register_routers



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

register_routers(app)

####################################################
# Health Check
####################################################
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "healthy"
    }
