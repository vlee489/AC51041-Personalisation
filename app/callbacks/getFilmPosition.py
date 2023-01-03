from app.functions.packer import pack, unpack
from app.database import Connector
from pika import BasicProperties


def get_film_pos_callback(ch, method, props, body, db: Connector):
    body: dict = unpack(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    while not complete:
        for field in ["user_oid", "film_id"]:
            if field not in body:
                response["error"] = "MISSING-FIELD"
                complete = True
                continue
        film = db.get_film_pos(body["user_oid"], body["film_id"])
        if film:
            response = {
                "state": "VALID",
                "film": film.dict
            }
            complete = True
        else:
            response["error"] = "NOT-FOUND"
            complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=pack(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
