from fastapi import APIRouter

router = APIRouter()


@router.get("/test/", tags=["PLACEHOLDER"])
async def get_test():
    return [{"a": "b"}, {"c": "d"}]


@router.get("/test/really", tags=["PLACEHOLDER"])
async def get_test_really():
    return {"here": "you go", "mr": "green"}
