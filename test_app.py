import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    tasks.clear()
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_time(client):
    response = client.get("/time")
    assert response.status_code == 200
    assert "current_time" in response.json

def test_add_task(client):
    response = client.post("/tasks", json={"task": "Learn DevOps"})
    assert response.status_code == 201
    assert response.json["task"]["status"] == "pending"

def test_get_tasks(client):
    client.post("/tasks", json={"task": "Learn DevOps"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json["tasks"]) == 1

def test_update_task(client):
    client.post("/tasks", json={"task": "Learn DevOps"})
    response = client.patch("/tasks/0", json={"status": "done"})
    assert response.status_code == 200
    assert response.json["task"]["status"] == "done"

def test_delete_task(client):
    client.post("/tasks", json={"task": "Learn DevOps"})
    response = client.delete("/tasks/0")
    assert response.status_code == 200
    assert response.json["task"]["task"] == "Learn DevOps"