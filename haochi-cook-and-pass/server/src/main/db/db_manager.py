from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Sostituisci <db_password> con la password corretta
URI = "mongodb+srv://elisayan811_db_user:<>@haochi.dtglmg1.mongodb.net/?appName=haochi"

class DBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(URI, server_api=ServerApi('1'))
            self.db = self.client["haochi_db"] 
            # Ping di controllo
            self.client.admin.command('ping')
            print("Database collegato correttamente!")
        except Exception as e:
            print(f"Errore di connessione al DB: {e}")

    def get_random_ingredient(self):
        pipeline = [{"$sample": {"size": 1}}]
        cursor = self.db["ingredients"].aggregate(pipeline)
        
        results = list(cursor)
        if results:
            return results[0]["name"]
        return None
        


db = DBManager()