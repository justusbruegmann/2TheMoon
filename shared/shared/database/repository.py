from enum import Enum

from .supabase_client import get_secret_client



class DatabaseTables(Enum):
    TEST = "test"


class Database:
    def __init__(self, client):
        self._client = client


    # Add database requests here

    def test_request(self, test_id: str):
        return (self._client
                .table(DatabaseTables.TEST)
                .select("*")
                .eq("asdf", test_id)
                .execute()
                )


db = Database(get_secret_client())
