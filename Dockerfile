FROM python:3.8.6-slim-buster AS base
RUN apt-get update -y && apt-get install -y curl 
WORKDIR /app

COPY poetry.toml poetry.toml
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL \
https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | \
python
RUN poetry config virtualenvs.create false --local
RUN poetry install

# PROD IMAGE
    FROM base as production
    RUN pip install gunicorn
    COPY todo_app todo_app 
    EXPOSE 5000
    ENTRYPOINT [ "gunicorn","--bind","0.0.0.0:5000","todo_app.app:app"]

# DEV IMAGE
    FROM base as development
    EXPOSE 5100
    ENTRYPOINT [ "flask","run","--host","0.0.0.0"]