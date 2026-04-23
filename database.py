import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def _load():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def _save(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def save_user(user_data):
    db = _load()
    db[user_data['email']] = user_data
    _save(db)

def fetch_user(email):
    db = _load()
    return db.get(email)
