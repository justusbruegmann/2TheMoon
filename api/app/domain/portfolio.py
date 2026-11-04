from uuid import UUID

from app.dependencies import UserDb
from app.util.response import DomainError
from shared.database.models import PortfolioInsert


def portfolio_get_one(db: UserDb, portfolio_id: UUID):
    portfolio = db.portfolios.get(id=portfolio_id)
    if portfolio is None:
        raise DomainError(status_code=404, message="Found no portfolio with this id")
    return portfolio


def portfolio_post_one(db: UserDb, payload: PortfolioInsert):
    return db.portfolios.insert(payload)[0]
