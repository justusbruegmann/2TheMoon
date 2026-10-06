# 2TheMoon Shared

Shared database models and utilities for the API and game server.

## Dev Setup

Install `uv`, then clone the repository and install the dependencies. `uv sync` automatically creates `.venv`.

```bash
git clone https://github.com/justusbruegmann/2TheMoon.git
cd 2TheMoon/shared
uv sync --locked
```

## Usage

This package is installed automatically when running `uv sync` in `api/` or `gameserver/`. Editable installation makes Python code changes available without reinstalling; restart running processes to load them.

Shared is a library and does not run as a separate application.