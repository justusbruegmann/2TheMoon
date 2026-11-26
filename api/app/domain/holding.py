from uuid import UUID

from shared.database.models import Holding, HoldingUpdate

from app.config.dependencies import UserDb
from app.util.response import DomainError
from app.domain.portfolio import portfolio_get_one


###
def holdings_get(db: UserDb, user_id: UUID, asset_id: UUID | None = None):
    # The return codes we have decided on:
    # If the user has no portfolio in the current season, the 404 raised by portfolio_get_one is handed through
    # If asset_id is requested and not found, return 404
    # If it is not set and the portfolio holds no assets (holdings), return 200 with payload []

    # Holdings carry no user_id, so we need to retrieve the user's portfolio for the current season.
    portfolio = portfolio_get_one(db, user_id, None)

    filters = {"portfolio_id": portfolio.id}
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
