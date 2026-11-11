# 2TheMoon Game Server

Loads all assets from Supabase on startup, simulates a new price per asset every tick and writes them to the Redis stream `market:prices`.

## Installation

Install `uv`, then:

```bash
git clone https://github.com/justusbruegmann/2TheMoon.git
cd 2TheMoon/gameserver
uv sync --locked
```

## Environment (`gameserver/.env`)

| Variable | Required | Default |
|---|---|---|
| `REDIS_URL` | yes (set by `docker-compose.yaml`) | – |
| `SUPABASE_URL` | yes | – |
| `SUPABASE_PUBLISHABLE_KEY` | yes | – |
| `SUPABASE_SECRET_KEY` | yes | – |
| `TICKS_PER_S` | no | `1.0` |
| `INITIAL_PRICE` | no | `100.0` |
| `VOLATILITY` | no | `0.01` |
| `MARKET_STREAM` | no | `market:prices` |
| `MARKET_STREAM_MAXLEN` | no | `10000` |
| `HEALTHCHECK_PATH` | no | `/tmp/healthcheck` |

## Running

With Docker (from the repository root, starts Redis as well):

```bash
docker compose up --build gameserver
```

Locally (needs a reachable Redis, e.g. `docker run -p 6379:6379 redis:7-alpine` and `REDIS_URL=redis://localhost:6379` in `.env`):

```bash
uv run --env-file .env python -m gameserver
```

## Tests

```bash
uv run pytest
```
