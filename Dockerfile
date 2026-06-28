# ---- Build stage ----
FROM python:3.14-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

RUN pip install --no-cache-dir uv

WORKDIR /build
COPY pyproject.toml uv.lock ./
COPY core/ core/
COPY app/ app/
COPY openrouter/ openrouter/

RUN uv sync --frozen --no-dev

# ---- Runtime stage ----
FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/core /app/core
COPY --from=builder /build/app /app/app
COPY --from=builder /build/openrouter /app/openrouter

RUN chown -R appuser:appuser /app

WORKDIR /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "app.src.main.main"]
