import re
import os
import json
import urllib.request
from .game import Game, Room, Item, Number
from .game import (TextWithRequirements, OptionWithRequirements,
                   NameWithRequirements)
from .ave_format import symbols, attributes


def _replacements(string):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "../VERSION")) as f:
        v = f.read().strip()
    string = v.join(string.split("%v%"))
    return string


def remove_links(txt):
    return re.sub(r"\[(.*)\]\((.*)\)", r"\2", txt)


def clean(string):
    return _replacements(string.strip())


def _escape(matches):
    text = matches[1]
    for i, j in symbols.items():
        text = text.replace(i, j)
    return text


def escape(line):
    return re.sub(r"<\|(.*)\|>", _escape, line)


def unescape(text):
    for i, j in symbols.items():
        text = text.replace(j, i)
    return text


def parse_requirements(req, id_of_text="text"):
    reqs = {a: [] for a in attributes.values()}
    pattern = re.compile(r"(\([^\)]*) ([^\)]*\))")
    while pattern.search(req) is not None:
        req = pattern.sub(r"\1,\2", req)
    pattern2 = re.compile(r" +((=|<|>)=?) +")
    while pattern2.search(req) is not None:
        req = pattern2.sub(r"\1", req)
    lsp = req.split()
    for i in range(len(lsp) - 1):
        for a, b in attributes.items():
            if lsp[i] == a:
                if a in ["?", "?!"]:
                    lsp[i + 1] = lsp[i + 1].replace("(", "")
                    lsp[i + 1] = lsp[i + 1].replace("(", "")
                    lsp[i + 1] = lsp[i + 1].replace(")", "")
                    reqs[b].append(lsp[i + 1].split(","))
                else:
                    reqs[b].append(lsp[i + 1])
    return reqs


def parse_line(line):
    i = min([line.index(a) if a in line else len(line) for a in
             [" " + b + " " for b in attributes]])
    text = unescape(clean(line[:i]))
    reqs = parse_requirements(line[i:])
    return text, reqs


def parse_option(line):
    text, rest = line.split("=>", 1)
    test = unescape(clean(text))
    destination, req = (rest.strip() + " ").split(" ", 1)
    destination = clean(destination)
    reqs = parse_requirements(req)
    return OptionWithRequirements(text=text, destination=destination, **reqs)


def parse_text_line(line):
    text, reqs = parse_line(line)
    return TextWithRequirements(text=text, **reqs)


def parse_name_part(line):
    text, reqs = parse_line(line)
    return NameWithRequirements(text=text, **reqs)


def parse_room(id, room):
    room = escape(room)
    text = []
    options = []
    for line in room.split("\n"):
        line = clean(line)
        if "=>" in line:
            options.append(parse_option(line))
        elif clean(line) != "":
            text.append(parse_text_line(line))
    return Room(id=id, text=text, options=options)


def parse_item(id, item):
    item = escape(item)
    hidden = None
    number = False
    default = None
    names = []
    for line in item.split("\n"):
        line = clean(line)
        if line.startswith("__HIDDEN__"):
            hidden = True
        elif line.startswith("__NUMBER__"):
            number = True
            if "(" in line:
                try:
                    default = int(line.split("(", 1)[1].split(")")[0])
                except ValueError:
                    default = 0
        elif line != "":
            if hidden is None:
                hidden = False
            names.append(parse_name_part(line))
    if number:
        return Number(id=id, names=names, hidden=hidden, default=default)
    else:
        return Item(id=id, names=names, hidden=hidden)


def load_full_game(text):
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


def load_game_from_file(file):
    title = "untitled"
    number = None
    description = ""
    author = "anonymous"
    active = True
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
            if line[:2] == "~~" == line[-2:]:
                if clean(line[2:-2]) == "off":
                    active = False

    return Game(file=file, title=title, number=number,
                description=description,
                author=author, active=active)


def load_game_from_library(url):
    info = load_library_json()[url]
    return Game(url="http://avegame.co.uk/download/" + url,
                title=info["title"], description=info["desc"],
                author=info["author"], active=info["active"],
                number=info["n"])


library_json = None


def load_library_json():
    global library_json
    if library_json is None:
        with urllib.request.urlopen(
                "http://avegame.co.uk/gamelist.json") as f:
            library_json = json.load(f)
    return library_json


def load_full_game_from_file(file):
    with open(file) as f:
        return load_full_game(f.read())


def load_full_game_from_url(url):
    with urllib.request.urlopen(url) as f:
        return load_full_game(f.read().decode('utf-8'))
