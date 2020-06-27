import pytest
import os
from ave.ave import Game, Character
from ave.screen import DummyScreen

path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../games")
games = [os.path.join(path, filename) for filename in os.listdir(path)
         if filename[-4:] == ".ave"]

@pytest.mark.parametrize('filename', games)
def test_notebook(filename):
    ds = DummyScreen()
    c = Character(ds)

    def avefile():
        with open(filename) as f:
            return f.readlines()


    game = Game(avefile, ds, c)
    game.load()
    not_inc = []
    ach = ["start"]
    for id in game.rooms:
        for key in game[id].options:
            if key['id'] not in ach:
                ach.append(key['id'])
            if key['id'] not in game.rooms and key['id'] != "__GAMEOVER__" and key['id'] != "__WINNER__" and key['id'] not in not_inc:
                not_inc.append(key['id'])

    not_ach = [i for i in game.rooms if i not in ach]

    if len(not_inc)>0 or len(not_ach)>0:
        if len(not_inc)>0:
            print("Rooms not defined:")
            for key in not_inc:
                print(" ", key)
        if len(not_ach)>0:
            print("Rooms not accessible:")
            for key in not_ach:
                print(" ", key)
    assert len(not_inc) == 0
    assert len(not_ach) == 0
