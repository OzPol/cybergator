FROM python:3.12-slim-bookworm AS builder
ARG POETRY_VERSION=2.5.1
ARG INSTALL_EXTRAS=""
ENV PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /app
RUN pip install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock ./
RUN if [ -n "$INSTALL_EXTRAS" ]; then \
      poetry install --only main --no-root --extras "$INSTALL_EXTRAS"; \
    else \
      poetry install --only main --no-root; \
    fi

FROM python:3.12-slim-bookworm AS runtime
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0

RUN groupadd --gid 10001 cybergator && \
    useradd --uid 10001 --gid cybergator --create-home cybergator
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --chown=cybergator:cybergator . .
USER cybergator

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)"
CMD ["python", "app.py"]
