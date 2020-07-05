import json
import os
from ave import config
from ave.__main__ import generate_json


def test_gamelist():
    config.debug = True
    with open(os.path.join(config.ave_folder, "gamelist.json")) as f:
        gamelist = json.load(f)
    for game in gamelist:
        game["ave_version"] = tuple(game["ave_version"])

    games = generate_json(config.games_folder)

    games.sort(key=lambda x: x["filename"])
    gamelist.sort(key=lambda x: x["filename"])
    assert gamelist == games
