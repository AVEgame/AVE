def clean(string):
    while len(string) > 0 and string[0] == " ":
        string = string[1:]
    while len(string) > 0 and string[-1] == " ":
        string = string[:-1]
    return clean_newlines(string)

def clean_newlines(string):
    while "\n" in string:
        string = string.strip("\n")
    return string

def comment(string):
    while len(string) > 0 and clean(string)[0] == "#":
        string = string[1:]
    return clean(string)
