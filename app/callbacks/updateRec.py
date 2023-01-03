import logging

from app.functions.packer import pack, unpack
from app.database import Connector
from pika import BasicProperties


def update_rec_callback(ch, method, props, body, db: Connector):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    body: dict = unpack(body)

    for field in ["user_oid", "tags", "categories"]:
        if field not in body:
            logging.error(f"missing field {field}")
            return

    db.update_rec(body["user_oid"], body["tags"], body["categories"])
