# 2TheMoon Shared

Shared database models and utilities for the API and game server.

## Dev Setup

Install `uv`, then clone the repository and install the dependencies. `uv sync` automatically creates `.venv`.

```bash
git clone https://github.com/justusbruegmann/2TheMoon.git
cd 2TheMoon/shared
uv sync --locked
```

Update supabase types.
You can find the [DB CONNECTION STRING] on Discord (documents channel).

```bash
uv run sb-pydantic gen --type pydantic --db-url "[DB CONNECTION STRING]" --dir shared/database/models
```

## Usage

This package is installed automatically when running `uv sync` in `api/` or `gameserver/`. Editable installation makes Python code changes available without reinstalling; restart running processes to load them.

Shared is a library and does not run as a separate application.