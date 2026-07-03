import sys, os, asyncio, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../server/src"))

from unittest.mock import MagicMock, AsyncMock, patch
from main.controller_server import handle_start_game, handle_join_room, handle_start_playing, handle_start_level, handle_pass_ingredient, handle_plate_complete
from main.player import Player
from main.room import Room

def create_player(id, ingr_id = None, position = None):
    ws = AsyncMock()
    p = Player(player_id = id, websocket = ws)
    p.ingr_id = ingr_id
    p.position = position
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

def test_handle_join_room_wrong_game_code():
    player = create_player("player1")
    data = {"code": "1234"}
    ws = AsyncMock()
    with patch("main.controller_server.room_manager.get_room", return_value = None):
              
              asyncio.run(handle_join_room(ws, player, data))
              
              #check behaviour in case the code of the room is not correct 
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
    room.players = {player1.ingr_id: player1}
    room.host_id = player1.ingr_id
    with patch("main.controller_server.room_manager.get_room", 
                return_value = room), \
         patch("main.controller_server.db.get_random_ingredient",
                return_value = player1.ingr_id):
            
            asyncio.run(handle_join_room(ws, player2, data)) 
            
            #check assigned id of the added player in the game
            assert player2.ingr_id == "chili"

            #check that the server has sent message to added player to change state 
            calls_added_player = ws.send.await_args_list
            change_model_msg = json.loads(calls_added_player[0].args[0])
            assert change_model_msg["action"] == "CHANGE_MODEL_STATE"

            #check that the server has sent message to the host of the game to get updated about the new player 
            calls_host_player = player1.websocket.send.await_args_list
            update_players_in_game = json.loads(calls_host_player[0].args[0])
            assert update_players_in_game["action"] == "UPDATE_CURRENT_PLAYERS" 
            assert set(update_players_in_game["players_id"]) == {"chili", "tomato"}

def test_starting_playing():
    data = {"players_position": ["tomato", "chili", "onion"]}
    ws = AsyncMock()
    player1 = create_player("player1", ingr_id="onion") #host that starts the game
    player2 = create_player("player2", ingr_id="chili")
    player3 = create_player("player3", ingr_id="tomato")
    room = Room("AAAA")
    room.add_player(player1)
    room.add_player(player2)
    room.add_player(player3)

    with patch("main.controller_server.room_manager.get_room", 
               return_value = room), \
         patch("main.controller_server.handle_start_level", 
               new_callable=AsyncMock), \
         patch("main.controller_server.manager", new_callable=AsyncMock) as mock_manager:
            asyncio.run(handle_start_playing(ws, player1, data))

            #check correct order players in game
            assert player3.position == 0
            assert player2.position == 1
            assert player1.position == 2

            #check sended messages
            assert mock_manager.broadcast.call_count == 1
            assert set(mock_manager.broadcast.call_args[1]["include_only"]) == set([player1.websocket, player2.websocket, player3.websocket])

def test_handle_start_level_level_0():
    ws = AsyncMock()
    player1 = create_player("player1", ingr_id="tomato")
    player2 = create_player("player2", ingr_id="chili")
    room = Room("AAAA")
    room.curr_level = 0
    room.players = {
        player1.id: player1,
        player2.id: player2
    }

    easy_recipe = {"ingredients": ["bread", "avocado"]}
    medium_recipe = {"ingredients": ["nachos", "chili", "avocado"]}

    def simple_db(diff, n):
        if diff == "easy":
            return [easy_recipe] * n
        if diff == "medium":
            return [medium_recipe] * n
        return []

    with patch("main.controller_server.room_manager.get_room",
               return_value=room), \
         patch("main.controller_server.db.get_random_recipes_by_difficulty",
               side_effect=simple_db), \
         patch("main.controller_server.random.shuffle",
               lambda x: x):

        asyncio.run(handle_start_level(ws, player1, {}))

    #check users receive the correct number of messages (one for the list of recipes and one for the list of ingredients)
    assert player1.websocket.send.await_count == 2
    assert player2.websocket.send.await_count == 2

    #check that the number of recipes is 3 for each player and that the list of recipes is sent to each player with a message of action "STARTING_RECIPES"
    msg1 = json.loads(player1.websocket.send.await_args_list[0].args[0])
    msg2 = json.loads(player2.websocket.send.await_args_list[0].args[0])
    assert msg1["action"] == "STARTING_RECIPES"
    assert msg2["action"] == "STARTING_RECIPES"
    assert len(msg1["recipes"]) == 3
    assert len(msg2["recipes"]) == 3
    all_ingredients_of_recipes = []
    for rec in msg1["recipes"] + msg2["recipes"]:
        all_ingredients_of_recipes.extend(rec["ingredients"])


   #check that the list of ingredients is sent to each player with a message of action "STARTING_INGREDIENTS" and the number of ingredients is correct for completing all the recipes
    ing1 = json.loads(player1.websocket.send.await_args_list[1].args[0])
    ing2 = json.loads(player2.websocket.send.await_args_list[1].args[0])
    assert ing1["action"] == "STARTING_INGREDIENTS"
    assert ing2["action"] == "STARTING_INGREDIENTS"
    all_assigned_ingredients = ing1["ingredients"] + ing2["ingredients"]
    assert len(all_assigned_ingredients) == len(all_ingredients_of_recipes)

    #check ingredients correctly updated
    assert player1.initial_ingredients == player1.current_ingredients
    assert player2.initial_ingredients == player2.current_ingredients            

def test_handle_pass_ingredient():
    ws = AsyncMock()
    #SET UP (position players in game): receiver - sender - other_player
    sender = create_player("player1", ingr_id="tomato", position=1)
    receiver = create_player("player2", ingr_id="chili", position=0)
    other_player = create_player("player3", ingr_id="onion", position=2)
    room = Room("AAAA")
    room.players = {sender.ingr_id: sender, receiver.ingr_id: receiver, other_player.ingr_id: other_player}
    data = {
        "direction": "LEFT",
        "ingr_name": "bread",
        "score": 15
    }
    with patch("main.controller_server.room_manager.get_room",
            return_value=room):
        asyncio.run(handle_pass_ingredient(ws, sender, data))

        assert sender.num_passed_ingr == 1
        assert receiver.websocket.send.await_count == 1
        sent_msg = json.loads(receiver.websocket.send.await_args_list[0].args[0])
        assert sent_msg["action"] == "NEW_INGREDIENT"
        assert sent_msg["ingr_name"] == "bread"
        assert sent_msg["direction"] == "RIGHT"
        assert sent_msg["score"] == 15

def test_handle_plate_complete_single_plate():
    ws = AsyncMock()
    player = create_player("player1", ingr_id="tomato")
    player.room_code = "AAAA"
    room = MagicMock()
    data = {
        "gained_score": 50,
        "finished_all_plates": False
    }
    with patch("main.controller_server.room_manager.get_room",
                return_value=room):
        asyncio.run(handle_plate_complete(ws, player, data))
        
        assert player.score == 50
        assert player.num_plates_completed == 1


               
