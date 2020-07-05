"""Functions to run AVE."""

import os
import json
from ave import AVE, Character, config


def run():
    """Run AVE in terminal."""
    from .display.curses_screen import CursesScreen
    ave = AVE(screen=CursesScreen(), character=Character())
    ave.load_games_from_json(os.path.join(config.ave_folder, "gamelist.json"))
    ave.start()


def make_json():
    """Make a json containing metadata for every game."""
    config.debug = True
    ave = AVE()
    ave.load_games(config.games_folder)
    gamelist = [{
        "title": game.title,
        "author": game.author,
        "desc": game.description,
        "active": game.active,
        "version": game.version,
        "ave_version": game.ave_version,
        "filename": game.filename,
        "number": game.number
    } for game in ave.games]

    with open(os.path.join(config.ave_folder, "gamelist.json"), "w") as f:
        json.dump(gamelist, f)
