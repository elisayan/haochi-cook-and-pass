import json
import random

from .db.db_manager import db
from .connection_manager import manager
from .room_manager import RoomManager
from .room import Room, RoomState

room_manager = RoomManager()
levels_setting = {"level_0": {"easy": 2, "medium": 1, "hard": 0},
                   "level_1": {"easy": 2, "medium": 2, "hard": 0},
                   "level_2": {"easy": 1, "medium": 2, "hard": 1}
                 }

'''Method to create a new game for a player'''
async def handle_start_game(websocket, current_player, data):
    room = room_manager.create_room() 
    game_code = room.code
    
    current_player.room_code = game_code
    random_ingredient = db.get_random_ingredient()

    if random_ingredient:
        current_player.ingr_id = random_ingredient
        print(f"Player {current_player.id} assigned ingredient: {current_player.ingr_id}")
    else:
        print("No ingredients found in the database.")
        current_player.ingr_id = "shrimp"  # Default ingredient if DB is empty

    room.add_player(current_player)
    print(f"Giocatori nella room dopo la creazione:", [player.id for player in room.players.values()])
    print(f"DEBUG: id del giocatore che ha creato la room è: {current_player.ingr_id}")
    #Send message to change the state to LOBBY
    response = json.dumps({
        "action": "ROOM_CREATED", 
        "code": game_code, 
        "player_id": current_player.id
    })
    await websocket.send(response)

    #Send message to update LOBBY interface (now it has only the starting player)
    response = json.dumps({
            "action": "UPDATE_CURRENT_PLAYERS", 
            "players_id": [current_player.ingr_id],
            "is_starting_player": True
        })
    await websocket.send(response)

    
    '''await manager.broadcast(json.dumps({
        "action": "PLAYER_READY", 
        "player_id": current_player.id
    }), exclude=websocket)'''

#Quando un nuovo giocatore si aggiunge alla partita:
# - La sua interfaccia deve passare a LOBBY_STATE con is_starting_player a False
# - Si deve aggiungere il giocatore alla room
# - Si deve creare un nuovo ingr_id per l'utente che sia diverso da tutti quelli già presenti (ogni volta si prende da DB)
# - Si deve avvisare l'host della room che si è unito un nuovo giocatore
'''Method to add a new player in an existing playing room'''
async def handle_join_room(websocket, current_player, data):
    game_code = data.get("code")
    room = room_manager.get_room(game_code)

    if room is None:
        await websocket.send(json.dumps({"action": "ERROR", "message": "Room not found"}))
        return

    taken_ids = [player.ingr_id for player in room.players.values()]

    found_unique = False
    attempts = 0
    max_attempts = 20
    
    assigned_ingr = "chili" # default ingredient id

    while not found_unique and attempts < max_attempts:
        random_candidate = db.get_random_ingredient()
        
        if random_candidate not in taken_ids:
            assigned_ingr = random_candidate
            found_unique = True
        
        attempts += 1

    current_player.ingr_id = assigned_ingr
    room.add_player(current_player)

    #Messaggio inviato al giocatore che ha preso parte ad una room per farlo passare a LobbyState
    print(f"DEBUG: id del giocatore aggiunto è: {current_player.ingr_id}")
    current_player_response = json.dumps({
        "action": "CHANGE_MODEL_STATE", 
        "current_state": "AWAIT_JOIN",
        "ingr_id": current_player.ingr_id 
    }) 
    await websocket.send(current_player_response)

    all_taken_ids = [p.ingr_id for p in room.players.values()]
    host_player = room.players.get(room.host_id)
    print(f"Host player id: {host_player.id}, Host player ingr_id: {host_player.ingr_id}")#debug
    if host_player:
        await host_player.websocket.send(json.dumps({
            "action": "UPDATE_CURRENT_PLAYERS", 
            "players_id": all_taken_ids,
            "is_starting_player": True
        }))

