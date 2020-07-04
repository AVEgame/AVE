"""Parsing a .ave file."""

import re
from .game import Room
from .components import (TextWithRequirements, OptionWithRequirements,
                         NameWithRequirements)
from .string_functions import escape, unescape, clean, between
from .components.items import Item, NumberItem
from .components import requirements as rq
from .components import item_giver as ig
from .components import numbers as no


def _parse_rq(condition):
    """Parse a requirement."""
    if condition.startswith("(") and condition.endswith(")"):
        return rq.Or(*[_parse_rq(i) for i in condition[1:-1].split(",")])
    if condition.startswith("!"):
        return rq.Not(_parse_rq(condition[1:]))
    if ">" in condition or "<" in condition or "=" in condition:
        for sign in [">=", "<=", "==", "<", ">", "="]:
            if sign in condition:
                n, val = condition.split(sign, 1)
                return rq.RequiredNumber(
                    _parse_value(n), sign, _parse_value(val))
    return rq.RequiredItem(condition)


def _parse_value(value):
    """Parse a number or expression."""
    # TODO: Brackets in expression (use escaping)
    if "+" in value:
        if value[0] == "-":
            value = "0+" + value
        if "-" in value:
            value = value.replace("-", "+-")
        return no.Sum(*[_parse_value(v) for v in value.split("+")])
    if value.startswith("-"):
        return no.Negative(_parse_value(value[1:]))

    if "*" in value:
        return no.Product(*[_parse_value(v) for v in value.split("*")])
    if "/" in value:
        return no.Division(*[_parse_value(v) for v in value.split("/")])

    if re.match(r"^[0-9]+$", value):
        return no.Constant(int(value))
    if re.match(r"^[0-9\.]+$", value):
        return no.Constant(float(value))

    if "__R__" == value:
        return no.Random()
    if value.startswith("__R__("):
        return no.Random(*[_parse_value(i)
                           for i in between(value, "(", ")").split(",")])

    return no.Variable(value)


def _parse_ig_add(item):
    """Parse an addition of an item, or addition to a number."""
    if "=" in item:
        n, value = item.split("=", 1)
        return ig.Set(n, _parse_value(value))
    if "+" in item:
        n, value = item.split("+", 1)
        return ig.Add(n, _parse_value(value))
    if "-" in item:
        n, value = item.split("-", 1)
        return ig.Remove(n, _parse_value(value))
    return ig.Add(item)


def _parse_ig_remove(item):
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
            needs = rq.And(needs, _parse_rq(j))
        elif i == "?!":
            needs = rq.And(needs, rq.Not(_parse_rq(j)))
        elif i == "+":
            items.append(_parse_ig_add(j))
        elif i == "~":
            items.append(_parse_ig_remove(j))
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
    """Parse a line with a destination option."""
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
                    default = _parse_value(line.split("(", 1)[1].split(")")[0])
                except ValueError:
                    default = no.Constant(0)
        elif line != "":
            if hidden is None:
                hidden = False
            names.append(parse_name_part(line))
    if number:
        return NumberItem(id=id, names=names, hidden=hidden, default=default)
    else:
        return Item(id=id, names=names, hidden=hidden)
