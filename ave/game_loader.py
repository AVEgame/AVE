"""Parsing a .ave file."""

import re
import json
import urllib.request
from .game import Game, Room
from .game import (TextWithRequirements, OptionWithRequirements,
                   NameWithRequirements)
from .escaping import escape, unescape, clean, between
from .items import Item, Number
from . import requirements as rq
from . import item_giver as ig
from . import numbers as no

library_json = None


def load_library_json():
    """Load the list of games in the online library."""
    global library_json
    if library_json is None:
        with urllib.request.urlopen(
                "http://avegame.co.uk/gamelist.json") as f:
            library_json = json.load(f)
    return library_json


def parse_rq(condition):
    """Parse a requirement."""
    if condition.startswith("(") and condition.endswith(")"):
        return rq.Or(*[parse_rq(i) for i in condition[1:-1].split(",")])
    if condition.startswith("!"):
        return rq.Not(parse_rq(condition[1:]))
    if ">" in condition or "<" in condition or "=" in condition:
        for sign in [">=", "<=", "==", "<", ">", "="]:
            if sign in condition:
                n, val = condition.split(sign, 1)
                return rq.RequiredNumber(
                    parse_value(n), sign, parse_value(val))
    return rq.RequiredItem(condition)


def parse_value(value):
    """Parse a number or expression."""
    # TODO: Brackets in expression (use escaping)
    if "+" in value:
        if value[0] == "-":
            value = "0+" + value
        if "-" in value:
            value = value.replace("-", "+-")
        return no.Sum(*[parse_value(v) for v in value.split("+")])
    if value.startswith("-"):
        return no.Negative(parse_value(value[1:]))

    if "*" in value:
        return no.Product(*[parse_value(v) for v in value.split("*")])
    if "/" in value:
        return no.Division(*[parse_value(v) for v in value.split("/")])

    if re.match(r"^[0-9]+$", value):
        return no.Constant(int(value))
    if re.match(r"^[0-9\.]+$", value):
        return no.Constant(float(value))

    if "__R__" == value:
        return no.Random()
    if value.startswith("__R__("):
        return no.Random(*[parse_value(i)
                           for i in between(value, "(", ")").split(",")])

    return no.Variable(value)


def parse_ig_add(item):
    """Parse an addition of an item, or addition to a number."""
    if "=" in item:
        n, value = item.split("=", 1)
        return ig.Set(n, parse_value(value))
    if "+" in item:

        n, value = item.split("+", 1)
        return ig.Add(n, parse_value(value))
    if "-" in item:
        n, value = item.split("-", 1)
        return ig.Remove(n, parse_value(value))
    return ig.Add(item)


def parse_ig_remove(item):
    """Parse the removal of an item."""
    return ig.Remove(item)


def parse_requirements(req, id_of_text="text"):
    """Parse the requirements of a line."""
    items = []
    needs = rq.Satisfied()
    pattern = re.compile(r"(\([^\)]*) ([^\)]*\))")
    while pattern.search(req) is not None:
        req = pattern.sub(r"\1,\2", req)
    pattern2 = re.compile(r" +((=|<|>)=?) +")
    while pattern2.search(req) is not None:
        req = pattern2.sub(r"\1", req)
    lsp = req.split()
    for i, j in zip(lsp[:-1:2], lsp[1::2]):
        if i == "?":
            needs = rq.And(needs, parse_rq(j))
        elif i == "?!":
            needs = rq.And(needs, rq.Not(parse_rq(j)))
        elif i == "+":
            items.append(parse_ig_add(j))
        elif i == "~":
            items.append(parse_ig_remove(j))
        else:
            raise ValueError("Unknown symbol")
    return items, needs


def parse_line(line):
    """Parse a line in a .ave file."""
    i = min([line.index(a) if a in line else len(line) for a in
             [" ? ", " ?! ", " + ", " ~ "]])
    text = unescape(clean(line[:i]))
    items, needs = parse_requirements(line[i:])
    return text, items, needs


def parse_option(line):
    """Parse an destination option."""
    text, rest = line.split("=>", 1)
    text = unescape(clean(text))
    dest, req = (rest.strip() + " ").split(" ", 1)
    dest = dest.strip()
    items, needs = parse_requirements(req)
    if dest.startswith("__R__"):
        dests = [unescape(clean(i)) for i in
                 between(dest, "(", ")").split(",")]
        if "[" in dest:
            random = [int(i) for i in between(dest, "[", "]").split(",")]
        else:
            random = [1 for d in dests]
        return OptionWithRequirements(
            text=text, destination=dests, random=random,
            items=items, needs=needs)
    else:
        return OptionWithRequirements(
            text=text, destination=dest, items=items, needs=needs)


def parse_text_line(line):
    """Parse a line of text."""
    text, items, needs = parse_line(line)
    return TextWithRequirements(text=text, items=items, needs=needs)


def parse_name_part(line):
    """Parse the name of an item."""
    text, items, needs = parse_line(line)
    return NameWithRequirements(text=text, items=items, needs=needs)


def parse_room(id, room):
    """Parse a room."""
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
    """Parse an item."""
    item = escape(item)
    hidden = None
    number = False
    default = no.Constant(0)
    names = []
    for line in item.split("\n"):
        line = clean(line)
        if line.startswith("__HIDDEN__"):
            hidden = True
        elif line.startswith("__NUMBER__"):
            number = True
            if "(" in line:
                try:
                    default = parse_value(line.split("(", 1)[1].split(")")[0])
                except ValueError:
                    default = no.Constant(0)
        elif line != "":
            if hidden is None:
                hidden = False
            names.append(parse_name_part(line))
    if number:
        return Number(id=id, names=names, hidden=hidden, default=default)
    else:
        return Item(id=id, names=names, hidden=hidden)


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


def load_game_from_library(url):
    """Load the metadata of a game from the online library."""
    info = load_library_json()[url]
    return Game(url="http://avegame.co.uk/download/" + url,
                title=info["title"], description=info["desc"],
                author=info["author"], active=info["active"],
                number=info["n"])


def load_full_game_from_file(file):
    """Load the full game from a file."""
    with open(file) as f:
        return load_full_game(f.read())


def load_full_game_from_url(url):
    """Load the full game from the online library."""
    with urllib.request.urlopen(url) as f:
        return load_full_game(f.read().decode('utf-8'))
