"""Functions to manipulate strings."""

import re
from . import config

symbols = {
    "!?": "SYMBOLIINNTTEERROOBBAANNGG",
    "=>": "SYMBOLAARROOWW",
    "?": "SYMBOLQQUUEESSTTIIOONN",
    "+": "SYMBOLPPLLUUSS",
    "~": "SYMBOLTTIILLDDEE",
    "=": "SYMBOLEEQQUUAALL",
    "-": "SYMBOLDDAASSHH",
    "*": "SYMBOLAASSTTEERRIISSKK",
    "/": "SYMBOLFFWWDDSSLLAASSHH",
    "@": "SYMBOLAATT",
    "%": "SYMBOLPPEERRCCEENNTT",
    "#": "SYMBOLHHAASSHH",
    "_": "SYMBOLUUNNDDEERRSCCOORREE",
    "[": "SYMBOLOOPPEENNSQ",
    "]": "SYMBOLCCLLOOSSEESQ",
    "(": "SYMBOLOOPPEENNRO",
    ")": "SYMBOLCCLLOOSSEERO",
    "<": "SYMBOLOOPPEENNPO",
    ">": "SYMBOLCCLLOOSSEEPO"
}

more_symbols = {
    "$": "SYMBOLDDOOLLAARR"
}


def between(text, pre, post):
    """Get the part of a string between two substrings.

    Parameters
    ----------
    test : string
        The string to search
    pre : string
        The substring before the selection.
    post : string
        The substring after the selection.

    Returns
    -------
    string
        The text between the substrings, or an empty string if not found
    """
    if pre not in text or post not in text:
        return ""
    else:
        return text.split(pre, 1)[1].split(post, 1)[0]


def _replacements(txt):
    txt = config.version.join(txt.split("%v%"))
    return txt


def clean(txt):
    """Strip spaces and newlines and insert data."""
    txt = txt.replace("<newline>", "\n")
    return _replacements(txt.strip())


def clean_newlines(txt):
    """Strip newlines and insert data such as the AVE version number."""
    txt = txt.replace("<newline>", "\n")
    return _replacements(txt.strip("\n"))


def _escape(matches):
    text = matches[1]
    for i, j in symbols.items():
        text = text.replace(i, j)
    for i, j in more_symbols.items():
        text = text.replace(i, j)
    return text


def escape(txt):
    """Escape text between <| and |>."""
    return re.sub(r"<\|(.*?)\|>", _escape, txt)


def unescape(text):
    """Restore text between <| and |> that was escaped."""
    for i, j in symbols.items():
        text = text.replace(j, i)
    return text


def more_unescape(text):
    """Restore final bits of text between <| and |> that was escaped.

    These are done later as they would otherwise be changed when getting
    room text. For example <| $variable$ |> would be replaces with the
    variable value if it was unescaped earlier.
    """
    for i, j in more_symbols.items():
        text = text.replace(j, i)
    return text
