from contextlib import contextmanager

from fastapi.testclient import TestClient

from app.config.config import settings
from app.config.dependencies import get_user_db
from app.main import app
from ..conftest import FakeTable

#################################################################
# Shared testing fixtures for all router tests (since they all look very similar):
# - a fixture that overrides get_user_db
#################################################################

_ = FakeTable  # Keep PyCharm from marking the import as unused and removing it when formatting. Pytest will fail if it is missing.

client = TestClient(app)

VALID_HEADERS = {"Authorization": "Bearer test-token"}
GAMESERVER_HEADERS = {**VALID_HEADERS, "Authorization_Gameserver": settings.gameserver_shared_secret}


@contextmanager
def override_user_db(db):
    previous = app.dependency_overrides.get(get_user_db)
    app.dependency_overrides[get_user_db] = lambda: db
    yield db
    if previous is not None:
        app.dependency_overrides[get_user_db] = previous
    else:
        app.dependency_overrides.pop(get_user_db, None)
