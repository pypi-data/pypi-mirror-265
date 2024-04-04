import json

from telebot_mem.db import MemDB

from pymongo import MongoClient
from telebot.types import Message


class MongoMem(MemDB):
    def __init__(self, connecion_string, db_name):
        self.client = MongoClient(connecion_string)[db_name]

    def insert_message(self, message: Message):
        if message and message.json:
            obj = message.json
            obj.update({"_id": f"{message.chat.id}_{message.message_id}"})
            self.client.messages.insert_one(obj)

    def get_message(self, message_id):
        return self.client.messages.find_one({"_id": message_id})

    def get_last_message(self):
        return self.client.messages.find_one({"deleted": {"$ne": True}}, sort=[("_id", -1)])
    
    def get_all_message_for_chat(self, chat_id):
        return self.client.messages.find({"chat.id": chat_id, "deleted": {"$ne": True}})
    
    def mark_delete(self, chat_id):
        self.client.messages.update_many({"chat.id": chat_id}, {"$set": {"deleted": True}})

    def validate(self):
        # check message collection exists
        return "messages" in self.client.list_collection_names()

    # decorator methods
    def memorize(self, func):
        def wrapper(*args, **kwargs):
            self.insert_message(args[0] if args else kwargs["message"])
            func(*args, **kwargs)

        return wrapper
