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


def mongo_collection():
    db_name = os.environ.get("DB_NAME", "database")
    quizzes_collection = os.environ.get("COLLECTION_NAME", "collection")
    client = MongoClient()
    db = client[db_name]
    collection = db[quizzes_collection]
    return collection
