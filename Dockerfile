FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml uv.lock README.md ./

# Install dependencies without installing the project itself
RUN uv sync --frozen --no-dev --no-install-project

# Copy application and migration code
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

# Install the project itself
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["./entrypoint.sh"]