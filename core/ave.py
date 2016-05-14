from __future__ import division
from core.utils import *
from core.errors import *

class AVE:
    def __init__(self, folder="games"):
        from screen import Screen
        self.screen = Screen()
        self.games = Games(folder, self.screen)

    def start(self):
        self.screen.print_titles()
        game_to_load = self.screen.menu(self.games.titles(), 8)
        self.games[game_to_load].load()
        again = True
        while again:
            again = False
            try:
                self.games[game_to_load].begin()
            except AVEGameOver:
                next = self.screen.gameover()
                if next == 0:
                    again = True
                if next == 2:
                    raise AVEQuit
                

    def exit(self):
        self.screen.close()

class Games:
    def __init__(self, folder, screen):
        import os
        self.screen = screen
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("..",folder))
        self.games = []
        for game in os.listdir(self.path):
            if ".ave" in game:
                self.games.append(Game(os.path.join(self.path,game), self.screen))

    def titles(self):
        return [g.title for g in self.games]

    def descriptions(self):
        return [g.description for g in self.games]

    def titles_and_descriptions(self):
        return zip(self.titles(),self.descriptions())

    def game(self,n):
        return self.games[n]

    def __getitem__(self,n):
        return self.games[n]

class Game:
    def __init__(self, path, screen):
        self.screen = screen
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
                        rooms[c_room] = Room(c_room, " ".join(c_txt), c_opts, self.screen)
                    preamb = False
                    while len(line) > 0 and line[0] in ["#"]:
                        line = line[1:]
                    c_room = clean(line)
                    c_txt = []
                    c_opts = {}
                elif not preamb and clean(line) != "":
                    if "=>" in line:
                        lsp = line.split("=>")
                        c_opts[clean(lsp[1])] = clean(lsp[0])
                    else:
                        c_txt.append(clean(line))
        self.rooms = rooms

    def __getitem__(self, id):
        return self.load_room(id)

    def load_room(self, id):
        if id == "__GAMEOVER__":
            raise AVEGameOver
        try:
            return self.rooms[id]
        except KeyError:
            return self.fail_room()

    def begin(self):
        room = self['start']
        while True:
            next = room.show()
            room = self[next]

    def fail_room(self):
        return Room("fail", "You fall off the edge of the game. GAME OVER", {"__GAMEOVER__":"Continue"}, self.screen)


class Room:
    def __init__(self, id, text, options, screen):
        self.id = id
        self.text = text
        self.options = []
        self.option_keys = []
        for a,b in options.items():
            self.option_keys.append(a)
            self.options.append(b)
        self.screen = screen

    def __str__(self):
        return "Room with id " + self.id

    def show(self):
        from core.screen import WIDTH
        stuff = []
        for i,c in enumerate(self.text):
            stuff.append((i // WIDTH, i % WIDTH, c))
        self.screen.type(stuff)

        num = self.screen.menu(self.options, min(8,len(self.options)))
        return self.option_keys[num]
