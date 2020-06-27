import pytest
import os
from ave.ave import Game, Character
from ave.screen import DummyScreen

path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../games")
games = [os.path.join(path, filename) for filename in os.listdir(path)
         if filename[-4:] == ".ave"]


@pytest.mark.parametrize('filename', games)
def test_all_rooms_acessible(filename):
    ds = DummyScreen()
    c = Character(ds)

    def avefile():
        with open(filename) as f:
            return f.readlines()

    game = Game(avefile, ds, c)
    game.load()
    ach = ["start"]
    for id in game.rooms:
        for key in game[id].options:
            if key['id'].startswith("__R__"):
                for d in key["id"][6:].split(")")[0].split(","):
                    if d not in ach:
                        ach.append(key)
            elif key['id'] not in ach:
                ach.append(key['id'])

    not_ach = [i for i in game.rooms if i not in ach]

    if len(not_ach) > 0:
        print("Rooms not accessible:")
        for key in not_ach:
            print(" ", key)
        assert False


@pytest.mark.parametrize('filename', games)
def test_all_rooms_defined(filename):
    ds = DummyScreen()
    c = Character(ds)

    def avefile():
        with open(filename) as f:
            return f.readlines()

    game = Game(avefile, ds, c)
    game.load()
    not_inc = []
    for id in game.rooms:
        for key in game[id].options:
            if key['id'].startswith("__R__"):
                dests = key["id"][6:].split(")")[0].split(",")
            else:
                dests = [key['id']]
            for d in dests:
                if d in game.rooms:
                    continue
                if d == "__GAMEOVER__" or d == "__WINNER__":
                    continue
                if d not in not_inc:
                    not_inc.append(d)

    if len(not_inc) > 0:
        print("Rooms not defined:")
        for key in not_inc:
            print(" ", key)
        assert False
