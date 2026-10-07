from functools import lru_cache
from supabase import Client, create_client
from ..config import DbSettings



# With caching to reuse existing clients

@lru_cache(maxsize=1)
def get_settings() -> DbSettings:
    return DbSettings()


@lru_cache(maxsize=1)
def get_public_client() -> Client:
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_publishable_key)


@lru_cache(maxsize=1)
def get_secret_client() -> Client:
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_secret_key)
