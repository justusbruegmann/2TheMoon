import httpx
from postgrest.exceptions import APIError

from .supabase_client import get_secret_client



###############################
# Database Tables
###############################
TEST = "test"



class DatabaseError(Exception):
    """
    Throw this if a database request fails
    """
    pass



class Database:

    def __init__(self, client):
        self._client = client


    ###############################
    # Add database requests here
    ###############################

    def test_request(self, test_id: str):
        try:
            return (self._client
                    .table(TEST)
                    .select("*")
                    .eq("asdf", test_id)
                    .execute()
                    )
        except (APIError, httpx.HTTPError) as exc:
            raise DatabaseError(
                f"Query to table '{TEST}' failed"
            ) from exc


db = Database(get_secret_client())
