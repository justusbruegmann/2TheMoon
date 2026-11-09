# 2TheMoon API

## Dev Setup

Install `uv`, then clone the repository and install the dependencies. `uv sync` automatically creates `.venv` and installs the local shared package.

```bash
git clone https://github.com/justusbruegmann/2TheMoon.git
cd 2TheMoon/api
uv sync --locked
```

Create .env and fill in the [supabase keys](https://supabase.com/dashboard/project/ryunncblswchrbxygtvq/settings/api-keys)
If you want to run tests against the live database, fill in the login data for the test user as is registered on Supabase.
To communicate with the gameserver, add a shared secret. This is unused as of yet, but required. You can fill in arbitrary text for now.

```dotenv
SUPABASE_URL=
SUPABASE_PUBLISHABLE_KEY=

TEST_USER_EMAIL=
TEST_USER_PASSWORD=

GAMESERVER_SHARED_SECRET=
```

## Running the application

```bash
uv run fastapi dev
```