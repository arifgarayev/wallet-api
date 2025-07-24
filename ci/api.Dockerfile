FROM python:3.13.5 AS DJANGO_CORE

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    libxml2-dev \
    libxmlsec1-dev \
    libsuitesparse-dev \
    git \
    libpq-dev \
    htop \
    vim \
    wget \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

WORKDIR /b2broker-task

COPY pyproject.toml poetry.lock /b2broker-task

RUN poetry install

COPY entrypoints /entrypoints/
RUN chmod +x /entrypoints/*