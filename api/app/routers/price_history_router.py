from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status

from app.dependencies import UserDb, gameserver_route_protection
from app.util.response import success_response, error_response, db_error_response
from shared.database import DatabaseError
from shared.database.models import PriceHistory, PriceHistoryInsert
from shared.database.models.api_response import ApiResponse



###########################################################################
# The price_history table stores 5-minute summaries of the gameserver's real-time simulation data.
# It is in the form {open, close, low, high} which is necessary to build the candle chart in the frontend.
###########################################################################

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
def price_history_get_all(
        db: UserDb, start: datetime | None = None, end: datetime | None = None, ticker: str | None = None
):
    filters = {}
    if start:
        filters["gt"] = {"recorded_at": start}
    if end:
        filters["lt"] = {"recorded_at": end + CANDLE_WIDTH}

    try:
        if ticker:
            asset = db.assets.find(ticker=ticker, limit=1)
            if not asset:
                raise error_response(status_code=404, message="Found no asset with this ticker")
            filters["asset_id"] = asset[0].id

        rows = db.price_history.find(
            **filters
        )
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])



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
# def price_history_post_one(payload: PriceHistoryInsert, db: UserDb):
#     try:
#         row = db.price_history.insert(payload)[0]
#     except DatabaseError as e:
#         raise db_error_response(e)
#     return success_response(data=row.model_dump(by_alias=True, mode="json"))
