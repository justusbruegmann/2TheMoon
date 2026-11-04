from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.domain.portfolio import portfolio_get_one, portfolio_post_one
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
    path="/{portfolio_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Portfolio],
    description="Returns the portfolio with the specified id"
)
def handle_get_one_portfolio(db: UserDb, portfolio_id: UUID):
    portfolio_get_one(db, portfolio_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[Portfolio],
    description="Creates a new type of portfolio"
)
def handle_post_one_portfolio(db: UserDb, payload: PortfolioInsert):
    portfolio_post_one(db, payload)
