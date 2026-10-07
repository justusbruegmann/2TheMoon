from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_publishable_key: str
    supabase_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()