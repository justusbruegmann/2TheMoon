from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies import UserDb, gameserver_route_protection
from app.util.response import success_response, error_response, db_error_response
from shared.database import DatabaseError
from shared.database.models import PriceHistory, PriceHistoryInsert
from shared.database.models.api_response import ApiResponse

###########################################################################
# The price_history table stores 5-minute summaries of the gameserver's real-time simulation data.
# It is in the form {start, end, low, high} which is necessary to build the candle chart in the frontend.
###########################################################################

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[PriceHistory]],
    description="Returns a list of all history items (5-minute candles)"
)
def price_history_get_all(db: UserDb):
    try:
        rows = db.price_history.find()
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])


@router.get(
    path="/{price_history_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PriceHistory],
    description="Returns the price_history with the specified id"
)
def price_history_get_one(price_history_id: UUID, db: UserDb):
    try:
        row = db.price_history.get(id=price_history_id)
    except DatabaseError as e:
        raise db_error_response(e)
    if row is None:
        raise error_response(status_code=404, message="Found no price_history with this id")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))



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
