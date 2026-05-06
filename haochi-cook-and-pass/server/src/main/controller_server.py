import json
from .connection_manager import manager
from .room_manager import RoomManager
from .room import Room

room_manager = RoomManager()

async def handle_start_game(websocket, current_player, data):
    game_code = room_manager.generate_code(length=4)
    current_player.room_code = game_code
    #Aggiungere anche un ingrediente id per il giocatore iniziale 
    current_player.ingr_id = "carrot" #TO DO prendere id ingrediente del giocatore dal DB
    room = Room(game_code) #si crea la room
    room.add_player(current_player)

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

    if room is None:
        await websocket.send(json.dumps({"action": "ERROR", "message": "Room not found"}))
        return

    room = room_manager.get_room(game_code)
    room.add_player(current_player)
    
    ingr_possible_ids = ["lemon", "orange", "pepper", "rice", "shrimp", "carrot", "basil", "broccoli"]
    players_in_room = room.players
    taken_ids = []
    for player in players_in_room:
        taken_ids.append(player.ingr_id)
    #TO DO prendere da DB fin tanto che non se ne trova uno diverso 
    available_ids = list(set(ingr_possible_ids) - set(taken_ids))
    current_player.ingr_id = available_ids[0]  
    #Messaggio inviato al giocatore che ha preso parte ad una room per farlo passare a LobbyState
    current_player_response = json.dumps({
        "action": "CHANGE_MODEL_STATE", 
        "current_state": "LOBBY",
        "ingr_id": current_player.ingr_id 
    }) 
    await websocket.send(current_player_response)


    taken_ids.insert(0, current_player.ingr_id)
    host_id_socket = players_in_room[room.host_id].websocket 
    response = json.dumps({
        "action": "UPDATE_CURRENT_PLAYERS", 
        "players_id": taken_ids,
        "is_starting_player": True
    })
    await host_id_socket.send(response)

async def handle_quit_room(websocket, current_player, data):
    #TO DO Decommentare per avere corretto funzionamento
    room = room_manager.get_room(current_player.room_code)
    room.remove_player(current_player)
    players_in_room = room.players
    taken_ids = []
    for player in players_in_room:
        taken_ids.append(player.ingr_id)
    host_id_socket = players_in_room[room.host_id].websocket 
    response = json.dumps({
        "action": "UPDATE_CURRENT_PLAYERS", 
        "players_id": taken_ids,
        "is_starting_player": True
    })
    await host_id_socket.send(response)

    current_player_response = json.dumps({
        "action": "CHANGE_MODEL_STATE", 
        "current_state": "MENU",
    }) 
    await websocket.send(current_player_response)

#Quando il giocatore che ha avviato la partita clicca START nella LOBBY:
# - Si setta la posizione dei giocatori a quella ricevuta dal messaggio
# - Si fa cambiare lo stato del model a tutti i giocatori in PLAYING 
async def handle_start_playing(websocket, current_player, data):
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
