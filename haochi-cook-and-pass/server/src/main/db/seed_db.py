from db_manager import db

def seed():
    db.connect()

    ingredients = [
        {"name": "avocado", "type": "fruit"},
        {"name": "bacon", "type": "protein"},
        {"name": "basil", "type": "herb"},
        {"name": "bread", "type": "grain"},
        {"name": "broccoli", "type": "vegetable"},
        {"name": "carrot", "type": "vegetable"},
        {"name": "chili", "type": "spice"},
        {"name": "cobb", "type": "vegetable"},
        {"name": "egg", "type": "protein"},
        {"name": "fish", "type": "protein"},
        {"name": "fried_egg", "type": "protein"},
        {"name": "lemon", "type": "fruit"},
        {"name": "mushroom", "type": "vegetable"},
        {"name": "nachos", "type": "grain"},
        {"name": "onion", "type": "vegetable"},
        {"name": "orange", "type": "fruit"},
        {"name": "peas", "type": "vegetable"},
        {"name": "pizza_pie", "type": "grain"},
        {"name": "raw_shrimp", "type": "seafood"},
        {"name": "rice", "type": "grain"},
        {"name": "salad", "type": "vegetable"},
        {"name": "shrimp", "type": "seafood"},
        {"name": "tomato_soup", "type": "vegetable"},
        {"name": "tomato", "type": "vegetable"}
    ]

    db.db["ingredients"].insert_many(ingredients)
    print("Database seeded with ingredients!")

if __name__ == "__main__":
    seed()