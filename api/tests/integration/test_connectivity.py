"""
Integration test against the live database. It is skipped if test_user_email or test_user_password are not set as env variables.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from shared.database.scripts.get_test_token import get_test_access_token
from shared.config import DbSettings



pytestmark = pytest.mark.integration

client = TestClient(app)


@pytest.fixture(scope="module")
def access_token():
    settings = DbSettings()
    if not settings.test_user_email or not settings.test_user_password:
        pytest.skip("TEST_USER_EMAIL / TEST_USER_PASSWORD not set; skipping live Supabase test")
    return get_test_access_token(settings)


def test_database_reachable_with_real_token(access_token):
    response = client.get("/test/database", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    assert response.json().get("success") is True


def test_database_rejects_malformed_token(access_token):
    response = client.get("/test/database", headers={"Authorization": "Bearer not-a-real-token"})

    assert response.status_code == 503
