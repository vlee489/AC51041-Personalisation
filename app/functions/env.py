"""Loads environment vars"""
import os


class EnvVars:
    @staticmethod
    def get_with_default(key, default):
        return os.environ.get(key, default)

    @staticmethod
    def get_required(key):
        if value := os.environ.get(key, None):
            return value
        else:
            raise EnvironmentError(f"Required value {key} not found!")

    def __init__(self):
        self.debug = self.get_with_default("DEBUG", None)
        self.mq_uri = self.get_with_default("MQURI", "amqp://rabbitmq:5672")
        self.mongo_uri = self.get_required("MONGOURI")

