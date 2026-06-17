import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../server/src"))

from unittest.mock import MagicMock
from main.player import Player
from main.room_manager import RoomManager

def test_create_room_unique_code():
    rm = RoomManager()
    r1 = rm.create_room()
    r2 = rm.create_room()
    assert r1.code != r2.code

def test_remove_room_resets_players():
    rm = RoomManager()
    room = rm.create_room()
    ws = MagicMock()
    p = Player("p1", ws)
    p.position = 2
    room.add_player(p)
    rm.remove_room(room.code)
    assert p.room_code is None
    assert p.position is None

def test_remove_player_closes_room_if_host_leaves():
    rm = RoomManager()
    room = rm.create_room()
    p1 = Player("p1", MagicMock())
    p2 = Player("p2", MagicMock())
    room.add_player(p1)
    room.add_player(p2)
    rm.remove_player("p1")  # p1 è l'host
    assert room.code not in rm.rooms