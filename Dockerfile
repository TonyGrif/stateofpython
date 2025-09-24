FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /stateofpython
ADD pyproject.toml README.md uv.lock .
ADD pypi/ ./pypi
ADD scripts/ ./scripts

RUN uv sync --no-dev --locked

CMD ["uv", "run", "scripts/get_latest_index.py"]
