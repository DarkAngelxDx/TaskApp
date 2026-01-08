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
