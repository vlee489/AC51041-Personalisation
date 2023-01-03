from app.functions.env import EnvVars
from app.database import Connector
import pika

from app.callbacks import *

env_vars = EnvVars()  # Load in environment variables
# Message Broker--------
database = Connector(env_vars.mongo_uri, "notflix")
connection = pika.BlockingConnection(pika.connection.URLParameters(env_vars.mq_uri))  # Connect to message broker
channel = connection.channel()  # creates connection channel
# Define Queues and consumer
channel.queue_declare(queue="film-pos")  # Declare Queue
channel.basic_consume(queue="film-pos", on_message_callback=lambda ch, method, properties, body:
                      get_film_pos_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-pos-update")  # Declare Queue
channel.basic_consume(queue="film-pos-update", on_message_callback=lambda ch, method, properties, body:
                      add_film_pos_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-pos-remove")  # Declare Queue
channel.basic_consume(queue="film-pos-remove", on_message_callback=lambda ch, method, properties, body:
                      remove_film_pos_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-rec")  # Declare Queue
channel.basic_consume(queue="film-rec", on_message_callback=lambda ch, method, properties, body:
                      get_rec_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-rec-update")  # Declare Queue
channel.basic_consume(queue="film-rec-update", on_message_callback=lambda ch, method, properties, body:
                      update_rec_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-history")  # Declare Queue
channel.basic_consume(queue="film-history", on_message_callback=lambda ch, method, properties, body:
                      get_watched_films_callback(ch, method, properties, body, database))
# Start application consumer
channel.start_consuming()
connection.close()
