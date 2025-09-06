ARG PYTHON
FROM python:3.10

WORKDIR /playground
RUN useradd -m iac

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chown=iac:iac pyproject.toml .
COPY --chown=iac:iac uv.lock .

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-cache --no-dev 

COPY --chown=iac:iac . .

USER iac

EXPOSE 5000/tcp

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask_app:app"]