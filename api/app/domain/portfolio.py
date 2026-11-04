from uuid import UUID

from app.dependencies import UserDb
from app.util.response import success_response, error_response, db_error_response
from shared.database import DatabaseError
from shared.database.models import PortfolioInsert


def portfolio_get_one(db: UserDb, portfolio_id: UUID):
    try:
        row = db.portfolios.get(id=portfolio_id)
    except DatabaseError as e:
        raise db_error_response(e)
    if row is None:
        raise error_response(status_code=404, message="Found no portfolio with this id")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))


def portfolio_post_one(db: UserDb, payload: PortfolioInsert):
    try:
        row = db.portfolios.insert(payload)[0]
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=row.model_dump(by_alias=True, mode="json"))
