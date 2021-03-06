# Simple Python message service

This is a simple Python/Flask REST API for a message service that supports sending, retrieving and deleting messages. 

## Setup instructions

1. Run `pip install -r requirements.txt` to install dependencies. 
3. Run `python app.py` to start the service. 
4. The service will now run on http://localhost:5000

## How to use the API

### Send message

Send message to recipient. 

URL: `/api/messages/{recipient}`

Method: `POST`

Form params: 

    "message": "[text message, required]"
    
Curl example: 

    curl --location --request POST 'localhost:5000/api/messages/112' \
    --form 'message=SOS'

Success Response: `200 Created`

Error Response: 

* `400 Bad request` if missing valid text message


### Retrieve new unread messages

Retrieve all unread messages for recipient and mark them as read. 

URL: `/api/messages/{recipient}`

Method: `PUT`

Curl example: 

    curl --location --request PUT 'localhost:5000/api/messages/112'

Success Response: `200 OK`

    [
        {
            "index": 0,
            "message": "SOS",
            "read": true,
            "timestamp": "2020-04-23 22:09:13"
        }
    ]

Error Response: 

* `400 Bad request` if invalid recipient


### Delete messages

Delete one or more message for recipient. Returns a list of remaining messages for recipient. 

URL: `/api/messages/{recipient}`

Method: `DELETE`

Query parameters

    "index": "[index for message, required]"

Curl example: 

    curl --location --request DELETE 'localhost:5000/api/messages/112?index=0&index=2'

Success Response: `200 OK`

    [
        {
            "index": 0,
            "message": "SOS",
            "read": true,
            "timestamp": "2020-04-23 22:09:13"
        }
    ]

Error Response: 

* `400 Bad request` if index is not specified in query or invalid recipient
* `404 Not found`  if index does not exist


### Retrieve messages by index

Retrieve messages for recipient for start and/or end index or all messages if no index is specified

URL: `/api/messages/{recipient}`

Method: `GET`

Query parameters

        "start": "[start index for messages, optional]",
        "stop": "[stop index for messages, optional]"

Curl example: 

    curl --location --request GET 'localhost:5000/api/messages/112?start=0&stop=1'

Success Response: `200 OK`

    [
        {
            "index": 1,
            "message": "The tiger ate my family",
            "read": false,
            "timestamp": "2020-04-23 22:23:50"
        },
        {
            "index": 0,
            "message": "SOS",
            "read": true,
            "timestamp": "2020-04-23 22:09:13"
        }
    ]

Error Response: 

* `400 Bad request` if index is not specified in query or invalid recipient
* `404 Not found` if index does not exist
