from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []
next_id = 1


@app.route("/")
def index():
    return jsonify({"message": "Todo API is running"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)


@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    todo = {"id": next_id, "title": data["title"], "done": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "not found"}), 404
    data = request.get_json()
    if "done" in data:
        todo["done"] = data["done"]
    return jsonify(todo)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)