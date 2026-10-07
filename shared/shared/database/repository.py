import httpx
from postgrest.exceptions import APIError

from .supabase_client import get_secret_client



###############################
# Database Tables
###############################
TEST = "testing-table"



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

    def test_request(self, id: int):
        try:
            return (
                self._client
                .table(TEST)
                .select("*")
                .eq("id", id)
                .execute()
            )
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Query to table '{TEST}' failed")


db = Database(get_secret_client())
