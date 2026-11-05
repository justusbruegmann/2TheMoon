from datetime import UTC, datetime

from app.dependencies import UserDb
from shared.database.models import Season



def get_current_season(db: UserDb) -> Season | None:
    now = datetime.now(UTC).isoformat()
    query = (
        db.seasons.select_query()
        .or_(f"ends_at.is.null,ends_at.gt.{now}")
        .limit(1)
    )
    seasons = db.seasons.run(query)
    return seasons[0] if seasons else None
