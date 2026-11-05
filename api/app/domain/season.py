from datetime import UTC, datetime

from app.dependencies import UserDb
from shared.database.models import Season


# ToDo: Introduce an internal db independent of user requests and login that can be used for internal API calls to these domain functions
def get_current_season(db: UserDb) -> Season | None:
    table = db.seasons
    now = datetime.now(UTC).isoformat()

    query = (
        table.client.table(table.name)
        .select(table.columns)
        .or_(f"ends_at.is.null,ends_at.gt.{now}")
        .limit(1)
    )
    seasons = table._run(query)
    return seasons[0] if seasons else None
