from datetime import datetime, timedelta

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.domain.price_history import price_history_get_all
from shared.database.models import PriceHistory
from shared.database.models.api_response import ApiResponse

#####################
# Information
#
# The price_history table stores 5-minute summaries of the gameserver's real-time simulation data.
# It is in the form {open, close, low, high} which is necessary to build the candle chart in the frontend.
#
#####################
# RLS
#
# - GET /price_history      Anyone may see all price histories
#####################

router = APIRouter()

# We interpret the history entry's 'recorded_at' field as the end of the candle.
# If start/end times overlap with a candle's covered (hardcoded) 5-minute span, we need to retrieve that one as well.
CANDLE_WIDTH = timedelta(minutes=5)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[PriceHistory]],
    description="Returns history items (5-minute candles) overlapping the optional [start, end] window, "
                "optionally restricted to a single asset by ticker"
)
def handle_get_price_history(
        db: UserDb,
        start: datetime | None = None,
        end: datetime | None = None,
        ticker: str | None = None
):
    price_history_get_all(db, start, end, ticker)

############################
# Protected POST – only the gameserver is allowed to write entries into the table
#
# REMARK AFTER REVIEW
# The gameserver will communicate with the database through the shared/ functions directly instead of using the API.
# This code will be inactive, but in case we need it again later, I'll keep it around.
############################

# @router.post(
#     dependencies=[Depends(gameserver_route_protection)],
#     path="/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ApiResponse[PriceHistory],
#     description="Creates a new history entry"
# )
# def handle_post_price_history(db: UserDb, payload: PriceHistoryInsert):
#     price_history_post_one(db, payload)
