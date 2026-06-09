# devops_pipeline
Think of a flask application as a restaurant : 

flask app= the kitchen 
endpoint= the serving window(each window serves something different)
request=your order
response=what you get back

Every time you type a URL in your browser , you re making a request to a specific endpoint, and the server sends back a response.

Each @app.route(...) in the code defines one of those windows:
/   -> "Hello, the server is running"
/health  ->"Yes, I'm up an healthy"
/time -> "Current time iss 14:32:05"
/tasks -> "Here are your tasks" (GET) or "Task added!"(Post) . The difference between get and post is that get is used when you re asking for something and post is used when you're senfing something
# DevOps CI/CD Pipeline

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

## Tech Stack

- **Python** / **Flask** — REST API
- **Docker** — containerization
- **GitHub Actions** — CI/CD pipeline
- **Docker Hub** — image registry
- **pytest** — automated testing

## Run locally

```bash
git clone https://github.com/georgianacucoanes/devops-pipeline.git
cd devops-pipeline
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
