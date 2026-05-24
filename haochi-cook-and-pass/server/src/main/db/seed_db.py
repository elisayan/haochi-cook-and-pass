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

    #Ricetta
    recipes = [
        {"name": "avocado_toast", "ingredients": ["avocado", "bread"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "bacon_and_eggs", "ingredients": ["bacon", "egg"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "caprese_salad", "ingredients": ["basil", "tomato"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "grilled_cheese", "ingredients": ["bread", "cheese"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "broccoli_stir_fry", "ingredients": ["broccoli", "carrot", "onion"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "bacon_french_toast", "ingredients": ["bread", "bacon", "egg"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "pizza_margherita", "ingredients": ["pizza_pie", "tomato_soup", "mozzarella", "basil"], "difficulty": "hard", "points": 40, "time": 180}
    ]

    db.db["ingredients"].insert_many(ingredients)
    db.db["recipes"].insert_many(recipes)
    print("Database seeded with ingredients and recipes!")


if __name__ == "__main__":
    seed()