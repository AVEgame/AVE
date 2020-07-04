import pytest
import os
from ave import config, AVE, Character, exceptions
from ave import load_game_from_file, load_game_from_library

config.debug = True
games_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../games")
testgames_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../test/games")

games = [os.path.join(games_path, filename)
         for filename in os.listdir(games_path) if filename[-4:] == ".ave"]


@pytest.mark.parametrize(
    'filename', [os.path.join(testgames_path, "hidden_test.ave")])
def test_version_checking(filename):
    try:
        game = load_game_from_file(filename)
        game.load()
        assert False
    except exceptions.AVEVersionError:
        pass

    ave = AVE()
    ave.load_games("test/games")
    for game in ave.games:
        assert game.file != filename


@pytest.mark.parametrize('filename', games)
def test_all_rooms_acessible(filename):
    game = load_game_from_file(filename)
    game.load()
    ach = {"start"}
    for room in game.rooms.values():
        for option in room.options:
            for d in option.get_all_destinations():
                ach.add(d)
    not_ach = [i for i in game.rooms if i not in ach]

    if len(not_ach) > 0:
        print("Rooms not accessible:")
        for key in not_ach:
            print(" ", key)
        assert False


@pytest.mark.parametrize('filename', games)
def test_all_rooms_defined(filename):
    game = load_game_from_file(filename)
    game.load()
    not_inc = set()
    for room in game.rooms.values():
        for option in room.options:
            for d in option.get_all_destinations():
                if d == "__GAMEOVER__" or d == "__WINNER__":
                    continue
                if d not in game.rooms:
                    not_inc.add(d)

    if len(not_inc) > 0:
        print("Rooms not defined:")
        for key in not_inc:
            print(" ", key)
        assert "test.ave" in filename
        assert len(not_inc) == 1 and "fakeroom" in not_inc


@pytest.mark.parametrize('filename', games)
def test_has_start(filename):
    game = load_game_from_file(filename)
    game.load()
    assert game["start"].id != "fail"


@pytest.mark.parametrize('filename', games)
def test_first_room(filename):
    ave = AVE(character=Character())
    game = load_game_from_file(filename)
    game.load()
    game["start"].get_text(ave.character)
    game["start"].get_options(ave.character)


def test_game_library():
    ave = AVE()
    ave.get_download_menu()


def test_load_game_from_library():
    ave = AVE()
    game = load_game_from_library(ave.get_download_menu()[0][2])
    game.load()
    assert game["start"].id != "fail"
