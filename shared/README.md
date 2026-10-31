# 2TheMoon Shared

Shared database code for the API and game server. It is a library, not an application.

## Setup

```bash
cd 2TheMoon/shared
uv sync --locked
```

The modules that use it need `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY` in their environment or `.env`; the game
server also needs `SUPABASE_SECRET_KEY`.

## Usage

The tables live in `supabase/supabase/migrations/`. `shared/database/models/` has one file per table with its model
(`Trade`) plus an insert model (`TradeInsert`) for tables where the database fills in ids or timestamps. If you change a
table in a migration, change its model too.

There are two ways to get a `Database`:

- `get_public_db(access_token)` uses the publishable key plus the player's Supabase JWT, so Row Level Security applies.
  Use it in the API. Players can only read; the RLS policies allow no writes.
- `get_secret_db()` uses the secret key and bypasses RLS. Use it in the game server, and in the API only for writes the
  backend does on a player's behalf (e.g. recording a trade).

```python
from shared.database import get_secret_db
from shared.database.models import TradeInsert

db = get_secret_db()

season = db.seasons.get(status="active")
trades = db.trades.find(portfolio_id=portfolio.id, order_by="executed_at", desc=True, limit=20)
db.trades.insert(TradeInsert(...))
db.portfolios.update({"cash_balance": "9500"}, id=portfolio.id)
db.user_assets.upsert(holding, on_conflict="portfolio_id,asset_id")
db.market_events.delete(id=event.id)
```

Every table has `find`, `get`, `insert`, `upsert`, `update` and `delete`. Keyword arguments are equality filters. Failed
requests raise `DatabaseError`. For anything else, use `db.trades.client` directly.

In the API, use `UserDbDep` (reads the `Authorization: Bearer <jwt>` header) or `SecretDbDep` from
`app/dependencies.py`.

## Tests

```bash
uv run pytest
```
