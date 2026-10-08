from fastapi import APIRouter, HTTPException

from app.util.response import success_response, error_response
from shared.database import DatabaseError, db



router = APIRouter()


@router.get("/", tags=["API Test"])
async def get_test():
    return {
        "success": True,
        "message": "Endpoint is reachable"
    }


@router.get("/database", tags=["API Test"])
async def get_database_test():
    try:
        res = db.test_request(1)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    return success_response(data=res.data)