import datetime


class Model:
    def __init__(self, database):
        self.db = database

    def get_unread_messages_by_recipient_id(self, recipient_id):
        existing_recipient = self.get_recipient(recipient_id)
        if existing_recipient:
            unread_messages = self.get_unread_messages(existing_recipient["messages"])

            for m in unread_messages:
                m["read"] = True
            self.db.save_changes(self.db.data)

            result = self.sort_messages_by_desc_date(unread_messages)
            result = self.add_index(result, existing_recipient["messages"])

            return result
        return KeyError

    @staticmethod
    def get_unread_messages(messages):
        return [message for message in messages if not message["read"]]

    def get_messages_by_index(self, recipient_id, start_index, stop_index):
        existing_recipient = self.get_recipient(recipient_id)
        if existing_recipient:
            messages = existing_recipient["messages"]
            if stop_index is not None:
                stop_index += 1

            result = self.sort_messages_by_desc_date(messages[start_index:stop_index])
            result = self.add_index(result, existing_recipient["messages"])
            return result
        return KeyError

    @staticmethod
    def sort_messages_by_desc_date(messages):
        return sorted(messages, key=lambda x: datetime.datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"), reverse=True)

    @staticmethod
    def add_index(subset, data):
        for x in subset:
            x["index"] = data.index(x)
        return subset

    def add_message(self, recipient_id, message):
        existing_recipient = self.get_recipient(recipient_id)
        if existing_recipient:
            existing_recipient["messages"].append(self.create_message_json(message))
            self.db.save_changes(self.db.data)
        else:
            self.db.append({"recipient_id": recipient_id, "messages": [self.create_message_json(message)]})

    def get_recipient(self, recipient_id):
        return next((x for x in self.db.data if x["recipient_id"] == recipient_id), None)

    @staticmethod
    def create_message_json(message):
        return {"message": message, "read": False, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    def delete_messages(self, recipient_id, indexes_to_remove):
        existing_recipient = self.get_recipient(recipient_id)
        if existing_recipient:
            messages = existing_recipient["messages"]

            indexes_to_remove.sort(reverse=True)
            for i in indexes_to_remove:
                messages.pop(i)

            self.db.save_changes(self.db.data)
            return self.get_messages_by_index(recipient_id, None, None)
        return KeyError

