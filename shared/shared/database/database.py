from decimal import Decimal
from functools import lru_cache
from typing import Any, get_args

import httpx
from postgrest import APIError
from pydantic import BaseModel
from supabase import Client, ClientOptions, create_client

from .database_error import DatabaseError, status_code_of
from .models.test import Test
from ..config import DbSettings
from .models import (
    Asset,
    Insert,
    MarketEvent,
    Portfolio,
    PortfolioHistory,
    PriceHistory,
    Profile,
    Season,
    Trade,
    UserAsset,
)


class Table[RowT: BaseModel]:
    def __init__(self,
                 client: Client,
                 name: str,
                 model: type[RowT]
                 ) -> None:
        self.client = client
        self.name = name
        self.model = model
        self.columns = ",".join(
            f"{field}::text" if Decimal in (info.annotation, *get_args(info.annotation)) else field
            for field, info in model.model_fields.items()
        )

    def find(self,
             order_by: str | None = None,
             desc: bool = False,
             limit: int | None = None,
             **filters: Any
             ) -> list[RowT]:

        query = self.client.table(self.name).select(self.columns)
        for column, value in filters.items():
            query = query.eq(column, str(value))
        if order_by:
            query = query.order(order_by, desc=desc)
        if limit:
            query = query.limit(limit)
        return self._run(query)

    def get(self, **filters: Any) -> RowT | None:
        rows = self.find(limit=1, **filters)
        return rows[0] if rows else None

    def insert(self, *rows: Insert) -> list[RowT]:
        payload = [row.to_payload() for row in rows]
        return self._run(
            self.client.table(self.name).insert(payload, default_to_null=False).select(self.columns)
        )

    def upsert(self, row: Insert, on_conflict: str) -> RowT:
        query = self.client.table(self.name).upsert(row.to_payload(), on_conflict=on_conflict)
        return self._run(query.select(self.columns))[0]

    def update(self, values: dict[str, Any], **filters: Any) -> list[RowT]:
        if not filters:
            raise ValueError("update needs at least one filter")
        query = self.client.table(self.name).update(values)
        for column, value in filters.items():
            query = query.eq(column, str(value))
        return self._run(query.select(self.columns))

    def delete(self, **filters: Any) -> list[RowT]:
        if not filters:
            raise ValueError("delete needs at least one filter")
        query = self.client.table(self.name).delete()
        for column, value in filters.items():
            query = query.eq(column, str(value))
        return self._run(query.select(self.columns))

    def _run(self, query: Any) -> list[RowT]:
        try:
            response = query.execute()
        except (APIError, httpx.HTTPError) as error:
            raise DatabaseError(
                f"Request on table '{self.name}' failed: {getattr(error, "message", str(error))}",
                status_code=status_code_of(error),
            ) from error
        return [self.model.model_validate(row) for row in response.data]


class Database:
    def __init__(self, client: Client) -> None:
        self.profiles = Table(client, "profile", Profile)
        self.seasons = Table(client, "season", Season)
        self.assets = Table(client, "asset", Asset)
        self.portfolios = Table(client, "portfolio", Portfolio)
        self.trades = Table(client, "trade", Trade)
        self.user_assets = Table(client, "user_asset", UserAsset)
        self.portfolio_history = Table(client, "portfolio_history", PortfolioHistory)
        self.price_history = Table(client, "price_history", PriceHistory)
        self.market_events = Table(client, "market_event", MarketEvent)

        self.test = Table(client, "testing_table", Test)


@lru_cache(maxsize=1)
def get_settings() -> DbSettings:
    return DbSettings()


def _create_client(key: str, access_token: str | None = None) -> Client:
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    options = ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
        headers=headers,
        httpx_client=httpx.Client(timeout=30, follow_redirects=True),
    )
    return create_client(get_settings().supabase_url, key, options)


def get_public_db(access_token: str) -> Database:
    if not access_token:
        raise ValueError("access_token is required")
    return Database(_create_client(get_settings().supabase_publishable_key, access_token))


@lru_cache(maxsize=1)
def get_secret_db() -> Database:
    secret_key = get_settings().supabase_secret_key
    if not secret_key:
        raise RuntimeError("SUPABASE_SECRET_KEY is not set")
    return Database(_create_client(secret_key))
