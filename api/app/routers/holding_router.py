from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.domain.holding import holdings_get_one
from shared.database.models import Holding
from shared.database.models.api_response import ApiResponse

#####################
# Information
#####################
# RLS
#
# - GET /holdings/:id     Only the owning user may see their own holding
# -
#####################

router = APIRouter()


@router.get(
    path="/{holding_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Holding],
    description="Returns the holding with the specified id"
)
def handle_get_one(db: UserDb, holding_id: UUID):
    holdings_get_one(db, holding_id)

############################
# YAGNI – But here they are anyways since I already wrote them
# And these can work as a template for other routers
############################

# @router.post(
#     path="/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ApiResponse[Holding],
#     description="Creates a new type of holding"
# )
# def holdings_post_one(payload: HoldingInsert, db: UserDb):
#     try:
#         row = db.holdings.insert(payload)[0]
#     except DatabaseError as e:
#         raise db_error_response(e)
#     return success_response(data=row.model_dump(by_alias=True, mode="json"))
#
#
# @router.patch(
#     path="/{holding_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=ApiResponse[Holding],
#     description="Update the holding with the given id"
# )
# def holdings_patch_one(holding_id: UUID, payload: HoldingInsert, db: UserDb):
#     if not payload.model_fields_set:
#         raise error_response(status_code=400, message="No fields to update")
#     try:
#         rows = db.holdings.update(payload.model_dump(exclude_unset=True), id=holding_id)
#     except DatabaseError as e:
#         raise db_error_response(e)
#     if not rows:
#         raise error_response(status_code=404, message="Found no holding with this id")
#     return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
#
#
# @router.delete(
#     path="/{holding_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     description="Delete the holding with the given id"
# )
# def holdings_delete_one(holding_id: UUID, db: UserDb):
#     try:
#         rows = db.holdings.delete(id=holding_id)
#     except DatabaseError as e:
#         raise db_error_response(e)
#     if not rows:
#         raise error_response(status_code=404, message="Found no holding with this id")
#     return success_response(data=rows[0].model_dump(by_alias=True, mode="json"))
