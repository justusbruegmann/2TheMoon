from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.util.response import success_response, error_response, db_error_response
from shared.database import DatabaseError
from shared.database.models import Asset
from shared.database.models.api_response import ApiResponse

###########################################################################
# I design routers to be included in main.py with a shared path (e.g. /assets/) and only define the subpaths here.
#
# Endpoints will be named according to convention with the plural name of the requested resource
# (e.g. assets instead of asset)
###########################################################################

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[Asset]],
    description="Returns a list of all available assets"
)
def assets_get_all(db: UserDb):
    try:
        rows = db.assets.find()
    except DatabaseError as e:
        raise db_error_response(e)
    return success_response(data=[r.model_dump(by_alias=True, mode="json") for r in rows])


@router.get(
    path="/{asset_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Asset],
    description="Returns the asset with the specified id"
)
def assets_get_one(asset_id: UUID, db: UserDb):
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

# @router.post(
#     path="/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ApiResponse[Asset],
#     description="Creates a new type of asset"
# )
# def assets_post_one(payload: AssetInsert, db: UserDb):
#     try:
#         row = db.assets.insert(payload)[0]
#     except DatabaseError as e:
#         raise db_error_response(e)
#     return success_response(data=row.model_dump(by_alias=True, mode="json"))
#
#
# @router.patch(
#     path="/{asset_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=ApiResponse[Asset],
#     description="Update the asset with the given id"
# )
# def assets_patch_one(asset_id: UUID, payload: AssetInsert, db: UserDb):
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
# @router.delete(
#     path="/{asset_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     description="Delete the asset with the given id"
# )
# def assets_delete_one(asset_id: UUID, db: UserDb):
#     try:
#         rows = db.assets.delete(id=asset_id)
#     except DatabaseError as e:
#         raise db_error_response(e)
#     if not rows:
#         raise error_response(status_code=404, message="Found no asset with this id")
#     return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
