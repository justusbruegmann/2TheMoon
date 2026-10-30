from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.util.response import error_response
from shared.database import Database, get_public_db

bearer = HTTPBearer(auto_error=False)


def get_user_db(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> Database:
    if not credentials:
        raise error_response(status_code=401, message="Authentication header missing or malformed")
    return get_public_db(credentials.credentials)


UserDb = Annotated[Database, Depends(get_user_db)]
# SecretDbDep = Annotated[Database, Depends(get_secret_db)]
