import json

from .db.db_manager import db
from .connection_manager import manager
from .room_manager import RoomManager
from .room import Room

room_manager = RoomManager()

async def handle_start_game(websocket, current_player, data):
    room = room_manager.create_room() 
    game_code = room.code
    
    current_player.room_code = game_code
    #Aggiungere anche un ingrediente id per il giocatore iniziale 
    #current_player.ingr_id = db.get_ingredients()[0]
    random_ingredient = db.get_random_ingredient()

    if random_ingredient:
        current_player.ingr_id = random_ingredient
        print(f"Player {current_player.id} assigned ingredient: {current_player.ingr_id}")
    else:
        print("No ingredients found in the database.")
        current_player.ingr_id = "shrimp"  # Default ingredient if DB is empty

    room.add_player(current_player)
    print(f"Giocatori nella room dopo la creazione:", [player.id for player in room.players.values()])

    response = json.dumps({
        "action": "ROOM_CREATED", 
        "code": game_code, 
        "player_id": current_player.id
    })
    await websocket.send(response)

    #Invio del messaggio per aggiornare l'interfaccia della LOBBY 
    response = json.dumps({
            "action": "UPDATE_CURRENT_PLAYERS", 
            "players_id": [current_player.ingr_id],
            "is_starting_player": True
        })
    await websocket.send(response)

    
    await manager.broadcast(json.dumps({
        "action": "PLAYER_READY", 
        "player_id": current_player.id
    }), exclude=websocket)

#Quando un nuovo giocatore si aggiunge alla partita:
# - La sua interfaccia deve passare a LOBBY_STATE con is_starting_player a False
# - Si deve aggiungere il giocatore alla room OK
# - Si deve creare un nuovo ingr_id per l'utente che sia diverso da tutti quelli già presenti (ogni volta si prende da DB) OK
# - Si deve avvisare ogni giocatore nella room che si è unito un nuovo giocatore (per adesso si avvisa solo il giocatore che ha avviato la partita) OK
async def handle_join_room(websocket, current_player, data):
    #Si aggiunge un utente alla partita  
    game_code = data.get("code")
    room = room_manager.get_room(game_code)
    #ingr_possible_ids = db.get_ingredients()

    if room is None:
        await websocket.send(json.dumps({"action": "ERROR", "message": "Room not found"}))
        return

    taken_ids = [player.ingr_id for player in room.players.values()]

    found_unique = False
    attempts = 0
    max_attempts = 20 # Sicurezza per evitare cicli infiniti se il DB è piccolo
    
    assigned_ingr = "chili" # Fallback predefinito

    while not found_unique and attempts < max_attempts:
        random_candidate = db.get_random_ingredient()
        
        if random_candidate not in taken_ids:
            assigned_ingr = random_candidate
            found_unique = True
        
        attempts += 1

    current_player.ingr_id = assigned_ingr
    room.add_player(current_player)

    players_in_room = room.players.values()

    print("Giocatori nella room dopo l'aggiunta:", [player.id for player in room.players.values()])

    for player in players_in_room:
        taken_ids.append(player.ingr_id)

    #TO DO prendere da DB fin tanto che non se ne trova uno diverso 
    #available_ids = list(set(ingr_possible_ids) - set(taken_ids))
    #current_player.ingr_id = available_ids[0]  

    #print(f"Player {current_player.id} ha preso ingr_id: {current_player.ingr_id}")

    #Messaggio inviato al giocatore che ha preso parte ad una room per farlo passare a LobbyState
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
    #TO DO Decommentare per avere corretto funzionamento

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
    #Si cambia lo stato di tutti i giocatori in PLAYING tutti i giocatori
    await manager.broadcast(json.dumps({
        "action": "CHANGE_MODEL_STATE", 
        "current_state": "PLAYING",
    }))
    #TO DO:
    # @ pensare a come distribuire i piatti da completare ai giocatori attraverso STARTING_PLATES
    # @ pensare a come distribuire tutti gli ingredienti dei piatti tra i vari giocatori attraverso messaggio STARTING_INGREDIENTS
        

async def handle_pass_ingredient(websocket, current_player, data):
    #bisogna prendere la websocket del giocatore che si trova a sinistra o a destra a sinistra
    pass_direction = data.get("direction") #LEFT o RIGHT
    room = room_manager.get_room(current_player.room_code)
    if pass_direction == "LEFT":
        #prendere la websocket del player a sinistra di quello corrente
        target_direction = "RIGHT"
    elif pass_direction == "RIGHT":
        #prendere la websocket del player a destra di quello corrente
        target_direction = "LEFT"
#TO DO creare la funzione
    target_player = room.get_near_player(current_player, pass_direction)
    target_player_socket = target_player.websocket        
    response = json.dumps({
        "action": "NEW_INGREDIENT", 
        "ingr_name": data.get("ingr_name"),
        "direction": target_direction,
        "score": data.get("score"),
        "dimension": data.get("dimension")
    })
    await target_player_socket.send(response)


async def handle_plate_complete(websocket, current_player, data):
    room = room_manager.get_room(current_player.room_code)
    if data.get("finished_all_plates"):
        #se il giocatore ha finito tutti i suoi piatti allora si verifica se tutti i giocaotori sono in attesa o se ancora c'è qualcuno che sta giocando (ha piatti da completare)
        room.num_waiting_players += 1
        if room.num_waiting_players == len(room.players):
            # si deve passare al livello successivo
            # TO DO inviare STARTING_INGREDIENTS e STARTING_PLATES a tutti i giocatori
            pass
    current_player.score += data.get("gained_score")   
    # TO DO  
    # si può anche pensare di tenere traccia attraverso un dizionario del numero di ciascun tupo di ingrediente usato dal giocatore
    # e anche del numero di piatti composti e del numero di essi per ogni tipo
    # in modo da realizzare il report

ACTION_HANDLERS = {
    "START_GAME": handle_start_game,
    "JOIN_ROOM": handle_join_room,
    "QUIT_ROOM": handle_quit_room,
    "START_PLAYING": handle_start_playing,
    "PASS_INGERDIENT": handle_pass_ingredient,
    "PLATE_COMPLETE": handle_plate_complete
}
