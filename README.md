# Flask Docker Pipeline

A Flask REST API with a fully automated CI/CD pipeline using GitHub Actions and Docker.

## What it does

Every time code is pushed to the `main` branch, the pipeline automatically:
1. Runs automated tests with pytest
2. Builds a Docker image
3. Pushes the image to Docker Hub

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns server status |
| GET | `/health` | Returns health check |
| GET | `/time` | Returns current server time |
| GET | `/tasks` | Returns all tasks |
| POST | `/tasks` | Adds a new task |
| PATCH | `/tasks/<id>` | Updates task status |
| DELETE | `/tasks/<id>` | Deletes a task |
| GET | `/ui` | Frontend interface |

## Tech Stack

- **Python / Flask** — REST API
- **PostgreSQL / Supabase** — cloud database
- **SQLAlchemy** — ORM
- **Docker** — containerization
- **GitHub Actions** — CI/CD pipeline
- **Docker Hub** — image registry
- **pytest** — automated testing
- **python-dotenv** — environment variables

## Run locally

```bash
git clone https://github.com/georgianacucoanes/flask-docker-pipeline.git
cd flask-docker-pipeline
pip install -r requirements.txt
python app.py
```

## Run with Docker

```bash
docker pull georgianacucoanes/devops-pipeline
docker run -p 5000:5000 georgianacucoanes/devops-pipeline
```

## Pipeline status

![CI/CD](https://github.com/georgianacucoanes/flask-docker-pipeline/actions/workflows/ci-cd.yml/badge.svg)