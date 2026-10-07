from pydantic_settings import BaseSettings, SettingsConfigDict



# These environment variables need to be set in the modules that load the shared/ library!

class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", extra="ignore", env_file=".env")

    supabase_url: str
    supabase_publishable_key: str
    supabase_secret_key: str
