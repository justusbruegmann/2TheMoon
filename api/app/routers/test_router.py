from fastapi import APIRouter, HTTPException

from shared.database import DatabaseError, db



router = APIRouter()


@router.get("/", tags=["PLACEHOLDER"])
async def get_test():
    return [{"a": "b"}, {"c": "d"}]


@router.get("/database", tags=["PLACEHOLDER"])
async def get_database_test():
    try:
        res = db.test_request("hallo")
    except DatabaseError as exc:
        raise HTTPException(status_code=503, detail="Database request failed") from exc
    return {"database response": res}
