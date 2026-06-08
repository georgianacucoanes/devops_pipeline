import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

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
    tasks = client.get("/tasks").json["tasks"]
    task_id = tasks[0]["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json["task"]["status"] == "done"

def test_delete_task(client):
    client.post("/tasks", json={"task": "Learn DevOps"})
    tasks = client.get("/tasks").json["tasks"]
    task_id = tasks[0]["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200