from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.domain.portfolio import portfolio_post_one, portfolio_get_one
from app.util.response import api_response
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
@api_response
def handle_get_one_portfolio(db: UserDb, user_id: UUID, season_id: UUID | None = None):
    return portfolio_get_one(db, user_id, season_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[Portfolio],
    description="Creates a new type of portfolio"
)
@api_response
def handle_post_one_portfolio(db: UserDb, payload: PortfolioInsert):
    return portfolio_post_one(db, payload)
