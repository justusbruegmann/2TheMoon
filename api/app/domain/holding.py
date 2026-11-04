from uuid import UUID

from app.dependencies import UserDb
from app.util.response import DomainError
from shared.database.models import Holding, HoldingUpdate


def holdings_get_one(db: UserDb, holding_id: UUID):
    holding: Holding = db.holdings.get(id=holding_id)
    if holding is None:
        raise DomainError(status_code=404, message="Found no holding with this id")
    return holding


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
