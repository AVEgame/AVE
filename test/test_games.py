import pytest
import os
from ave import config, AVE
from ave import load_game_from_file, load_game_from_library

config.debug = True
path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../games")
games = [os.path.join(path, filename) for filename in os.listdir(path)
         if filename[-4:] == ".ave"]


def run_access_test(game):
    ach = {"start"}
    for room in game.rooms.values():
        for option in room.options:
            for d in option.get_destinations():
                ach.add(d)
    print(ach)
    not_ach = [i for i in game.rooms if i not in ach]

    if len(not_ach) > 0:
        print("Rooms not accessible:")
        for key in not_ach:
            print(" ", key)
        assert False


def run_defined_test(game):
    not_inc = set()
    for room in game.rooms.values():
        for option in room.options:
            for d in option.get_destinations():
                if d == "__GAMEOVER__" or d == "__WINNER__":
                    continue
                if d not in game.rooms:
                    not_inc.add(d)

    if len(not_inc) > 0:
        print("Rooms not defined:")
        for key in not_inc:
            print(" ", key)
        assert False


def run_start_test(game):
    assert game["start"].id != "fail"


@pytest.mark.parametrize('filename', games)
def test_all_rooms_acessible(filename):
    game = load_game_from_file(filename)
    game.load()
    run_access_test(game)


@pytest.mark.parametrize('filename', games)
def test_all_rooms_defined(filename):
    game = load_game_from_file(filename)
    game.load()
    run_defined_test(game)


@pytest.mark.parametrize('filename', games)
def test_has_start(filename):
    game = load_game_from_file(filename)
    game.load()
    run_start_test(game)


def test_game_library():
    ave = AVE(dummy=True)
    ave.get_download_menu()


def test_load_game_from_library():
    ave = AVE(dummy=True)
    game = load_game_from_library(ave.get_download_menu()[0][2])
    game.load()
    run_start_test(game)
