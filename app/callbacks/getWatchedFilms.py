from app.functions.packer import pack, unpack
from app.database import Connector
from pika import BasicProperties


def get_watched_films_callback(ch, method, props, body, db: Connector):
    body: dict = unpack(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    while not complete:
        if "user_oid" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        films = db.get_to_continue_films(body["user_oid"], limit=4)
        if films:
            response = {
                "state": "VALID",
                "films": [f.dict for f in films]
            }
            complete = True
        else:
            response = {
                "state": "VALID",
                "films": []
            }
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=pack(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
