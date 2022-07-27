# Small-ish Coding excercise

This application comprises of four different services all running in different docker containers
within the same network, three of which are internal and only within the network.


### Services
- Posts service that receives blog posts which consist of a title
and one or more paragraphs and is the only service exposed publicly. This service calls the internal ml service and request to the ml service are run asynchronously on a worker service.
- Dummy ML service which content moderation ML model that can detect foul
language in text. This model is exposed as an internal REST API. The model operates
at the sentence level. It can only process one sentence a time(just a dummy, no actual model) and request to this service are made via a worker.
- A redis service which acts as a message broker to disribute tasks across workers and manages task queue
- A worker service(Celery) that executes the tasks dleivered by the broker.



This application is a REST API that receives blog posts which consist of a title
and one or more paragraphs and detects if there's a foul language present. Sample request below:

```
    curl -X 'POST' 'http://127.0.0.1:8000/posts/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
        "title": "This is an engaging title",
        "paragraphs": [
        "This is the first paragraph. It contains two sentences.",
        "This is the second parapgraph. It contains two more sentences",
        "Third paraphraph here."
        ]
    }'
```

## How to run
To run this app, you need to have docker and docker-compose installed, after which you can run
```commandline
docker-compose up
```
This should bring the entire stack up and run all the services in their respective containers. the app would be available on `http://localhost:8000/posts/`

## Running tests
```commandline
docker build -f tests.Dockerfile -t tests . && docker run -it tests
```

