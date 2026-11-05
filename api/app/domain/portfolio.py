from uuid import UUID

from app.config.dependencies import UserDb
from app.domain.season import get_current_season
from app.util.response import DomainError
from shared.database.models import PortfolioInsert


def portfolio_get_one(db: UserDb, user_id: UUID, season_id: UUID | None):
    if season_id is None:
        current_season = get_current_season(db)
        if current_season is None:
            raise DomainError(404, "No active season")
        season_id = current_season.id

    portfolio = db.portfolios.get(user_id=user_id, season_id=season_id)
    if portfolio is None:
        raise DomainError(status_code=404, message=f"Found no portfolio for user {user_id} in season {season_id}")
    return portfolio



def portfolio_post_one(db: UserDb, payload: PortfolioInsert):
    return db.portfolios.insert(payload)[0]
