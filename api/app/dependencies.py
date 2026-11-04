import hmac
from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.util.response import error_response
from shared.database import Database, get_public_db

bearer = HTTPBearer(auto_error=False)


def get_user_db(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> Database:
    if not credentials:
        raise error_response(status_code=401, message="Authentication header missing or malformed")
    return get_public_db(credentials.credentials)


UserDb = Annotated[Database, Depends(get_user_db)]
# SecretDbDep = Annotated[Database, Depends(get_secret_db)]


def gameserver_route_protection(
        authorization_gameserver: Annotated[str | None, Header(alias="Authorization_Gameserver")] = None
) -> None:
    if not authorization_gameserver or not hmac.compare_digest(
            authorization_gameserver, settings.gameserver_shared_secret
    ):
        raise error_response(status_code=401, message="Invalid or missing gameserver authorization")
