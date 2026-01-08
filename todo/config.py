import os
import tomllib
import tomli_w

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".todo")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")

DEFAULT_CONFIG = {
    "user": "default",
    "date_format": "%Y-%m-%d"
}


def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(DEFAULT_CONFIG, f)


def load_config():
    ensure_config()
    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def save_config(config):
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)
