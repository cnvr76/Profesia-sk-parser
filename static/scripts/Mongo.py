from pymongo import MongoClient
from urllib.parse import quote
import os

class Mongo:
    def __init__(self):
        self._password = quote(os.getenv("MONGO_DB_PASSWORD"))
        self._uri = f"mongodb+srv://cnvr76:{self._password}@profesiask.qxbih.mongodb.net/?retryWrites=true&w=majority&appName=Profesiask"
        self.client = MongoClient(self._uri)
        self.db = self.client["profesiask"]

        self.vacancies_collection = self.db["Vacancies"]

    def create():
        ...