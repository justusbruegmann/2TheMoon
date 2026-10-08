from fastapi import APIRouter

from app.util.response import success_response, error_response
from shared.database import DatabaseError, db
from shared.database.models.fastapi.schema_public_latest import TestingTableInsert, TestingTableUpdate



router = APIRouter()


@router.get("/database/", tags=["API Test"])
def test_get_all():
    try:
        rows = db.test_select_all()
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])


@router.get("/database/{id}", tags=["API Test"])
def test_get_one(element_id: int):
    try:
        row = db.test_select(element_id)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    if row is None:
        raise error_response(status_code=404, message="Entry not found")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))


@router.post("/database/", tags=["API Test"], status_code=201)
def test_post(payload: TestingTableInsert):
    try:
        row = db.test_insert(payload)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))


@router.patch("/database/{id}", tags=["API Test"])
def test_patch(element_id: int, payload: TestingTableUpdate):
    if not payload.model_fields_set:
        raise error_response(status_code=400, message="No fields to update")
    try:
        rows = db.test_update(element_id, payload)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    if not rows:
        raise error_response(status_code=404, message="Entry not found")
    return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))


@router.delete("/database/{id}", tags=["API Test"])
def test_delete(element_id: int):
    try:
        rows = db.test_delete(element_id)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    if not rows:
        raise error_response(status_code=404, message="Entry not found")
    return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
