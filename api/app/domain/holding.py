from uuid import UUID

from app.dependencies import UserDb
from app.util.response import db_error_response, error_response, success_response
from shared.database import DatabaseError


def holdings_get_one(db: UserDb, holding_id: UUID):
    try:
        row = db.holdings.get(id=holding_id)
    except DatabaseError as e:
        raise db_error_response(e)
    if row is None:
        raise error_response(status_code=404, message="Found no holding with this id")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))