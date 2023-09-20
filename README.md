# Habitus: Statistics microservice

## Description
This microservice provides endpoints to get statistics and reports about a habit for users.

You can find the API documentation [here](https://arquisoftunal.github.io/statistics_ms/).

## Installation
To run this microservice you can use the following commands:

### Local

First, create a virtual environment and activate it:

**For Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**For Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

Then, install the dependencies:
```bash
pip install -r requirements.txt
```

Finally, run the microservice:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

You can also use the 'make' comand
```bash
make run
```

### Docker

Or you can use the provided Dockerfile to build a Docker image and run it:
```bash
docker build -t habitus_statistics_ms .
docker run --env-file .env -d -p 8000:8000 --name habitus_statistics_ms habitus_statistics_ms
```

or simply use the provided Makefile:
```bash
make build-docker
make run-docker
```
