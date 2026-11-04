from uuid import UUID

from app.dependencies import UserDb
from app.util.response import db_error_response, error_response, success_response
from shared.database import DatabaseError


def assets_get_all(db: UserDb):
    try:
        rows = db.assets.find()
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])


def assets_get_one(db: UserDb, asset_id: UUID):
    try:
        row = db.assets.get(id=asset_id)
    except DatabaseError as e:
        raise db_error_response(e)
    if row is None:
        raise error_response(status_code=404, message="Found no asset with this id")
    return success_response(data=row.model_dump(by_alias=True, mode="json"))

############################
# YAGNI – But here they are anyways since I already wrote them
# And these can work as a template for other routers
############################

# def assets_post_one(db: UserDb, payload: AssetInsert):
#     try:
#         row = db.assets.insert(payload)[0]
#     except DatabaseError as e:
#         raise db_error_response(e)
#     return success_response(data=row.model_dump(by_alias=True, mode="json"))
#
#
# def assets_patch_one(db: UserDb, asset_id: UUID, payload: AssetInsert):
#     if not payload.model_fields_set:
#         raise error_response(status_code=400, message="No fields to update")
#     try:
#         rows = db.assets.update(payload.model_dump(exclude_unset=True), id=asset_id)
#     except DatabaseError as e:
#         raise db_error_response(e)
#     if not rows:
#         raise error_response(status_code=404, message="Found no asset with this id")
#     return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
#
#
# def assets_delete_one(db: UserDb, asset_id: UUID):
#     try:
#         rows = db.assets.delete(id=asset_id)
#     except DatabaseError as e:
#         raise db_error_response(e)
#     if not rows:
#         raise error_response(status_code=404, message="Found no asset with this id")
#     return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
