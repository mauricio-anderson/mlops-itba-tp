
FROM python:3.9-slim-buster

# pipx & poetry
ENV PATH="/root/.local/bin:$PATH"
ENV PATH="/root/.local/pipx/venvs/poetry/bin/:$PATH"

# Set up the environment
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update --assume-yes && apt-get upgrade --assume-yes

# Setup pipx and poetry
RUN apt-get install curl --assume-yes
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.5.1
RUN poetry config virtualenvs.create false

# Copy files
COPY pyproject.toml poetry.lock /src/project/
WORKDIR /src/project
RUN poetry install --no-interaction --no-root
COPY . /src/project
RUN poetry install --no-interaction

# Cleanup
RUN apt-get purge --auto-remove -yqq  \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

EXPOSE 80 5000 8080
