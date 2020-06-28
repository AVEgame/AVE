# For internal use
def _clean_newlines(string):
    while "\n" in string:
        string = string.strip("\n")
    return string


def _clean(string):
    string = _clean_newlines(string)
    while len(string) > 0 and string[0] == " ":
        string = string[1:]
    while len(string) > 0 and string[-1] == " ":
        string = string[:-1]
    string = _clean_newlines(string)
    return string


def _replacements(string):
    import os
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "../VERSION")) as f:
        v = _clean(f.read())
    string = v.join(string.split("%v%"))
    return string


# For public use
def clean(string):
    string = _clean(string)
    string = _replacements(string)
    return string


def clean_newlines(string):
    string = _clean_newlines(string)
    string = _replacements(string)
    return string


def comment(string):
    string = _clean_newlines(string)
    while len(string) > 0 and _clean(string)[0] == "#":
        string = string[1:]
    string = _clean(string)
    string = _replacements(string)
    return string
