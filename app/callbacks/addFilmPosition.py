import logging
from app.functions.packer import unpack
from app.database import Connector


def add_film_pos_callback(ch, method, props, body, db: Connector):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    body: dict = unpack(body)
    for field in ["user_oid", "film_id", "pos"]:
        if field not in body:
            logging.error(f"Missing Field: {field}")
            return
    db.add_film_pos(body["user_oid"], body["film_id"], body['pos'])

