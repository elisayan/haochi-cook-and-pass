from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = "mongodb+srv://elisayan811_db_user:<db_password>@haochi.dtglmg1.mongodb.net/?appName=haochi"

class DBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(URI, server_api=ServerApi('1'))
            # Sostituisci "haochi_db" con il nome che vuoi dare al tuo DB
            self.db = self.client["haochi_db"] 
            # Ping di controllo
            self.client.admin.command('ping')
            print("Database collegato correttamente!")
        except Exception as e:
            print(f"Errore di connessione al DB: {e}")

    def get_random_ingredient(self, exclude_ids):
        pass


db = DBManager()