async def handle_quit_room(websocket, current_player, data):        

    #modificato in modo che se esce l'host allora la stanza venga chiusa 
    # e tutti i giocatori vengano riportati al menu, 
    #altrimenti se esce un giocatore qualsiasi allora venga 
    #rimosso dalla stanza e venga notificato l'host 
    #per aggiornare la lista ingredienti/posizioni dei giocatori rimasti
    room = room_manager.get_room(current_player.room_code)

    if not room:
        print(f"Room with code {current_player.room_code} not found.")
        return

    print("Host ID:", room.host_id)  # Debug: stampa l'ID dell'host
    print("Current Player ID:", current_player.id)  # Debug: stampa l'ID
    
    is_host_leaving = (current_player.id == room.host_id)

    if room.state == RoomState.IN_GAME:
        # redistribuisce ingredienti, notifica gli altri, gestisce fine partita
        await handle_player_disconnect(current_player, current_player.id)
        # se la room esiste ancora (non è stata rimossa da handle_player_disconnect)
        # aggiorna l'host con il primo giocatore rimasto
        remaining_room = room_manager.get_room(current_player.room_code)
        if remaining_room and remaining_room.players:
            remaining_room.host_id = next(iter(remaining_room.players.keys()))
        current_player_response = json.dumps({
            "action": "CHANGE_MODEL_STATE",
            "current_state": "MENU",
        })
        await websocket.send(current_player_response)
        return

    if is_host_leaving:
        print(f"Host player {current_player.id} is leaving the room.")
        response = json.dumps({
            "action": "ROOM_CLOSED",
            "message": "The host has left. Room is now closed."
        })

        for player in room.players.values():
                if player.id != current_player.id:
                    await player.websocket.send(response)
        print(f"Room {room.code} closed due to host leaving.")

        room_manager.remove_room(room.code)
    else:
        room.remove_player(current_player.id)
        print(f"Player {current_player.id} left. Remaining: {len(room.players)}")

        # Notifica l'host rimasto per aggiornare la lista ingredienti/posizioni
        host_player = room.players.get(room.host_id)
        if host_player:
            taken_ids = [p.ingr_id for p in room.players.values()]
            await host_player.websocket.send(json.dumps({
                "action": "UPDATE_CURRENT_PLAYERS", 
                "players_id": taken_ids,
                "is_starting_player": True
            }))

    current_player_response = json.dumps({
        "action": "CHANGE_MODEL_STATE", 
        "current_state": "MENU",
    }) 
    await websocket.send(current_player_response)
    
#Quando il giocatore che ha avviato la partita clicca START nella LOBBY:
# - Si setta la posizione dei giocatori a quella ricevuta dal messaggio
# - Si fa cambiare lo stato del model a tutti i giocatori in PLAYING 
async def handle_start_playing(websocket, current_player, data):
    print(f"DEBUG: Ricevuto ordine posizioni: {data.get('players_position')}")
    room = room_manager.get_room(current_player.room_code)
    room.set_players_position_in_play(data.get("players_position"))
    room.set_in_game()
    #Si cambia lo stato di tutti i giocatori in PLAYING tutti i giocatori
    ws_players_in_game = []
    for player in room.players.values():
        ws_players_in_game.append(player.websocket)
    await manager.broadcast(json.dumps({
        "action": "CHANGE_MODEL_STATE", 
        "current_state": "PLAYING",
    }), include_only=ws_players_in_game)
    await handle_start_level(websocket, current_player, data)

