from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import UserDb
from app.domain.asset import assets_get_all, assets_get_one
from app.util.response import api_response
from shared.database.models import Asset
from shared.database.models.api_response import ApiResponse

#####################
# Information
#
# I design routers to be included in main.py with a shared path (e.g. /assets/) and only define the subpaths here.
#
# Endpoints will be named according to convention with the plural name of the requested resource
# (e.g. assets instead of asset)
#####################
# RLS
#
# - GET /assets         Anyone may see all assets
# - GET /assets/:id     Anyone may see one asset's details
#####################

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[Asset]],
    description="Returns a list of all available assets"
)
@api_response
def handle_get_all_assets(db: UserDb):
    return assets_get_all(db)


@router.get(
    path="/{asset_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[Asset],
    description="Returns the asset with the specified id"
)
@api_response
def handle_get_one_asset(db: UserDb, asset_id: UUID):
    return assets_get_one(db, asset_id)
