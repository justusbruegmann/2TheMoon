from fastapi import APIRouter

from shared.database import db



router = APIRouter()


@router.get("/", tags=["PLACEHOLDER"])
async def get_test():
    return [{"a": "b"}, {"c": "d"}]


@router.get("/database", tags=["PLACEHOLDER"])
async def get_database_test():
    res = db.test_request("hallo")
    return {"database response": res}
