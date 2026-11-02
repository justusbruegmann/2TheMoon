"""
Integration test against the live database. It is skipped if test_user_email or test_user_password are not set as env variables.
"""

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_user_db
from app.main import app
from shared.config import DbSettings
from shared.database import DatabaseError
from shared.database.scripts.get_test_token import get_test_access_token

pytestmark = pytest.mark.integration

client = TestClient(app)


@pytest.fixture(scope="module")
def access_token():
    settings = DbSettings()
    if not settings.test_user_email or not settings.test_user_password:
        pytest.skip("TEST_USER_EMAIL / TEST_USER_PASSWORD not set; skipping live Supabase test")
    return get_test_access_token(settings)


class UnreachableDatabase:
    #####################################
    # Simulates a Supabase/network failure so routes except DatabaseError paths are exercised.
    #####################################

    class _FailingTable:
        def __getattr__(self, _name):
            def _raise(*_args, **_kwargs):
                raise DatabaseError("simulated outage")

            return _raise

    assets = _FailingTable()


def test_database_reachable_with_real_token(access_token):
    response = client.get("/assets", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json().get("success") is True


def test_database_rejects_malformed_token():
    response = client.get("/assets", headers={"Authorization": "Bearer not-a-real-token"})

    assert response.status_code == 401
    assert response.json().get("success") is False
    assert "Expected 3 parts in JWT; got 1" in response.json().get("message")


def test_database_rejects_missing_token():
    response = client.get("/assets", headers={"Authorization": "not-a-token"})

    assert response.status_code == 401
    assert response.json().get("success") is False
    assert response.json().get("message") == "Authentication header missing or malformed"


def test_get_assets_returns_503_when_db_unreachable(access_token):
    app.dependency_overrides[get_user_db] = lambda: UnreachableDatabase()
    try:
        response = client.get("/assets/", headers={"Authorization": f"Bearer {access_token}"})
    finally:
        app.dependency_overrides.pop(get_user_db, None)
    assert response.status_code == 503
