from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Login data for the test user in supabase. These are used for the auth token generating script in
    # /scripts/get_test_token.py
    supabase_url: str | None = None
    supabase_publishable_key: str | None = None
    test_user_email: str | None = None
    test_user_password: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
