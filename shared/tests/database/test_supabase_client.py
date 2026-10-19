from shared.database.supabase_client import get_client, get_settings

# For all cached entities let's check whether the same object is returned twice

def test_get_settings_is_cached():
    assert get_settings() is get_settings()


def test_get_public_client_is_cached():
    assert get_client() is get_client()
