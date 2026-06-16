import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../client/src/main"))

import numpy as np
from utilities import Element, Ingredient, PassIngredientMsg, CompletePlateMsg, Side

#Element.get_boundaries
def test_get_boundaries():
    e = Element("plate.PNG", (100, 60), (200, 200))
    l, r, t, b = e.get_boundaries()
    assert l == 150 and r == 250
    assert t == 170 and b == 230

def test_check_click_inside():
    e = Element("plate.PNG", (100, 100), (200, 200))
    e.check_click((200, 200))
    assert e.dragging == True

def test_check_click_outside():
    e = Element("plate.PNG", (100, 100), (200, 200))
    e.check_click((400, 400))
    assert e.dragging == False

def test_stop_dragging():
    e = Element("plate.PNG", (100, 100), (200, 200))
    e.dragging = True
    e.stop_dragging()
    assert e.dragging == False

#Ingredient
def test_ingredient_name_strips_suffix():
    i = Ingredient("shrimp.PNG", (50, 50), (0, 0), 1.5)
    assert i.name == "shrimp"

def test_ingredient_inside_plate():
    plate = Element("plate.PNG", (100, 100), (200, 200))
    ingr = Ingredient("shrimp.PNG", (30, 30), (200, 200), 1.0)
    assert ingr.inside(plate) == True

def test_ingredient_outside_plate():
    plate = Element("plate.PNG", (100, 100), (200, 200))
    ingr = Ingredient("shrimp.PNG", (30, 30), (400, 400), 1.0)
    assert ingr.inside(plate) == False

#PassIngredientMsg
def test_pass_ingredient_msg_structure():
    import numpy as np
    msg = PassIngredientMsg("shrimp", Side.LEFT, 1.5, np.array([50.0, 50.0]))
    assert msg.msg["action"] == "PASS_INGREDIENT"
    assert msg.msg["ingr_name"] == "shrimp"
    assert msg.msg["direction"] == "LEFT"
    assert msg.msg["score"] == 1.5

#CompletePlateMsg
def test_complete_plate_msg_structure():
    ingr1 = Ingredient("shrimp.PNG", (30, 30), (0, 0), 1.0)
    ingr2 = Ingredient("lemon.PNG", (30, 30), (0, 0), 2.0)
    msg = CompletePlateMsg([ingr1, ingr2], 3.0)
    assert msg.msg["action"] == "PLATE_COMPLETE"
    assert "shrimp" in msg.msg["completed_plate"]
    assert msg.msg["finished_all_plates"] == False

def test_complete_plate_msg_finished():
    msg = CompletePlateMsg([], 0.0, finished_all_plates=True)
    assert msg.msg["finished_all_plates"] == True