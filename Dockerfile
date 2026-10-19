FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project

COPY tripmateai_langgraph_multiagent ./tripmateai_langgraph_multiagent

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "tripmateai_langgraph_multiagent.api:app", "--host", "0.0.0.0", "--port", "8000"]