# Dockerfile
FROM python:3.10-slim as base

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM base as runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    default-mysql-client default-libmysqlclient-dev systemctl jq sudo \
    && apt-get -y clean

WORKDIR /app

COPY --from=base /app/requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
