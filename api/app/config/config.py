from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Login data for the test user in supabase. These are used for the auth token generating script in
    # /scripts/get_test_token.py
    supabase_url: str | None = None
    supabase_publishable_key: str | None = None
    test_user_email: str | None = None
    test_user_password: str | None = None

    # Shared secret for all communication with the gameserver – necessary for the gameserver to call special, protected
    # endpoints that should not be callable from the frontend.
    gameserver_shared_secret: str


settings = Settings()
