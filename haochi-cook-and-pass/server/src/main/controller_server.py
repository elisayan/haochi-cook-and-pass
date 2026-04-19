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


ACTION_HANDLERS = {
    "START_GAME": handle_start_game,
    # todo: "JOIN_ROOM": handle_join_room, ecc.
}
