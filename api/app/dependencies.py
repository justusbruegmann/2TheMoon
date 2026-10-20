from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.database import Database, get_public_db, get_secret_db


def get_user_db(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> Database:
    return get_public_db(credentials.credentials)


UserDbDep = Annotated[Database, Depends(get_user_db)]
#SecretDbDep = Annotated[Database, Depends(get_secret_db)]
