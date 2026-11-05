from uuid import UUID

from fastapi import APIRouter, status

from app.config.dependencies import UserDb
from app.domain.holding import holdings_get_one
from app.util.response import api_response
from shared.database.models import Holding
from shared.database.models.api_response import ApiResponse

#####################
# Information
#####################
# RLS
#
# - GET /holdings/:id     Only the owning user may see their own holding
#####################

router = APIRouter()


@router.get(
    path="/{holding_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Holding],
    description="Returns the holding with the specified id"
)
@api_response
def handle_get_one(db: UserDb, holding_id: UUID):
    return holdings_get_one(db, holding_id)



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
# @api_response
# def holdings_post_one(payload: HoldingInsert, db: UserDb):
#     return db.holdings.insert(payload)[0]
#
#
# @router.patch(
#     path="/{holding_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=ApiResponse[Holding],
#     description="Update the holding with the given id"
# )
# @api_response
# def holdings_patch_one(holding_id: UUID, payload: HoldingInsert, db: UserDb):
#     if not payload.model_fields_set:
#         raise DomainError(status_code=400, message="No fields to update")
#     rows = db.holdings.update(payload.model_dump(exclude_unset=True), id=holding_id)
#     if not rows:
#         raise DomainError(status_code=404, message="Found no holding with this id")
#     return rows[0]
#
#
# @router.delete(
#     path="/{holding_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     description="Delete the holding with the given id"
# )
# @api_response
# def holdings_delete_one(holding_id: UUID, db: UserDb):
#     rows = db.holdings.delete(id=holding_id)
#     if not rows:
#         raise DomainError(status_code=404, message="Found no holding with this id")
#     return rows[0]
