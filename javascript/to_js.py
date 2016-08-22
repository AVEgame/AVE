attrs = {"+":"adds","?":"needs","?!":"unneeds","~":"rems"}

def get_game_info(txt):
    active = True
    for line in [l for l in txt.split("\n") if len(l)>0]:
        if line[:2] == "==" == line[-2:]:
            title = clean(line[2:-2])
        if line[:2] == "--" == line[-2:]:
            description = clean(line[2:-2])
        if line[:2] == "**" == line[-2:]:
            author = clean(line[2:-2])
        if line[:2] == "~~" == line[-2:]:
            if clean(line[2:-2]) == "off":
                active = False

    if active:
        return '{"title":"'+title+'","desc":"'+description+'","author":"'+author+'"}'
    else:
        return None



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
    return string

def clean(string):
    string = _clean(string)
    return string
