import pytest
import os
from ave import (config, AVE, Character, DummyScreen,
                 load_game_from_file, load_game_from_library)

config.debug = True
path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../games")
games = [os.path.join(path, filename) for filename in os.listdir(path)
         if filename[-4:] == ".ave"]


def run_access_test(game):
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


def run_defined_test(game):
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


def run_start_test(game):
    assert game["start"].id != "fail"


@pytest.mark.parametrize('filename', games)
def test_all_rooms_acessible(filename):
    ds = DummyScreen()
    c = Character(ds)

    game = load_game_from_file(filename)
    game.character = c
    game.screen = ds
    game.load()
    run_access_test(game)


@pytest.mark.parametrize('filename', games)
def test_all_rooms_defined(filename):
    ds = DummyScreen()
    c = Character(ds)

    game = load_game_from_file(filename)
    game.character = c
    game.screen = ds
    game.load()
    run_defined_test(game)


@pytest.mark.parametrize('filename', games)
def test_has_start(filename):
    ds = DummyScreen()
    c = Character(ds)

    game = load_game_from_file(filename)
    game.character = c
    game.screen = ds
    game.load()
    run_start_test(game)


def test_game_library():
    ave = AVE(dummy=True)
    ave.get_download_menu()


def test_load_game_from_library():
    ds = DummyScreen()
    c = Character(ds)

    ave = AVE(dummy=True)
    game = load_game_from_library(
        ave.get_download_menu()[0][2])
    game.character = c
    game.screen = ds
    game.load()
    run_defined_test(game)
    run_access_test(game)
    run_start_test(game)
