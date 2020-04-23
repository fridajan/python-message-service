import json


def load_db():
    with open("messages_db.json") as file:
        return json.load(file)


def save_changes(new_data):
    with open("messages_db.json", "w") as file:
        json.dump(new_data, file)


def append(value):
    db = load_db()
    db.append(value)
    with open("messages_db.json", "w") as file:
        json.dump(db, file)
        global data
        data = db


data = load_db()