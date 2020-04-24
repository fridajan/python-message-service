import json


class Database:
    def __init__(self, filename):
        self.db_file = filename
        self.data = self.load_db()

    def load_db(self):
        with open(self.db_file) as file:
            return json.load(file)

    def save_changes(self, new_data):
        with open(self.db_file, "w") as file:
            json.dump(new_data, file)
            self.data = new_data

    def append(self, value):
        db = self.load_db()
        db.append(value)
        with open(self.db_file, "w") as file:
            json.dump(db, file)
            self.data = db

    # db_file = "messages_db.json"
    # data = load_db()
