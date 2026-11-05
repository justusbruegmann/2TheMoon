from uuid import UUID

from app.config.dependencies import UserDb
from app.util.response import DomainError


def trades_get_all(db: UserDb):
    return db.trades.find()


def trades_get_one(db: UserDb, trade_id: UUID):
    trade = db.trades.get(id=trade_id)
    if trade is None:
        raise DomainError(status_code=404, message="Found no trade with this id")
    return trade



############################
# YAGNI – But here they are anyways since I already wrote them
# And these can work as a template for other routers
############################

# def trades_post_one(db: UserDb, payload: TradeInsert):
#     return db.trades.insert(payload)[0]
#
#
# def trades_patch_one(db: UserDb, trade_id: UUID, payload: TradeInsert):
#     if not payload.model_fields_set:
#         raise DomainError(status_code=400, message="No fields to update")
#     updated_trade_list = db.trades.update(payload.model_dump(exclude_unset=True), id=trade_id)
#     if not updated_trade_list:
#         raise DomainError(status_code=404, message="Found no trade with this id")
#     return updated_trade_list[0]
#
#
# def trades_delete_one(db: UserDb, trade_id: UUID):
#     deleted_trade_list = db.trades.delete(id=trade_id)
#     if not deleted_trade_list:
#         raise DomainError(status_code=404, message="Found no trade with this id")
#     return deleted_trade_list[0]
