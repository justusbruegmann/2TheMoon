import httpx
from postgrest.exceptions import APIError

from .models.fastapi.schema_public_latest import *
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

    def test_select(self, id: int):
        try:
            res = (
                self._client
                .table(TESTING_TABLE.name)
                .select(TESTING_TABLE.columns)
                .eq(TESTING_TABLE.col("id"), id)
                .limit(1)
                .execute()
            )
            rows = TESTING_TABLE.parse(res.data)
            return rows[0] if rows else None
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Query to table '{TESTING_TABLE.name}' failed")



    def test_select_all(self):
        try:
            res = (
                self._client
                .table(TESTING_TABLE.name)
                .select(TESTING_TABLE.columns)
                .execute()
            )
            return TESTING_TABLE.parse(res.data)
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Query to table '{TESTING_TABLE.name}' failed")



    def test_insert(self, data: TestingTableInsert) -> TestingTableBaseSchema:
        try:
            res = (
                self._client
                .table(TESTING_TABLE.name)
                .insert(data.to_payload())
                .execute()
            )
            return TESTING_TABLE.parse(res.data)[0]
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Insert into table '{TESTING_TABLE.name}' failed")



    def test_update(self, id: int, data: TestingTableUpdate) -> list[TestingTableBaseSchema]:
        try:
            res = (
                self._client
                .table(TESTING_TABLE.name)
                .update(data.to_payload())
                .eq(TESTING_TABLE.col("id"), id)
                .execute()
            )
            return TESTING_TABLE.parse(res.data)
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Update on table '{TESTING_TABLE.name}' failed")



    def test_delete(self, id: int) -> list[TestingTableBaseSchema]:
        try:
            res = (
                self._client
                .table(TESTING_TABLE.name)
                .delete()
                .eq(TESTING_TABLE.col("id"), id)
                .execute()
            )
            return TESTING_TABLE.parse(res.data)
        except (APIError, httpx.HTTPError):
            raise DatabaseError(f"Delete on table '{TESTING_TABLE.name}' failed")



db = Database(get_secret_client())
