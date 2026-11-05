from uuid import UUID

from fastapi import APIRouter, status

from app.config.dependencies import UserDb
from app.domain.trade import trades_get_all, trades_get_one, trades_buy, trades_sell
from app.util.response import api_response
from shared.database.models import Trade
from shared.database.models.api_response import ApiResponse
from shared.database.models.trade import TradeOffer

# ToDo

#####################
# RLS
#
# - GET /trades         Anyone may see all trades
# - GET /trades/:id     Anyone may see one trade's details
#####################

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[Trade]],
    description="Returns a list of all available trades"
)
@api_response
def handle_get_all_trades(db: UserDb):
    return trades_get_all(db)


@router.get(
    path="/{trade_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Trade],
    description="Returns the trade with the specified id"
)
@api_response
def handle_get_one_trade(db: UserDb, trade_id: UUID):
    return trades_get_one(db, trade_id)


@router.post(
    path="/buy",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[Trade],
    description="Post a buy offer"
)
@api_response
def handle_buy(db: UserDb, payload: TradeOffer):
    return trades_buy(db, payload)


@router.post(
    path="/sell",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[Trade],
    description="Post a sell offer"
)
@api_response
def handle_sell(db: UserDb, payload: TradeOffer):
    return trades_sell(db, payload)