#Quando si inizia un nuovo livello:    
# - Si distribuiscono i piatti da completare ai giocatori attraverso STARTING_RECIPES
# - Si distribuiscono tutti gli ingredienti dei piatti tra i vari giocatori attraverso messaggio STARTING_INGREDIENTS    
async def handle_start_level(websocket, current_player, data):
    room = room_manager.get_room(current_player.room_code)
    level_setting = levels_setting[f"level_{room.curr_level}"]
    if level_setting:
        shared_ingredients_in_play = [] #lista di ingredienti che il server deve distribuire tra i giocatori
        #Per ogni giocatore si estraggono dal db le ricette che deve comporre
        for player in room.players.values(): 
            player_recipes = [] 
            for difficulty in ["easy", "medium", "hard"]:
                number_rec = level_setting[difficulty]
                if number_rec > 0:
                    #tornata lista di ricette
                    recipes = db.get_random_recipes_by_difficulty(difficulty, number_rec)
                    player_recipes.extend(recipes)
                    for recipe in recipes:
                        shared_ingredients_in_play.extend(recipe["ingredients"])
            
            random.shuffle(player_recipes)
            current_player_recipes_msg = json.dumps({
            "action": "STARTING_RECIPES", 
            "recipes": player_recipes,
            }) 
            await player.websocket.send(current_player_recipes_msg)   
            print(f"inviato al giocatore {player.ingr_id} le ricette {player_recipes}")     

        # si procede distribuendo a tutti i giocatori gli ingredienti 
        random.shuffle(shared_ingredients_in_play)
        num_players = len(room.players)
        
        weights = [random.uniform(0.5, 1.5) for _ in range(num_players)]
        total_weight = sum(weights)
        start_index = 0
        players = list(room.players.values())
        for i, player in enumerate(players):
            # se è l'ultimo giocatore prende tutto il resto
            if i == num_players - 1:
                player_ingredients = shared_ingredients_in_play[start_index:]
            else:
                # calcola quanti ingredienti spettano in base al peso
                count = round(len(shared_ingredients_in_play) * (weights[i] / total_weight))
                count = max(1, count)  # almeno 1 ingrediente a testa
                end_index = min(start_index + count, len(shared_ingredients_in_play))
                player_ingredients = shared_ingredients_in_play[start_index:end_index]
                start_index = end_index

            random.shuffle(player_ingredients)
            player.initial_ingredients = player_ingredients.copy()
            player.current_ingredients = player_ingredients.copy()
            current_player_ingredients_msg = json.dumps({
                "action": "STARTING_INGREDIENTS",
                "ingredients": player_ingredients,
            })
            await player.websocket.send(current_player_ingredients_msg)
            print(f"inviato al giocatore {player.ingr_id} gli ingredienti {player_ingredients}")

async def handle_pass_ingredient(websocket, current_player, data):
    #bisogna prendere la websocket del giocatore che si trova a sinistra o a destra a sinistra
    print("IL SERVER ha ricevuto la richiesta di passaggio dell'ingrediente")
    current_player.num_passed_ingr += 1
    pass_direction = data.get("direction") #LEFT o RIGHT
    room = room_manager.get_room(current_player.room_code)
    if not room:
        print(f"Stanza non trovata per il giocatore {current_player.id}")
        return
    if pass_direction == "LEFT":
        #l'ingrediente passato a sinistra nella destinazione è ricevuto a destra
        target_direction = "RIGHT"
    elif pass_direction == "RIGHT":
        #l'ingrediente passato a destra nella destinazione è ricevuto a sinistra
        target_direction = "LEFT"
    print(target_direction)    
    target_player = room.get_near_player(current_player, pass_direction)
    if target_player is not None:
        print(f"Il vicino a cui passare l'ingrediente {data.get('ingr_name')} è {target_player.ingr_id}")
        target_player_socket = target_player.websocket        
        response = json.dumps({
            "action": "NEW_INGREDIENT", 
            "ingr_name": data.get("ingr_name"),
            "direction": target_direction,
            "score": data.get("score"),
            "dimension": data.get("dimension")
        })
        await target_player_socket.send(response)
    else:
        print(f"ATTENZIONE: Nessun vicino trovato in direzione {data.get('direction')} per questo giocatore!")    


