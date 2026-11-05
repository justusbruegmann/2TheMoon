from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.domain.season import get_current_season
from app.util.response import success_response, error_response, db_error_response
from shared.database import DatabaseError
from shared.database.models import Portfolio, PortfolioInsert
from shared.database.models.api_response import ApiResponse



#####################
# Documentation for RLS
#
# /portfolios needs the following endpoints:
# - GET /portfolios/:id     RLS needs to protect access to only allow a user to request their own profile
# - POST /portfolios/:id    RLS needs to restrict a user to create only one portfolio per active season
#####################

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Portfolio],
    description="Returns the portfolio for the given user and season. If no season_id is set, returns the portfolio for the current season."
)
def portfolios_get_one(user_id: UUID, db: UserDb, season_id: UUID | None = None):
    try:
        if season_id is None:
            current_season = get_current_season(db)
            season_id = current_season.id if current_season else None
        row = db.portfolios.get(user_id=user_id, season_id=season_id)
    except DatabaseError as e:
        raise db_error_response(e)
    if row is None:
        raise error_response(status_code=404, message="Found no portfolio with this id")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))



@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[Portfolio],
    description="Creates a new type of portfolio"
)
def portfolios_post_one(payload: PortfolioInsert, db: UserDb):
    try:
        row = db.portfolios.insert(payload)[0]
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=row.model_dump(by_alias=True, mode="json"))
