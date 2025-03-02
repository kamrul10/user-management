# Use official Python image
FROM python:3.12-alpine

# Create user to avoid running as root
RUN adduser -D -h /home/app-src app-src

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3

# Set the working directory
WORKDIR /usr/src/app-src

# Copy pyproject.toml and install dependencies
# Update pip
RUN apk update && \
    apk upgrade --no-cache
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml ./

RUN poetry install --only=main --no-interaction --no-ansi --no-cache

# Copy the app code
COPY . /usr/src/app-src

# Expose REST and gRPC ports
EXPOSE 8000 50051

# Run both REST and gRPC services
CMD ["sh", "-c", "uvicorn api.rest_api.main:app  --host 0.0.0.0 --port 8000 & python -m api.grpc.grpc_service"]
