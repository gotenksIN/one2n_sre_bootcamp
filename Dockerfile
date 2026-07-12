FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

WORKDIR /build

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-install-project

FROM python:3.14-slim

RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/sh -m -d /home/appuser appuser

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder --chown=appuser:appuser /build/.venv /app/.venv
COPY --chown=appuser:appuser app/ app/
COPY --chown=appuser:appuser migrations/ migrations/

USER appuser

EXPOSE 5000

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]
