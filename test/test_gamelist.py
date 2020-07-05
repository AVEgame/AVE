import json
import os
from ave import config
from ave.__main__ import generate_json


def test_gamelist():
    with open(os.path.join(config.ave_folder, "gamelist.json")) as f:
        gamelist_json = f.read()

    games = generate_json(config.games_folder)
    games_json = json.dumps(games)
    assert gamelist_json == games_json
