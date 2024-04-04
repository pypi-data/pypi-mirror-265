# Monkey patching telebot to save json messages
from telebot import types

# Override the de_json method for messages to also save a copy of input strings
types.Message._de_json = types.Message.de_json


def de_json(json_string):
    message = types.Message._de_json(json_string)
    if message:
        message.__setattr__("json", json_string)
    return message

types.Message.de_json = de_json

from .mongo_db import MongoMem
