import httpx
from postgrest.exceptions import APIError

from .models.db_schema_helper import TESTING_TABLE
from .supabase_client import get_secret_client



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
                .table(TESTING_TABLE.name)
                .select(TESTING_TABLE.cols(
                    "id",
                    "bool",
                    "text"
                ))
                .eq(TESTING_TABLE.col("id"), id)
                .execute()
            )
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Query to table '{TESTING_TABLE.name}' failed")


db = Database(get_secret_client())
