ARG VIRTUAL_ENV=/opt/venv
ARG PLATFORM=linux/amd64

# ---PYTHON_BASE stage---
FROM --platform=$PLATFORM python:3.11.11-slim AS python_base

RUN apt-get update -q \
    && useradd -ms /bin/bash kestra

WORKDIR /app

RUN pip install --upgrade pip setuptools --no-cache-dir

ARG DBT_PROFILES_DIR=/app/dbt
ENV DBT_PROFILES_DIR=$DBT_PROFILES_DIR

ARG DBT_PROJECT_DIR=/app/dbt
ENV DBT_PROJECT_DIR=$DBT_PROJECT_DIR

ENV GCP_PROJECT_ID=

ARG PYTHONPATH=/app/src
ENV PYTHONPATH=$PYTHONPATH

ARG VIRTUAL_ENV
ENV VIRTUAL_ENV=$VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=True

COPY pyproject.toml uv.lock ./

RUN python3 -m venv $VIRTUAL_ENV

RUN apt-get update -q \
    && apt-get install -qy \
    git \
    curl \
    && pip install --upgrade --progress-bar=off pip wheel \
    && pip install setuptools \
    && pip install uv==0.5.29 \
    && uv export --format requirements-txt --no-hashes > requirements.txt \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app

# ---PYTHON_DBT_BASE stage---
FROM --platform=$PLATFORM python_base AS python_dbt_base

WORKDIR /app

RUN dbt deps

# ---TERRAFORM stage---
FROM --platform=$PLATFORM hashicorp/terraform:1.10.5 AS terraform_stage

WORKDIR /app

# ---VS_CODE_DEV stage---
FROM python_dbt_base AS vs_code_dev_100

COPY --from=terraform_stage /bin/terraform /usr/local/bin/terraform

WORKDIR /app

ENV GCP_PROJECT_ID=

RUN uv export --format requirements-txt --no-hashes --group file_linters > requirements_linters.txt \
    && pip install -r requirements_linters.txt \
    && rm -rf /root/.cache/pip

RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get -y install apt-transport-https ca-certificates gnupg \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update && apt-get -y install google-cloud-sdk \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# ---DBT_ONLY stage---
FROM --platform=$PLATFORM python:3.11.10-slim AS dbt_only

WORKDIR /app

ARG DBT_PROFILES_DIR=/app/dbt
ENV DBT_PROFILES_DIR=$DBT_PROFILES_DIR

ARG DBT_PROJECT_DIR=/app/dbt
ENV DBT_PROJECT_DIR=$DBT_PROJECT_DIR

ENV GCP_PROJECT_ID=

COPY pyproject.toml uv.lock ./

RUN apt-get update -q \
    && pip install --upgrade --progress-bar=off pip wheel \
    && pip install setuptools \
    && pip install uv==0.5.29 \
    && uv export --format requirements-txt --no-hashes --group dbt_image > requirements_dbt_image.txt \
    && pip install -r requirements_dbt_image.txt \
    && rm -rf /root/.cache/pip

COPY dbt /app/dbt
