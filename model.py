import datetime
import db


def get_unread_messages_by_recipient_id(recipient_id):
    existing_recipient = get_recipient(recipient_id)
    if existing_recipient:
        unread_messages = get_unread_messages(existing_recipient["messages"])

        for m in unread_messages:
            m["read"] = True
        db.save_changes(db.data)

        result = sort_messages_by_desc_date(unread_messages)
        result = add_index(result, existing_recipient["messages"])

        return result
    return KeyError


def get_unread_messages(messages):
    return [message for message in messages if not message["read"]]


def get_messages_by_index(recipient_id, start_index, stop_index):
    existing_recipient = get_recipient(recipient_id)
    if existing_recipient:
        messages = existing_recipient["messages"]
        if stop_index is not None:
            stop_index += 1

        result = sort_messages_by_desc_date(messages[start_index:stop_index])
        result = add_index(result, existing_recipient["messages"])
        return result
    return KeyError


def sort_messages_by_desc_date(messages):
    return sorted(messages, key=lambda x: datetime.datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"), reverse=True)


def add_index(subset, data):
    for x in subset:
        x["index"] = data.index(x)
    return subset


def add_message(recipient_id, message):
    existing_recipient = get_recipient(recipient_id)
    if existing_recipient:
        existing_recipient["messages"].append(create_message_json(message))
        db.save_changes(db.data)
    else:
        db.append({"recipient_id": recipient_id, "messages": [create_message_json(message)]})


def get_recipient(recipient_id):
    return next((x for x in db.data if x["recipient_id"] == recipient_id), None)


def create_message_json(message):
    return {"message": message, "read": False, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


def delete_messages(recipient_id, indexes_to_remove):
    existing_recipient = get_recipient(recipient_id)
    if existing_recipient:
        messages = existing_recipient["messages"]

        indexes_to_remove.sort(reverse=True)
        for i in indexes_to_remove:
            messages.pop(i)

        db.save_changes(db.data)
        return get_messages_by_index(recipient_id, None, None)
    return KeyError
