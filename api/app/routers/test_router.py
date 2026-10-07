from fastapi import APIRouter, HTTPException

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
    except DatabaseError as exc:
        raise HTTPException(status_code=503, detail="Database request failed") from exc
    return {
        "success": True,
        "data": res.data
    }
