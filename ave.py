class Games:
    def __init__(self, folder):
        import os
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder)
        self.games = []
        for game in os.listdir(self.path):
            if ".ave" in game:
                self.games.append(Game(os.path.join(self.path,game)))

    def titles(self):
        return [g.title for g in self.games]

    def descriptions(self):
        return [g.description for g in self.games]

    def titles_and_descriptions(self):
        return zip(self.titles(),self.descriptions())

    def game(self,n):
        return self.games[n]

class Game:
    def __init__(self, path):
        self.path = path
        self.title = ""
        self.description = ""
        self.rooms = {}
        with open(path) as f:
            for line in f.readlines():
                line = clean(line)
                if len(line) > 0 and line[0] == "#":
                    break
                if line[:2] == "==" == line[-2:]:
                    self.title = clean(line[2:-2])
                if line[:2] == "--" == line[-2:]:
                    self.description = clean(line[2:-2])

    def load(self):
        rooms = {}
        preamb = True
        with open(self.path) as f:
            for line in f.readlines() + ["#"]:
                if line[0]=="#":
                    if not preamb:
                        rooms[c_room] = Room(c_room, " ".join(c_txt), c_opts)
                    preamb = False
                    while len(line) > 0 and line[0] in ["#"]:
                        line = line[1:]
                    c_room = clean(line)
                    c_txt = []
                    c_opts = {}
                elif not preamb and clean(line) != "":
                    if "=>" in line:
                        lsp = line.split("=>")
                        c_opts[clean(lsp[0])] = clean(lsp[1])
                    else:
                        c_txt.append(clean(line))
        self.rooms = rooms

    def load_room(self, id):
        try:
            return self.room[id]
        except IndexError:
            return fail_room

class Room:
    def __init__(self, id, text, options, gameover=False):
        self.id = id
        self.text = text
        self.options = options
        self.gameover = gameover

    def __str__(self):
        return "Room with id " + self.id

fail_room = Room("","You fall off the edge of the game. GAME OVER",{},True)

def clean(string):
    while len(string) > 0 and string[0] == " ":
        string = string[1:]
    while len(string) > 0 and string[-1] == " ":
        string = string[:-1]
    while "\n" in string:
        string = string.strip("\n")
    return string
