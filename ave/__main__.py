"""Functions to run AVE."""

import os
import json
from ave import AVE, config


def run():
    """Run AVE in terminal."""
    from .screen import Screen
    ave = AVE(screen=Screen())
    ave.load_games(config.games_folder)
    ave.start()


def make_json():
    """Make a json containing metadata for every game."""
    config.debug = True
    ave = AVE()
    ave.load_games(config.games_folder)
    gamelist = [{
        "title": game.title,
        "desc": game.description,
        "active": game.active,
        "version": game.version,
        "ave_version": game.ave_version,
        "filename": game.filename
    } for game in ave.games]

    with open(os.path.join(config.root_folder, "gamelist.json"), "w") as f:
        json.dump(gamelist, f)
