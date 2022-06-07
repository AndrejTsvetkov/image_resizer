FROM python:3.9

ENV PYTHONPATH=/code

RUN mkdir /code
WORKDIR /code

# requirements (poetry)
COPY ./poetry.lock ./poetry.toml ./pyproject.toml  /code/

RUN pip install poetry
RUN POETRY_VIRTUALENVS_CREATE=false poetry install

COPY ./app  /code/app/
COPY ./Makefile /code

ENTRYPOINT []