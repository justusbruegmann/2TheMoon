from datetime import datetime, timedelta

from app.config.dependencies import UserDb
from app.util.response import DomainError
from app.util.time_range import validate_time_range

# We interpret the history entry's 'recorded_at' field as the end of the candle.
# If start/end times overlap with a candle's covered (hardcoded) 5-minute span, we need to retrieve that one as well.
CANDLE_WIDTH = timedelta(minutes=5)


def price_history_get_all(
        db: UserDb,
        start: datetime | None = None,
        end: datetime | None = None,
        ticker: str | None = None
):
    validate_time_range(start, end)

    filters = {}
    if start:
        filters["gt"] = {"recorded_at": start}
    if end:
        filters["lt"] = {"recorded_at": end + CANDLE_WIDTH}

    if ticker:
        asset = db.assets.find(ticker=ticker, limit=1)
        if not asset:
            raise DomainError(status_code=404, message="Found no asset with this ticker")
        filters["asset_id"] = asset[0].id

    return db.price_history.find(**filters)

############################
# Protected POST – only the gameserver is allowed to write entries into the table
#
# REMARK AFTER REVIEW
# The gameserver will communicate with the database through the shared/ functions directly instead of using the API.
# This code will be inactive, but in case we need it again later, I'll keep it around.
############################

# def price_history_post_one(db: UserDb, payload: PriceHistoryInsert):
#     return db.price_history.insert(payload)[0]
