import flask
import model
import json_file_database

app = flask.Flask(__name__)


@app.route("/api/messages/<recipient>", methods=["GET", "POST", "PUT", "DELETE"])
def messages(recipient):
    try:
        request = flask.request
        query_args = request.args

        db = json_file_database.JsonFileDatabase("messages_db.json")
        message_model = model.Model(db)

        if request.method == "POST":
            message = request.form["message"]
            message_model.add_message(recipient, message)
            return flask.Response(status=201)

        elif request.method == "PUT":
            result = message_model.get_unread_messages_by_recipient_id(recipient)
            return flask.jsonify(result)

        elif request.method == "DELETE":
            request = flask.request
            indexes_to_remove = request.args.getlist("index", type=int)

            remaining_messages = message_model.delete_messages(recipient, indexes_to_remove)
            return flask.jsonify(remaining_messages)

        else:
            start_index = query_args.get("start")
            stop_index = query_args.get("stop")

            if start_index is not None:
                start_index = int(start_index)
            if stop_index is not None:
                stop_index = int(stop_index)

            result = message_model.get_messages_by_index(recipient, start_index, stop_index)
            return flask.jsonify(result)

    except KeyError:
        flask.abort(400)

    except IndexError:
        flask.abort(404)


if __name__ == '__main__':
    app.run(port=5000)