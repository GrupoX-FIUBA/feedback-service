FROM python:3.9-alpine as base

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt


# Test stage
FROM base as test

COPY ./requirements.dev.txt ./requirements.dev.txt
COPY ./test.sh ./test.sh

RUN pip install -r ./requirements.dev.txt

CMD sh test.sh


# Dev stage
FROM base as development

COPY ./start.sh ./start.sh

CMD sh start.sh


# Prod stage
FROM base as production

COPY ./start.sh ./start.sh
COPY ./app ./app

CMD sh start.sh
