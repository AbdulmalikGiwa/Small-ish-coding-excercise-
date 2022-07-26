FROM python:3.9-slim

RUN mkdir /ml-service

COPY . /ml-service

COPY pyproject.toml /ml-service

WORKDIR /ml-service

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev


CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "-p 5001"]