"""Loading a game from a .ave file."""

import re
import json
import urllib.request
from ..game import Game
from .. import config
from ..exceptions import AVENoInternet
from .string_functions import clean
from .file_parsing import parse_room, parse_item

library_json = None


def load_library_json():
    """Load the list of games in the online library."""
    global library_json
    try:
        if library_json is None:
            library_json = []
            with urllib.request.urlopen(
                    "https://avegame.co.uk/gamelist.json") as f:
                for game in json.load(f):
                    game["ave_version"] = tuple(game["ave_version"])
                    if game["user"]:
                        if game["ave_version"] <= config.version_tuple:
                            library_json.append(game)
    except:  # noqa: E722
        raise AVENoInternet
    return library_json


def load_full_game(text):
    """Parse the full game text."""
    rooms = {}
    for room in re.split(r"(^|\n)#", text)[1:]:
        room_id, room = re.split(r"(^|\n)%", room)[0].split("\n", 1)
        room_id = clean(room_id)
        if room_id != "":
            rooms[room_id] = parse_room(room_id, room)

    items = {}
    for item in re.split(r"(^|\n)%", text)[1:]:
        item_id, item = re.split(r"(^|\n)#", item)[0].split("\n", 1)
        item_id = clean(item_id)
        if item_id != "":
            items[item_id] = parse_item(item_id, item)

    return rooms, items


def load_game_from_file(file, filename=None):
    """Load the metadata of a game from a file."""
    title = "untitled"
    number = None
    description = ""
    author = "anonymous"
    active = True
    version = 0
    ave_version = (0, )
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line.startswith("%"):
                # Preamble has ended
                break
            if line[:2] == "==" == line[-2:]:
                title = clean(line[2:-2])
            if line[:2] == "@@" == line[-2:]:
                number = int(clean(line[2:-2]))
            if line[:2] == "--" == line[-2:]:
                description = clean(line[2:-2])
            if line[:2] == "**" == line[-2:]:
                author = clean(line[2:-2])
            if line[:2] == "vv" == line[-2:]:
                version = int(line[2:-2])
            if line[:2] == "::" == line[-2:]:
                ave_version = tuple(int(i) for i in line[2:-2].split("."))
            if line[:2] == "~~" == line[-2:]:
                if clean(line[2:-2]) == "off":
                    active = False

    return Game(file=file, filename=filename, title=title, number=number,
                description=description, author=author, active=active,
                version=version, ave_version=ave_version)


def load_game_from_library(n):
    """Load the metadata of a game from the online library."""
    info = load_library_json()[n]
    print(info)
    return Game(url="https://avegame.co.uk/download/user/" + info["filename"],
                title=info["title"], description=info["desc"],
                author=info["author"], active=info["active"],
                number=info["number"])


def load_full_game_from_file(file):
    """Load the full game from a file."""
    with open(file) as f:
        return load_full_game(f.read())


def load_full_game_from_url(url):
    """Load the full game from the online library."""
    with urllib.request.urlopen(url) as f:
        return load_full_game(f.read().decode('utf-8'))
