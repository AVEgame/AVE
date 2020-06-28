import re
from .game import Game, Room, attrs


def _replacements(string):
    import os
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "../VERSION")) as f:
        v = f.read().strip()
    string = v.join(string.split("%v%"))
    return string


def clean(string):
    return _replacements(string.strip())


def unescaped(line):
    pattern = re.compile(r"<\|.*\|>")
    while pattern.search(line) is not None:
        line = pattern.sub("", line)
    return line


def parse_req(line, id_of_text="text"):
    com = False
    reqs = {a: [] for b, a in attrs.items()}
    for i, c in enumerate(clean(line)):
        if line[i: i + 2] == "<|":
            com = True
        if line[i: i + 2] == "|>":
            com = False
        if not com \
                and line[i: i + 3] in [" + ", " ~ ", " ? "] \
                or line[i: i + 4] == " ?! ":
            reqs[id_of_text] = clean(line[:i])
            req = line[i:]
            break
    else:
        reqs[id_of_text] = clean(line)
        req = ""

    pattern = re.compile(r"(\([^\)]*) ([^\)]*\))")
    while pattern.search(req) is not None:
        req = pattern.sub(r"\1,\2", req)
    pattern2 = re.compile(r" +((=|<|>)=?) +")
    while pattern2.search(req) is not None:
        req = pattern2.sub(r"\1", req)
    lsp = req.split()
    for i in range(len(lsp) - 1):
        for a, b in attrs.items():
            if lsp[i] == a:
                if a in ["?", "?!"]:
                    lsp[i + 1] = lsp[i + 1].replace("(", "")
                    lsp[i + 1] = lsp[i + 1].replace("(", "")
                    lsp[i + 1] = lsp[i + 1].replace(")", "")
                    reqs[b].append(lsp[i + 1].split(","))
                else:
                    reqs[b].append(lsp[i + 1])
    return reqs


def _remove_links(txt):
    pattern = re.compile(r"\[(.*)\]\((.*)\)")
    while pattern.search(txt) is not None:
        txt = pattern.sub(r"\2", txt)
    return txt


def remove_links(txt):
    out = ""
    while "<|" in txt and "|>" in txt:
        tsp = txt.split("<|", 1)
        out += _remove_links(tsp[0])
        if "|>" in tsp[1]:
            ttsp = tsp[1].split("|>", 1)
            out += "<|" + ttsp[0] + "|>"
            txt = ttsp[1]
    out += _remove_links(txt)
    return out


def load_game_from_file(file):
    title = "untitled"
    number = None
    description = ""
    author = "anonymous"
    active = True
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
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

    game = Game(file, title=title, number=number, description=description,
                author=author, active=active)
    return game


def load_game_from_url(url):
    pass


def load_rooms_and_items_from_file(file, screen=None, character=None):
    rooms = {}
    items = {}
    preamb = True
    firstitem = True
    mode = "PREA"
    c_hidden = None
    c_room = None
    c_txt = None
    c_options = None
    c_default = None
    c_number = None
    c_item = None
    c_texts = None
    with open(file) as f:
        for line in f:
            if line[0] == "#" or line[0] == '%':
                if not preamb and mode == "ROOM" and len(c_options) > 0:
                    rooms[c_room] = Room(c_room, c_txt, c_options)
                if not firstitem and mode == "ITEM":
                    items[c_item] = [c_texts, c_hidden, c_number, c_default]
                if line[0] == "#":
                    mode = "ROOM"
                    preamb = False
                    while len(line) > 0 and line[0] == "#":
                        line = line[1:]
                    c_room = clean(line)
                    c_txt = []
                    c_options = []
                elif line[0] == "%":
                    mode = "ITEM"
                    firstitem = False
                    while len(line) > 0 and line[0] == "%":
                        line = line[1:]
                    c_item = clean(line)
                    c_hidden = True
                    c_number = False
                    c_default = None
                    c_texts = []
            elif mode == "ITEM":
                if clean(line) == "__HIDDEN__":
                    c_hidden = True
                if clean(line.split(" ", 1)[0]) == "__NUMBER__":
                    c_number = True
                    try:
                        c_default = int(line.split(" ", 1)[1])
                    except:
                        c_default = 0
                elif clean(line) != "":
                    c_hidden = False
                    next_item = parse_req(line, 'name')
                    c_texts.append(next_item)
            elif mode == "ROOM":
                if "=>" in unescaped(line):
                    lsp = line.split("=>")
                    next_option = parse_req(line)
                    next_option['option'] = clean(lsp[0])
                    lsp = clean(lsp[1]).split()
                    next_option['id'] = clean(lsp[0])
                    c_options.append(next_option)
                elif clean(line) != "":
                    c_txt.append(parse_req(line))
    if not preamb and mode == "ROOM" and len(c_options) > 0:
        rooms[c_room] = Room(c_room, c_txt, c_options)
    if not firstitem and mode == "ITEM":
        items[c_item] = [c_texts, c_hidden, c_number, c_default]
    return rooms, items
