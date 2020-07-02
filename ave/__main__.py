"""Functions to run AVE."""

from ave import AVE, config


def run():
    """Run AVE in terminal."""
    ave = AVE()
    ave.load_games(config.games_folder)
    ave.start()
