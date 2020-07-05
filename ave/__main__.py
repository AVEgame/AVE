"""Functions to run AVE."""

import os
import json
from ave import AVE, Character, config


def run():
    """Run AVE in terminal."""
    import argparse

    parser = argparse.ArgumentParser(description='Run the AVE game engine.')
    parser.add_argument('folder', metavar='folder', nargs='?', default=None,
                       help='A folder to load AVE games from.')

    args = parser.parse_args()

    from .display.curses_screen import CursesScreen
    ave = AVE(screen=CursesScreen(), character=Character())
    ave.load_games_from_json(os.path.join(config.ave_folder, "gamelist.json"))
    if args.folder is not None:
        ave.load_games(args.folder, "[*] ")
    ave.start()


def make_json(game_folder=config.games_folder, json_folder=config.ave_folder):
    """Make a json containing metadata for every game and write it to file."""
    config.debug = True
    ave = AVE()
    ave.load_games(game_folder)
    gamelist = generate_json(game_folder)
    with open(os.path.join(json_folder, "gamelist.json"), "w") as f:
        json.dump(gamelist, f)


def generate_json(game_folder=config.games_folder):
    """Make a json containing metadata for every game."""
    config.debug = True
    ave = AVE()
    ave.load_games(game_folder)
    return [{
        "title": game.title,
        "author": game.author,
        "desc": game.description,
        "active": game.active,
        "version": game.version,
        "ave_version": game.ave_version,
        "filename": game.filename,
        "number": game.number
    } for game in ave.games]
