import sqlite3
import os
from todo.models import Task
from todo.config import load_config, ensure_config


def get_db_path():
    ensure_config()
    config = load_config()
    return os.path.join(
        os.path.expanduser("~"),
        ".todo",
        f"{config['user']}.db"
    )


def get_connection():
    return sqlite3.connect(get_db_path())


def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            deadline TEXT,
            done INTEGER NOT NULL DEFAULT 0
        )
        """)


def add_task(title, priority, deadline):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO tasks (title, priority, deadline) VALUES (?, ?, ?)",
            (title, priority, deadline)
        )


def fetch_tasks(where=None, params=()):
    query = "SELECT id, title, priority, deadline, done FROM tasks"
    if where:
        query += f" WHERE {where}"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [Task(*row) for row in rows]


def mark_done(task_id):
    with get_connection() as conn:
        conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ?",
            (task_id,)
        )


def delete_task(task_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
