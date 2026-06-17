import sys, os, asyncio, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../server/src"))

from unittest.mock import MagicMock, AsyncMock, patch
from main.controller_server import handle_start_game, handle_join_room
from main.player import Player
from main.room import Room

def create_player(id):
    ws = AsyncMock()
    p = Player(player_id = id, websocket = ws)
    return p

def test_handle_start_game_creates_room():
    websocket = AsyncMock() #web socket of the server for player's connection
    player = create_player("player1")
    fake_room = MagicMock()
    fake_room.code = "LYMS"

    with patch("main.controller_server.room_manager.create_room",
               return_value=fake_room), \
         patch("main.controller_server.db.get_random_ingredient",
               return_value="tomato"):

        asyncio.run(handle_start_game(websocket, player, {}))

        # check player's updates
        assert player.room_code == "LYMS"
        assert player.ingr_id == "tomato"

        fake_room.add_player.assert_called_once_with(player)
        assert websocket.send.await_count == 2

        #calls = websocket.send.await_args_list

def test_handle_join_room_wrong_game_code():
    player = create_player("player1")
    data = {"code": "1234"}
    ws = AsyncMock()
    with patch("main.controller_server.room_manager.get_room", return_value = None):
              
              asyncio.run(handle_join_room(ws, player, data))
              
              sent_json_resp = ws.send.await_args_list[0].args[0]
              response =  json.loads(sent_json_resp)
              assert response["action"] == "ERROR"

def test_handle_join_room_correct_game_code():
    player1 = create_player("player1")
    player1.ingr_id = "tomato"
    player2 = create_player("player2")
    data = {"code": "1234"}
    ws = AsyncMock()
    room = Room(room_code = "1234")
    room.players = {"0": player1}
    room.host_id = "0"
    with patch("main.controller_server.room_manager.get_room", 
                return_value = room), \
         patch("main.controller_server.db.get_random_ingredient",
                return_value = player1.ingr_id):
            
            asyncio.run(handle_join_room(ws, player2, data)) 

            assert player2.ingr_id == "chili"

            calls_added_player = ws.send.await_args_list
            change_model_msg = json.loads(calls_added_player[0].args[0])
            assert change_model_msg["action"] == "CHANGE_MODEL_STATE"

            calls_host_player = player1.websocket.send.await_args_list
            update_players_in_game = json.loads(calls_host_player[0].args[0])
            assert update_players_in_game["action"] == "UPDATE_CURRENT_PLAYERS" 
            assert set(update_players_in_game["players_id"]) == {"chili", "tomato"}


               
