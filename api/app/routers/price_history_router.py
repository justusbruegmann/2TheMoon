from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status

from app.dependencies import UserDb, gameserver_route_protection
from app.util.response import success_response, db_error_response
from shared.database import DatabaseError
from shared.database.models import PriceHistory, PriceHistoryInsert
from shared.database.models.api_response import ApiResponse

###########################################################################
# The price_history table stores 5-minute summaries of the gameserver's real-time simulation data.
# It is in the form {start, end, low, high} which is necessary to build the candle chart in the frontend.
###########################################################################

router = APIRouter()

# shortcut: candle width is hardcoded instead of read from the row (the table only stores recorded_at,
# the candle's end); upgrade if candles ever get a variable/configurable width.
CANDLE_WIDTH = timedelta(minutes=5)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[PriceHistory]],
    description="Returns history items (5-minute candles) overlapping the optional [start, end] window"
)
def price_history_get_all(db: UserDb, start: datetime | None = None, end: datetime | None = None):
    try:
        rows = db.price_history.find(
            gt={"recorded_at": start} if start else None,
            lt={"recorded_at": end + CANDLE_WIDTH} if end else None,
        )
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])



############################
# Protected POST – only the gameserver is allowed to write entries into the table
############################

@router.post(
    dependencies=[Depends(gameserver_route_protection)],
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[PriceHistory],
    description="Creates a new history entry"
)
def price_history_post_one(payload: PriceHistoryInsert, db: UserDb):
    try:
        row = db.price_history.insert(payload)[0]
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=row.model_dump(by_alias=True, mode="json"))
