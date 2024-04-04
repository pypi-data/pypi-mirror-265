import logging


# Abstract class for MemDB with different Backend
class MemDB:
    def __init__(self, *args, **kwargs):
        pass

    def insert_message(self, message):
        logging.error("Not implemented")

    def get_message(self, message_id):
        logging.error("Not implemented")

    def validate(self):
        logging.error("Not implemented")
