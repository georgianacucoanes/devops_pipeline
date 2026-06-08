from flask import Flask, jsonify, request
from datetime import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
import logging

load_dotenv()

# configurare logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET", "default-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

PORT = int(os.getenv("FLASK_PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"

# modelul bazei de date
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="pending")

    def to_dict(self):
        return {"id": self.id, "task": self.task, "status": self.status}

with app.app_context():
    db.create_all()
    logger.info("Database tables created")

@app.route("/")
def home():
    logger.info("Home endpoint called")
    return jsonify({"message": "Hello from DevOps pipeline!", "status": "ok"})

@app.route("/health")
def health():
    logger.info("Health check called")
    return jsonify({"status": "healthy"})

@app.route("/time")
def current_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Time endpoint called - returned {now}")
    return jsonify({"current_time": now})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    logger.info(f"Get tasks called - {len(tasks)} tasks in database")
    return jsonify({"tasks": [t.to_dict() for t in tasks]})

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")
    if not task:
        logger.warning("Add task called with no task provided")
        return jsonify({"error": "No task provided"}), 400
    new_task = Task(task=task)
    db.session.add(new_task)
    db.session.commit()
    logger.info(f"Task added: {task}")
    return jsonify({"message": "Task added", "task": new_task.to_dict()}), 201

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        logger.warning(f"Task {task_id} not found")
        return jsonify({"error": "Task not found"}), 404
    logger.info(f"Get task {task_id} called")
    return jsonify({"task": task.to_dict()})

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task_status(task_id):
    task = Task.query.get(task_id)
    if not task:
        logger.warning(f"Update called on non-existent task {task_id}")
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    status = data.get("status")
    if status not in ["pending", "done"]:
        logger.warning(f"Invalid status provided: {status}")
        return jsonify({"error": "Status must be 'pending' or 'done'"}), 400
    task.status = status
    db.session.commit()
    logger.info(f"Task {task_id} status updated to {status}")
    return jsonify({"message": "Task updated", "task": task.to_dict()})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        logger.warning(f"Delete called on non-existent task {task_id}")
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    logger.info(f"Task {task_id} deleted")
    return jsonify({"message": "Task deleted", "task": task.to_dict()})

if __name__ == "__main__":
    logger.info(f"Starting app on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)