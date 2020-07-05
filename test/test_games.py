import pytest
import os
from ave import config, AVE, exceptions
from ave import load_game_from_file, load_game_from_library
from ave.test import check_game

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
def test_games_for_errors(filename):
    game = load_game_from_file(filename)
    game.load()

    errors = check_game(game)
    errors.sort(key=lambda e: -e.error_value)

    for e in errors:
        print(e)

    # remove Info and Note errors
    errors = [i for i in errors if i.error_value > 2]

    if filename.endswith("test.ave"):
        assert len(errors) == 1
        assert "fakeroom" in errors[0].description
    else:
        # Assert that the worst error is a Warning or lower
        assert len(errors) == 0


def test_game_library():
    ave = AVE()
    ave.get_download_menu()


def test_load_game_from_library():
    ave = AVE()
    game = load_game_from_library(ave.get_download_menu()[0][2])
    game.load()
    assert game["start"].id != "fail"
