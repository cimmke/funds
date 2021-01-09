# Dockerfile for building Django app
FROM python:3.9

ARG DEVEL=no

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip --no-cache-dir --disable-pip-version-check install --upgrade pip setuptools wheel

COPY requirements /tmp/requirements

RUN if [ "$DEVEL" = "yes" ]; then pip --no-cache-dir --disable-pip-version-check install -r /tmp/requirements/dev.txt; fi

RUN pip --no-cache-dir --disable-pip-version-check install -r /tmp/requirements/main.txt