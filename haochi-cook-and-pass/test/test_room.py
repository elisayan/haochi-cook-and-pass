import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../server/src/main"))

import pytest
from unittest.mock import MagicMock
from room import Room, RoomState
from player import Player

def make_player(pid, ingr_id=None):
    ws = MagicMock()
    p = Player(player_id=pid, websocket=ws)
    p.ingr_id = ingr_id
    return p

#add_player
def test_add_player_sets_host():
    room = Room("ABCD")
    p = make_player("p1")
    room.add_player(p)
    assert room.host_id == "p1"

def test_add_player_max_8():
    room = Room("ABCD")
    for i in range(8):
        assert room.add_player(make_player(f"p{i}")) == True
    assert room.add_player(make_player("p9")) == False

def test_state_becomes_ready_with_2_players():
    room = Room("ABCD")
    room.add_player(make_player("p1"))
    assert room.state == RoomState.INIT
    room.add_player(make_player("p2"))
    assert room.state == RoomState.READY

def test_state_does_not_change_during_game():
    room = Room("ABCD")
    room.add_player(make_player("p1"))
    room.add_player(make_player("p2"))
    room.set_in_game()
    room.add_player(make_player("p3"))
    assert room.state == RoomState.IN_GAME  #non deve tornare READY

#remove_player
def test_remove_player_updates_positions():
    room = Room("ABCD")
    p1, p2, p3 = make_player("p1"), make_player("p2"), make_player("p3")
    for p in [p1, p2, p3]:
        room.add_player(p)
    p1.position, p2.position, p3.position = 0, 1, 2
    room.remove_player("p1")
    assert p2.position == 0
    assert p3.position == 1

#get_near_player
def test_get_near_player_left_wraps():
    room = Room("ABCD")
    p1, p2 = make_player("p1", "ing1"), make_player("p2", "ing2")
    room.add_player(p1)
    room.add_player(p2)
    p1.position, p2.position = 0, 1
    result = room.get_near_player(p1, "LEFT")
    assert result == p2  # wrap circolare

#check_all_waiting
def test_check_all_waiting_true():
    room = Room("ABCD")
    room.add_player(make_player("p1"))
    room.add_player(make_player("p2"))
    room.num_waiting_players = 1  # tutti tranne uno
    assert room.check_all_waiting() == True