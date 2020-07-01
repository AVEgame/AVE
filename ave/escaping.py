import re
from . import config

symbols = {
    "!?": "IINNTTEERROOBBAANNGG",
    "=>": "AARROOWW",
    "?": "QQUUEESSTTIIOONN",
    "+": "PPLLUUSS",
    "~": "TTIILLDDEE",
    "=": "EEQQUUAALL",
    "-": "DDAASSHH",
    "*": "AASSTTEERRIISSKK",
    "@": "AATT",
    "%": "PPEERRCCEENNTT",
    "#": "HHAASSHH",
    "_": "UUNNDDEERRSCCOORREE",
    "[": "OOPPEENNSQ",
    "]": "CCLLOOSSEESQ",
    "(": "OOPPEENNRO",
    ")": "CCLLOOSSEERO",
    "<": "OOPPEENNPO",
    ">": "CCLLOOSSEEPO"
}

more_symbols = {
    "$": "DDOOLLAARR"
}


def between(text, pre, post):
    if pre not in text or post not in text:
        return ""
    else:
        return text.split(pre, 1)[1].split(post, 1)[0]


def _replacements(string):
    string = config.version.join(string.split("%v%"))
    return string


def remove_links(txt):
    return re.sub(r"\[(.*)\]\((.*)\)", r"\2", txt)


def clean(string):
    string = string.replace("<newline>", "\n")
    return _replacements(string.strip())


def clean_newlines(string):
    return _replacements(string.strip("\n"))


def _escape(matches):
    text = matches[1]
    for i, j in symbols.items():
        text = text.replace(i, j)
    for i, j in more_symbols.items():
        text = text.replace(i, j)
    return text


def escape(line):
    return re.sub(r"<\|(.*?)\|>", _escape, line)


def unescape(text):
    for i, j in symbols.items():
        text = text.replace(j, i)
    return text


def more_unescape(text):
    for i, j in more_symbols.items():
        text = text.replace(j, i)
    return text
