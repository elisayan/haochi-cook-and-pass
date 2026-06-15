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
        {"name": "fish", "type": "protein"},
        {"name": "fried_egg", "type": "protein"},
        {"name": "lemon", "type": "fruit"},
        {"name": "mozzarella", "type": "dairy"},
        {"name": "mushroom", "type": "vegetable"},
        {"name": "nachos", "type": "grain"},
        {"name": "onion", "type": "vegetable"},
        {"name": "orange", "type": "fruit"},
        {"name": "peas", "type": "vegetable"},
        {"name": "pizza_pie", "type": "grain"},
        {"name": "rice", "type": "grain"},
        {"name": "salad", "type": "vegetable"},
        {"name": "shrimp", "type": "seafood"},
        {"name": "tomato_soup", "type": "vegetable"},
        {"name": "tomato", "type": "vegetable"}
    ]

    recipes = [
        # EASY (2 ingredienti, points: 20)
        {"name": "avocado_toast", "ingredients": ["bread", "avocado"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "bacon_and_eggs", "ingredients": ["bacon", "fried_egg"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "caprese_salad", "ingredients": ["basil", "tomato"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "grilled_egg", "ingredients": ["bread", "fried_egg"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "shrimp_lemon", "ingredients": ["shrimp", "lemon"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "nachos_chili", "ingredients": ["nachos", "chili"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "rice_and_peas", "ingredients": ["rice", "peas"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "mushroom_salad", "ingredients": ["mushroom", "salad"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "carrot_salad", "ingredients": ["carrot", "salad"], "difficulty": "easy", "points": 20, "time": 60},
        {"name": "tomato_soup_basil", "ingredients": ["tomato_soup", "basil"], "difficulty": "easy", "points": 20, "time": 60},

        # MEDIUM (3 ingredienti, points: 30)
        {"name": "broccoli_stir_fry", "ingredients": ["broccoli", "carrot", "onion"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "fish_and_salad", "ingredients": ["fish", "salad", "lemon"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "nachos_platter", "ingredients": ["nachos", "chili", "avocado"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "mushroom_omelette", "ingredients": ["egg", "mushroom", "onion"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "raw_shrimp_cobb", "ingredients": ["raw_shrimp", "cobb", "lemon"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "mozzarella_tomato_toast", "ingredients": ["bread", "mozzarella", "tomato"], "difficulty": "medium", "points": 30, "time": 120},
        {"name": "broccoli_rice", "ingredients": ["broccoli", "rice", "carrot"], "difficulty": "medium", "points": 30, "time": 120},

        # HARD (4+ ingredienti, points: 40)
        {"name": "pizza_margherita", "ingredients": ["pizza_pie", "tomato_soup", "mozzarella", "basil"], "difficulty": "hard", "points": 40, "time": 180},
        {"name": "fish_tacos", "ingredients": ["fish", "avocado", "chili", "lemon", "salad"], "difficulty": "hard", "points": 40, "time": 180},
        {"name": "shrimp_stir_fry", "ingredients": ["shrimp", "broccoli", "onion", "rice"], "difficulty": "hard", "points": 40, "time": 180},
        {"name": "full_breakfast", "ingredients": ["bread", "bacon", "fried_egg", "mushroom", "tomato"], "difficulty": "hard", "points": 40, "time": 180},
        {"name": "cobb_salad", "ingredients": ["cobb", "bacon", "egg", "avocado", "tomato"], "difficulty": "hard", "points": 40, "time": 180},
        {"name": "spicy_rice_bowl", "ingredients": ["rice", "chili", "onion", "peas", "carrot"], "difficulty": "hard", "points": 40, "time": 180},
        {"name": "seafood_platter", "ingredients": ["shrimp", "raw_shrimp", "fish", "lemon"], "difficulty": "hard", "points": 40, "time": 180},
    ]

    db.db["ingredients"].insert_many(ingredients)
    db.db["recipes"].insert_many(recipes)
    print("Database seeded with ingredients and recipes!")


if __name__ == "__main__":
    seed()