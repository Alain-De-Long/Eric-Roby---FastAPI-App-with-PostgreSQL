FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

ENV UV_NO_DEV=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

# RUN uv sync --locked --no-install-project
RUN uv pip install --no-cache -r pyproject.toml

COPY . .

EXPOSE 8000

CMD [ "uvicorn" , "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
