# syntax=docker/dockerfile:1

    # ----- Build stage: install dependencies -----
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Keep the folder structure so that the /shared folder will be correctly imported
WORKDIR /app/gameserver

# First we copy the .toml to install dependencies
COPY shared /app/shared
COPY gameserver/pyproject.toml gameserver/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# Copy the rest of the files
COPY gameserver .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


    # ----- Runtime stage -----
FROM python:3.14-slim-bookworm

RUN groupadd --system app && useradd --system --gid app --home /app app

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/gameserver/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app/gameserver
USER app

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
    CMD python -c "import os,sys,time; sys.exit(0 if time.time()-os.path.getmtime('/tmp/healthcheck')<10 else 1)"

CMD ["python", "-m", "gameserver"]