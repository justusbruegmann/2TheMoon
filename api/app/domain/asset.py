from uuid import UUID

from app.dependencies import UserDb
from app.util.response import DomainError


def assets_get_all(db: UserDb):
    return db.assets.find()


def assets_get_one(db: UserDb, asset_id: UUID):
    row = db.assets.get(id=asset_id)
    if row is None:
        raise DomainError(status_code=404, message="Found no asset with this id")
    return row

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
#     rows = db.assets.update(payload.model_dump(exclude_unset=True), id=asset_id)
#     if not rows:
#         raise DomainError(status_code=404, message="Found no asset with this id")
#     return rows[0]
#
#
# def assets_delete_one(db: UserDb, asset_id: UUID):
#     rows = db.assets.delete(id=asset_id)
#     if not rows:
#         raise DomainError(status_code=404, message="Found no asset with this id")
#     return rows[0]
