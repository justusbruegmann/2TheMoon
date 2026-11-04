from uuid import UUID

from app.dependencies import UserDb
from app.util.response import DomainError


def assets_get_all(db: UserDb):
    return db.assets.find()


def assets_get_one(db: UserDb, asset_id: UUID):
    asset = db.assets.get(id=asset_id)
    if asset is None:
        raise DomainError(status_code=404, message="Found no asset with this id")
    return asset

############################
# YAGNI – But here they are anyways since I already wrote them
# And these can work as a template for other routers
############################

# def assets_post_one(db: UserDb, payload: AssetInsert):
#     return db.assets.insert(payload)[0]
#
#
# def assets_patch_one(db: UserDb, asset_id: UUID, payload: AssetInsert):
#     if not payload.model_fields_set:
#         raise DomainError(status_code=400, message="No fields to update")
#     updated_asset_list = db.assets.update(payload.model_dump(exclude_unset=True), id=asset_id)
#     if not updated_asset_list:
#         raise DomainError(status_code=404, message="Found no asset with this id")
#     return updated_asset_list[0]
#
#
# def assets_delete_one(db: UserDb, asset_id: UUID):
#     deleted_asset_list = db.assets.delete(id=asset_id)
#     if not deleted_asset_list:
#         raise DomainError(status_code=404, message="Found no asset with this id")
#     return deleted_asset_list[0]
