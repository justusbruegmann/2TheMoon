from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str
    supabase_publishable_key: str
    supabase_secret_key: str | None = None

    # Login data for the test user in supabase. These are used for integration tests to the database.
    # If they are not set, the integration test is skipped.
    test_user_email: str | None = None
    test_user_password: str | None = None
