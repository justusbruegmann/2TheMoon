from uuid import UUID

from app.config.dependencies import UserDb
from app.domain.season import get_current_season
from app.util.response import DomainError
from shared.database.models import Portfolio, PortfolioInsertInternalPayload


def portfolio_get_one(db: UserDb, user_id: UUID, season_id: UUID | None) -> Portfolio:
    if season_id is None:
        current_season = get_current_season(db)
        if current_season is None:
            raise DomainError(404, "No active season")
        season_id = current_season.id

    portfolio = db.portfolios.get(user_id=user_id, season_id=season_id)
    if portfolio is None:
        raise DomainError(status_code=404, message=f"Found no portfolio for user {user_id} in season {season_id}")
    return portfolio


def portfolio_post_one(db: UserDb, user_id: UUID) -> Portfolio:
    current_season = get_current_season(db)
    if current_season is None:
        raise DomainError(404, "No active season")

    # There is a constraint in the database that (user_id, season_id) must be unique.
    if db.portfolios.get(user_id=user_id, season_id=current_season.id) is not None:
        raise DomainError(
            status_code=400,
            message=f"Portfolio for user {user_id} already exists in the current season"
        )

    return db.portfolios.insert(PortfolioInsertInternalPayload(
        user_id=user_id,
        season_id=current_season.id,
        cash_balance=current_season.starting_balance
    ))[0]
