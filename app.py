from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return jsonify({
        "message": "Student Task Manager API is running!"
    })

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return jsonify([dict(task) for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    title = data.get("title")

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task added successfully!"
    })

if __name__ == "__main__":
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    app.run(debug=True)
