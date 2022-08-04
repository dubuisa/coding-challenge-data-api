 
<h1 align="center">
    Coding Challenge Data API
</h1>
<p align="center">
    <a href="#" title="Python Version"><img src="https://img.shields.io/badge/Python-3.9%2B-blue&style=flat"></a>
    <a href="#" title="Test status"><img src="https://github.com/dubuisa/coding-challenge-data-api/workflows/Tests/badge.svg"></a>
    <a href="https://app.codecov.io/gh/dubuisa/coding-challenge-data-api" title="Test status"><img src="https://codecov.io/gh/dubuisa/coding-challenge-data-api/branch/master/graph/badge.svg"></a>
</p>


FastAPI project that uses 
 - async SQLAlchemy
 - SQLModel
 - Postgres
 - Alembic
 - Docker

## How to run this API?
To launch this project, you must have docker compose installed (see [link](https://docs.docker.com/compose/install/) for installation)

Then you can run the following command to run the project
```sh
$ docker compose up -d --build
```

Once the component is instantiated, you can visit the endpoint documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

Enpoint documentation can be used to interact with the API graphically. It is also possible to query the api directly using curl as follows:

```sh
curl -X 'POST' \
  'http://localhost:8000/data/256/2048' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Hello World!",
  "language": "en"
}'
```

## How to run tests:

You can simply do the following:

```sh
poetry install
poetry run pytest --cov=app --cov=tests --cov-report=term-missing
```


