from uuid import UUID

from app.dependencies import UserDb
from app.util.response import DomainError
from shared.database.models import AssetInsert, Holding


def holdings_get_one(db: UserDb, holding_id: UUID):
    holding: Holding = db.holdings.get(id=holding_id)
    if holding is None:
        raise DomainError(status_code=404, message="Found no holding with this id")
    return holding


############################################################
# For internal use only – not hooked up to an API endpoint
############################################################

def assets_post_one(db: UserDb, payload: AssetInsert):
    return db.assets.insert(payload)[0]


def assets_patch_one(db: UserDb, asset_id: UUID, payload: AssetInsert):
    if not payload.model_fields_set:
        raise DomainError(status_code=400, message="No fields to update")
    rows = db.assets.update(payload.model_dump(exclude_unset=True), id=asset_id)
    if not rows:
        raise DomainError(status_code=404, message="Found no asset with this id")
    return rows[0]
