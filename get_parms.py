import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def base_parse(key):
    token = os.environ.get(key, None)
    if token is None:
        print(f"{key} :", None, "*"*20)
    return token


def bot_token():
    return base_parse(key="BOT_TOKEN")


def openai_key():
    return base_parse(key="OPENAI_KEY")

import json
import time

class JSONAppender:
    def __init__(self, file_path):
        self.file_path = file_path

    def insert_one(self, data):
        # Read existing data from the file
        existing_data = self._read_json_file()

        # Append new data to existing data
        existing_data["questions"].append(data)

        # Write the updated data back to the file
        self._write_json_file(existing_data)

    def _read_json_file(self):
        try:
            with open(self.file_path, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {"questions":[]}
        
        return existing_data

    def _write_json_file(self, data):
        json.dump(data, open(self.file_path, "w"))
    
    def close(self,):
        pass


def mongo_collection():
    db_name = os.environ.get("DB_NAME", "database")
    quizzes_collection = os.environ.get("COLLECTION_NAME", "collection")
    mongodb_host = os.environ.get("MONGODB_HOST", None)
    client = MongoClient(
        host=mongodb_host
    )
    try:
        # Check if the client is connected
        connected = client.server_info()  # This will trigger an exception if not connected
        print('MongoDB client connected:\n', connected)
        db = client[db_name]
        collection = db[quizzes_collection]
    except Exception as e:
        print('Failed to connect to MongoDB:', e)
        client.close()
        collection = JSONAppender("data/questions.json")
    return collection

if __name__ == "__main__":
    mongo_collection()