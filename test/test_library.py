from ave import AVE
from ave import load_game_from_library


def test_game_library():
    ave = AVE()
    ave.get_download_menu()


def test_load_game_from_library():
    ave = AVE()
    game = load_game_from_library(ave.get_download_menu()[0][2])
    game.load()
    assert game["start"].id != "fail"
