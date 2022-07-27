FROM python:3.9-slim

RUN mkdir /posts_service

COPY . /posts_service


WORKDIR /posts_service

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

WORKDIR /posts_service/server


CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "-p 5000"]