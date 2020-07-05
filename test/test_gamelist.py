import json
import os
from ave import config
from ave.__main__ import generate_json


def test_gamelist():
    config.debug = True
    with open(os.path.join(config.ave_folder, "gamelist.json")) as f:
        gamelist = json.load(f)

    games = generate_json(config.games_folder)
    assert gamelist == games
