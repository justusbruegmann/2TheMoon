from fastapi import APIRouter

from app.dependencies import UserDbDep
from app.util.response import success_response, error_response
from shared.database import DatabaseError
from shared.database.models.test import TestInsert



router = APIRouter()


@router.get("/database/")
def test_get_all(db: UserDbDep):
    try:
        rows = db.test.find()
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])


@router.get("/database/{row_id}")
def test_get_one(row_id: int, db: UserDbDep):
    try:
        row = db.test.get(id=row_id)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    if row is None:
        raise error_response(status_code=404, message="Entry not found")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))


@router.post("/database/", status_code=201)
def test_post(payload: TestInsert, db: UserDbDep):
    try:
        row = db.test.insert(payload)[0]
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))


@router.patch("/database/{row_id}")
def test_patch(row_id: int, payload: TestInsert, db: UserDbDep):
    if not payload.model_fields_set:
        raise error_response(status_code=400, message="No fields to update")
    try:
        rows = db.test.update(payload.model_dump(exclude_unset=True), id=row_id)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    if not rows:
        raise error_response(status_code=404, message="Entry not found")
    return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))


@router.delete("/database/{row_id}")
def test_delete(row_id: int, db: UserDbDep):
    try:
        rows = db.test.delete(id=row_id)
    except DatabaseError:
        raise error_response(status_code=503, message="Database request failed")
    if not rows:
        raise error_response(status_code=404, message="Entry not found")
    return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
