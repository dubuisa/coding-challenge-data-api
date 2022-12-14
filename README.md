 
<h1 align="center">
    Coding Challenge Data API
</h1>
<p align="center">
    <a href="#" title="Python Version"><img src="https://img.shields.io/badge/Python-3.9%2B-blue&style=flat"></a>
    <a href="#" title="Test status"><img src="https://github.com/dubuisa/coding-challenge-data-api/workflows/Tests/badge.svg"></a>
    <a href="https://app.codecov.io/gh/dubuisa/coding-challenge-data-api" title="Test status"><img src="https://codecov.io/gh/dubuisa/coding-challenge-data-api/branch/master/graph/badge.svg"></a>
</p>


This API exposes endpoint to:

- Send dialogs
- Consent/Refuse to make the dialogs available
- Retrieve consented dialogs


## How to run this API:
This project requires Docker compose (see [link](https://docs.docker.com/compose/install/) for installation).

To run the project execute the following command:
```sh
$ docker compose up -d --build
```

Once the component is instantiated, you can visit the endpoint documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

Enpoint documentation can be used to interact with the API graphically. It is also possible to query the api directly using curl as follows:

```sh
$ curl -X 'POST' \
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
$ poetry install
$ poetry run pytest tests/ --cov=app --cov=tests --cov-report=term-missing
```


# Disclaimer

This project has been developed and tested only on Linux. 

It is therefore possible that this project will not work "as-is" on a Windows environment.
