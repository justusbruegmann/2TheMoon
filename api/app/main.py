from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_user_db
from .exception_handlers import exception_handler
from .routers import asset_router



load_dotenv(Path(__file__).resolve().parent.parent / ".env")

####################################################
# App
####################################################
app = FastAPI()

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
