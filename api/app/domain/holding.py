from uuid import UUID

from shared.database.models import Holding, HoldingUpdate

from app.config.dependencies import UserDb
from app.util.response import DomainError


###
def holdings_get(db: UserDb, user_id: UUID, asset_id: UUID | None = None):
    # The return codes we have decided on:
    # If asset_id is requested and not found, return 404
    # If it is not set and nothing is found for this user, return 200 with payload []

    filters = {"user_id": user_id}
    if asset_id is not None:
        filters["asset_id"] = asset_id
    holdings: list[Holding] = db.holdings.find(**filters)
    if asset_id is not None and not holdings:
        raise DomainError(status_code=404, message="Found no holding for this user and asset")
    return holdings


############################################################
# For internal use only – not hooked up to an API endpoint
############################################################

def holdings_post_one(db: UserDb, payload: Holding):
    return db.holdings.insert(payload)[0]


def holdings_patch_one(db: UserDb, holding_id: UUID, payload: HoldingUpdate):
    if not payload.model_fields_set:
        raise DomainError(status_code=400, message="No fields to update")
    updated_holdings_list = db.holdings.update(payload.model_dump(exclude_unset=True), id=holding_id)
    if not updated_holdings_list:
        raise DomainError(status_code=404, message="Found no holding with this id")
    return updated_holdings_list[0]
