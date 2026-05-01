import json
from .connection_manager import manager
from .room_manager import RoomManager

room_manager = RoomManager()

async def handle_start_game(websocket, current_player, data):
    game_code = room_manager.generate_code(length=4)
    current_player.room_code = game_code
    
    response = json.dumps({
        "action": "ROOM_CREATED", 
        "code": game_code, 
        "player_id": current_player.id
    })
    await websocket.send(response)
    
    await manager.broadcast(json.dumps({
        "action": "PLAYER_READY", 
        "player_id": current_player.id
    }), exclude=websocket)

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
    # todo: "JOIN_ROOM": handle_join_room, ecc.
    "PASS_INGERDIENT": handle_pass_ingredient,
    "PLATE_COMPLETE": handle_plate_complete
}
