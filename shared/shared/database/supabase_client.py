from functools import lru_cache
from httpx import Client as HttpxClient
from postgrest.constants import DEFAULT_POSTGREST_CLIENT_TIMEOUT
from supabase import Client, ClientOptions, create_client
from ..config import DbSettings



# With caching to reuse existing clients

@lru_cache(maxsize=1)
def get_settings() -> DbSettings:
    return DbSettings()


@lru_cache(maxsize=1)
def get_client() -> Client:
    s = get_settings()
    # Pass our own httpx client so supabase doesn't forward the now-deprecated
    # timeout/verify kwargs directly to postgrest's client.
    options = ClientOptions(httpx_client=HttpxClient(timeout=DEFAULT_POSTGREST_CLIENT_TIMEOUT))
    return create_client(s.supabase_url, s.supabase_publishable_key, options)
