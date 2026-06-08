from flask import Flask, jsonify,request
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key=os.getenv("APP_SECRET","default-secret")

tasks=[]

PORT=int(os.getenv("FLASK_PORT",5000))
DEBUG=os.getenv("FLASK_DEBUG","False")=="True"

@app.route("/")
def home():
    return jsonify({"message": "Hello from DevOps pipeline!", "status": "ok"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/time")
def current_time():
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"current_time":now})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks":tasks})

@app.route("/tasks",methods=['POST'])
def add_task():
    data=request.get_json()
    task=data.get("task")
    if not task:
        return jsonify({"error": "No task provided"}),400 
    new_task={
        "id":len(tasks),
        "task":task,
        "status":"pending"
    }
    tasks.append(new_task)
    return jsonify({"message": "Task added", "task": new_task}), 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task_status(task_id):
    if task_id >=len(tasks):
        return jsonify({"error": "Task not found"}), 404 
    data = request.get_json()
    status = data.get("status")
    if status not in ["pending", "done"]:
        return jsonify({"error": "Status must be 'pending' or 'done'"}), 400
    tasks[task_id]["status"] = status
    return jsonify({"message": "Task updated", "task": tasks[task_id]})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    deleted = tasks.pop(task_id)
    return jsonify({"message": "Task deleted", "task": deleted})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)