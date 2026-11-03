# syntax=docker/dockerfile:1

    # ----- Build stage: install dependencies -----
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Keep the folder structure so that the /shared folder will be correctly imported
WORKDIR /app/api

# First we copy the .toml to install dependencies
COPY shared /app/shared
COPY api/pyproject.toml api/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# Copy the rest of the files
COPY api .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


    # ----- Runtime stage -----
FROM python:3.14-slim-bookworm

RUN groupadd --system app && useradd --system --gid app --home /app app

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/api/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app/api
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')" || exit 1

# Run FastAPI
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]