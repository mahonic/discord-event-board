FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /code

CMD ["python", "main.py"]