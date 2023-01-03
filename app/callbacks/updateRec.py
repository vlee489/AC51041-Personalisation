import logging

from app.functions.packer import pack, unpack
from app.database import Connector
from pika import BasicProperties


def update_rec_callback(ch, method, props, body, db: Connector):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    body: dict = unpack(body)
    complete = False

    while not complete:
        for field in ["user_oid", "tags", "categories"]:
            if field not in body:
                logging.error(f"missing field {field}")
                complete = True
                continue
        db.update_rec(body["user_oid"], body["tags"], body["categories"])
