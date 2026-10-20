from supabase import create_client

from shared.config import DbSettings



"""
Generate a real Supabase token for the test user.

Run with `uv run python scripts/get_test_token.py`

This script requires SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY TEST_USER_EMAIL and TEST_USER_PASSWORD to be set in .env.
"""
def get_test_access_token(settings: DbSettings | None = None) -> str:
    settings = settings or DbSettings()
    if not settings.test_user_email or not settings.test_user_password:
        raise RuntimeError("TEST_USER_EMAIL and TEST_USER_PASSWORD must be set")

    client = create_client(settings.supabase_url, settings.supabase_publishable_key)
    response = client.auth.sign_in_with_password(
        {"email": settings.test_user_email, "password": settings.test_user_password}
    )
    return response.session.access_token


if __name__ == "__main__":
    print(get_test_access_token())
