import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False 
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


def create_tables():
    with app.app_context():
        db.create_all()


from flask import Flask, jsonify, request, render_template

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([t.to_dict() for t in todos])


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    todo = Todo(title=data["title"])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    todo = Todo.session.get(todo_id)
    if not todo:
        return jsonify({"error": "not found"}), 404
    data = request.get_json()
    if "done" in data:
        todo.done = data["done"]
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.session.get(todo_id)
    if not todo:
        return jsonify({"error": "not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=5000)