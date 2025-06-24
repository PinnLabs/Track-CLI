import json
import os

SESSIONS_PATH = "data/sessions.json"


def load_sessions():
    if not os.path.exists(SESSIONS_PATH):
        return []
    with open(SESSIONS_PATH, "r") as f:
        return json.load(f)


def save_sessions(sessions):
    os.makedirs(os.path.dirname(SESSIONS_PATH), exist_ok=True)
    with open(SESSIONS_PATH, "w") as f:
        json.dump(sessions, f, indent=4)
