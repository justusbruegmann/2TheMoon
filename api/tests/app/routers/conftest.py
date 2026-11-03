from contextlib import contextmanager
from uuid import uuid4

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.config import settings
from app.dependencies import get_user_db
from app.main import app



#################################################################
# Shared testing fixtures for all router tests (since they all look very similar):
# - a FakeTable per db table
# - a fixture that overrides get_user_db
#################################################################

client = TestClient(app)

VALID_HEADERS = {"Authorization": "Bearer test-token"}
GAMESERVER_HEADERS = {**VALID_HEADERS, "Authorization_Gameserver": settings.gameserver_shared_secret}


class FakeTable:
    #################################
    # Testing replacement for shared.database.database.Table.
    #################################
    def __init__(self, model: type[BaseModel], extra_fields=lambda: {}):
        self.model = model
        self.extra_fields = extra_fields
        self._rows: dict[str, BaseModel] = {}

    def find(self, **_filters):
        return list(self._rows.values())

    def get(self, **filters):
        return self._rows.get(str(filters["id"]))

    def insert(self, *rows):
        created = []
        for row in rows:
            fields = self.extra_fields()
            entry = self.model(**row.model_dump(exclude=set(fields)), **fields)
            self._rows[str(fields.get("id", uuid4()))] = entry
            created.append(entry)
        return created


@contextmanager
def override_user_db(db):
    app.dependency_overrides[get_user_db] = lambda: db
    yield db
    app.dependency_overrides.pop(get_user_db, None)
