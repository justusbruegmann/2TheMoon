from datetime import datetime

from app.util.response import DomainError


############################
# Sanity checks for a start/end time range, (mainly) for filterable GET endpoints
############################
def validate_time_range(start: datetime | None, end: datetime | None) -> None:
    if start and end and start > end:
        raise DomainError(status_code=400, message="Requested start time cannot be later than end time")
    if start and start > datetime.now(start.tzinfo):
        raise DomainError(status_code=400, message="Requested start time cannot be in the future")
