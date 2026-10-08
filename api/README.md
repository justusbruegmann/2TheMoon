# 2TheMoon API

## Dev Setup

Install `uv`, then clone the repository and install the dependencies. `uv sync` automatically creates `.venv` and installs the local shared package.

```bash
git clone https://github.com/justusbruegmann/2TheMoon.git
cd 2TheMoon/api
uv sync --locked
```

Create .env and fill in the [supabase keys](https://supabase.com/dashboard/project/ryunncblswchrbxygtvq/settings/api-keys)

```dotenv
SUPABASE_URL=
SUPABASE_PUBLISHABLE_KEY=
SUPABASE_SECRET_KEY=
```

## Running the application

```bash
uv run fastapi dev
```