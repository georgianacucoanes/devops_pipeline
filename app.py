from flask import Flask, jsonify,request
from datetime import datetime

app = Flask(__name__)
tasks=[]

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
    tasks.append(task)
    return jsonify({"message": "Task added", "task": task}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)