async def handle_plate_complete(websocket, current_player, data):
    print(f"DEBUG handle_plate_complete: finished_all_plates={data.get('finished_all_plates')}, gained_score={data.get('gained_score')}")
    current_player.score += data.get("gained_score", 0)
    print("IL piatto è arrivato in cucina")
    current_player.num_plates_completed += 1
    room = room_manager.get_room(current_player.room_code)
    
    if not room:
        print(f"Room non trovata per il giocatore {current_player.ingr_id}, probabilmente chiusa dopo disconnessione")
        return

    if data.get("finished_all_plates"):
        #se il giocatore ha finito tutti i suoi piatti allora si verifica se tutti i giocaotori sono in attesa o se ancora c'è qualcuno che sta giocando (ha piatti da completare)
        room.num_waiting_players += 1
        print(f"DEBUG: {room.num_waiting_players}/{len(room.players)} giocatori in attesa")
        if room.num_waiting_players >= len(room.players):
            room.num_waiting_players = 0
            # si deve passare al livello successivo
            # inviare STARTING_INGREDIENTS e STARTING_PLATES a tutti i giocatori
            room.curr_level += 1
            next_level_key = f"level_{room.curr_level}"
            
            if next_level_key in levels_setting:
                await handle_start_level(websocket, current_player, data)
            else:
                # Fine partita — invia SCORE a tutti
                print("DEBUG: Partita finita! Invio schermata score.")

                for player in room.players.values():
                    passing_bonus = player.num_passed_ingr * 10
                    player.score += passing_bonus

                team_dishes = sum(p.num_plates_completed for p in room.players.values())
                team_points = sum(p.score for p in room.players.values())

                for player in room.players.values():
                    base_score = player.score - (player.num_passed_ingr * 10) 
                    await player.websocket.send(json.dumps({
                        "action": "CHANGE_MODEL_STATE",
                        "current_state": "SCORE",
                        "scores": {
                            "player": {
                                "name": player.ingr_id,
                                "dishes": player.num_plates_completed,
                                "points": base_score,
                                "passing_bonus": player.num_passed_ingr * 10
                            },
                            "team": {
                                "dishes": team_dishes,
                                "points": team_points,
                                "level": room.curr_level
                            }
                        }
                    }))

    
async def handle_player_disconnect(player, player_id):
    room = room_manager.get_room(player.room_code)
    if not room or room.state != RoomState.IN_GAME:
        return

    #distribuzione degli ingrendienti iniziali del player uscito
    ingredients_to_redistribute = player.initial_ingredients or []

    # Rimuovi subito il giocatore dalla room
    room.remove_player(player_id)

    if ingredients_to_redistribute:
        remaining_players = list(room.players.values())
        if remaining_players:
            random.shuffle(ingredients_to_redistribute)
            weights = [random.uniform(0.5, 1.5) for _ in remaining_players]
            total_weight = sum(weights)
            start_index = 0

            for i, p in enumerate(remaining_players):
                if i == len(remaining_players) - 1:
                    chunk = ingredients_to_redistribute[start_index:]
                else:
                    count = round(len(ingredients_to_redistribute) * (weights[i] / total_weight))
                    count = max(1, count)
                    end_index = min(start_index + count, len(ingredients_to_redistribute))
                    chunk = ingredients_to_redistribute[start_index:end_index]
                    start_index = end_index
                if chunk:
                    await p.websocket.send(json.dumps({
                        "action": "NEW_INGREDIENTS_BATCH",
                        "ingredients": chunk
                    }))

    for p in room.players.values():
        await p.websocket.send(json.dumps({
            "action": "PLAYER_DISCONNECTED",
            "player_ingr_id": player.ingr_id
        }))

    remaining = list(room.players.values())
    if len(remaining) < 2:
        if remaining:
            sole_player = remaining[0]
            team_dishes = sum(p.num_plates_completed for p in room.players.values())
            team_points = sum(p.score for p in room.players.values())
            passing_bonus = sole_player.num_passed_ingr * 10
            sole_player.score += passing_bonus
            base_score = sole_player.score - passing_bonus
            await sole_player.websocket.send(json.dumps({
                "action": "CHANGE_MODEL_STATE",
                "current_state": "SCORE",
                "scores": {
                    "player": {
                        "name": sole_player.ingr_id,
                        "dishes": sole_player.num_plates_completed,
                        "points": base_score,
                        "passing_bonus": passing_bonus
                    },
                    "team": {
                        "dishes": team_dishes,
                        "points": team_points,
                        "level": room.curr_level
                    }
                }
            }))
        room_manager.remove_room(player.room_code)
        return

    if room.check_all_waiting():
        room.num_waiting_players = 0
        room.curr_level += 1
        if f"level_{room.curr_level}" in levels_setting:
            await handle_start_level(None, player, {})

ACTION_HANDLERS = {
    "START_GAME": handle_start_game,
    "JOIN_ROOM": handle_join_room,
    "QUIT_ROOM": handle_quit_room,
    "START_PLAYING": handle_start_playing,
    "PASS_INGREDIENT": handle_pass_ingredient,
    "PLATE_COMPLETE": handle_plate_complete,
}