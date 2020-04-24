import unittest
import model
import json_file_database


class TestSum(unittest.TestCase):
    def setUp(self):
        self.mock_database = json_file_database.JsonFileDatabase("test_messages_db.json")
        self.mock_database.save_changes([])
        self.model = model.Model(self.mock_database)

    def tearDow(self):
        self.mock_database.save_changes([])

    def test_adding_message_for_new_recipient(self):
        self.model.add_message("new_recipient", "A message")

        result = self.model.get_recipient("new_recipient")
        messages = result["messages"]

        self.assertEqual(len(messages), 1, "Should store one message")
        self.assertEqual(messages[0]["message"], "A message", "Should store message")

    def test_adding_message_for_existing_recipient(self):
        self.model.add_message("existing_recipient", "old_message")

        self.model.add_message("existing_recipient", "new_message")

        result = self.model.get_recipient("existing_recipient")
        messages = result["messages"]

        self.assertEqual(len(messages), 2, "Should append new message to existing list")

    def test_retrieving_messages_with_index(self):
        self.mock_database.save_changes(test_data)

        result = self.model.get_messages_by_index("recipient", 0, 0)
        message = result[0]

        self.assertEqual(message["message"], "oldest message", "Should return message")
        self.assertEqual(message["index"], 0, "Should return index")

    def test_retrieving_messages_without_specifying_index(self):
        self.mock_database.save_changes(test_data)

        result = self.model.get_messages_by_index("recipient", None, None)
        first_message = result[0]
        second_message = result[1]

        self.assertEqual(len(result), 2, "Should return all messages")
        self.assertEqual(first_message["message"], "newest message",
                         "Should return newest message first")
        self.assertEqual(second_message["message"], "oldest message",
                         "Should return oldest message last")

    def test_retrieving_unread_messages(self):
        self.model.add_message("recipient", "unread message")

        result = self.model.get_unread_messages_by_recipient_id("recipient")
        message = result[0]

        self.assertEqual(len(result), 1, "Should return one message")
        self.assertEqual(message["read"], True, "Should mark message as read")

    def test_deleting_message(self):
        self.model.add_message("existing_recipient", "first message")
        self.model.add_message("existing_recipient", "second message")

        result = self.model.delete_messages("existing_recipient", [0])
        remaining_message = result[0]

        self.assertEqual(len(result), 1, "Should return one remaining message")
        self.assertEqual(remaining_message["message"], "second message", "Should return remaining message")


test_data = [
    {
        "recipient_id": "recipient",
        "messages": [
            {
                "message": "oldest message",
                "read": True,
                "timestamp": "2020-04-23 22:00:00"
            },
            {
                "message": "newest message",
                "read": False,
                "timestamp": "2020-04-24 22:00:00"
            }
        ]
    }
]

if __name__ == '__main__':
    unittest.main()
