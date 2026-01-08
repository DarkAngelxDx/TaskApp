import os
from todo.config import load_config, save_config, ensure_config

BASE_DIR = os.path.join(os.path.expanduser("~"), ".todo")


def list_users():
    ensure_config()
    return [f.replace(".db", "") for f in os.listdir(BASE_DIR) if f.endswith(".db")]


def switch_user(name):
    config = load_config()
    config["user"] = name
    save_config(config)


def create_user(name):
    path = os.path.join(BASE_DIR, f"{name}.db")
    if not os.path.exists(path):
        open(path, "a").close()
