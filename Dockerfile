FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code/

ENV PATH="/code/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project


ENV PYTHONPATH=/app


COPY ./pyproject.toml ./uv.lock ./alembic.ini /code/

COPY ./app /code/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync


CMD ["fastapi", "run", "--workers", "4", "app/main.py"]