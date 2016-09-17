from __future__ import division
from core.utils import *
from core.errors import *
import re
attrs = {"+":"adds","?":"needs","?!":"unneeds","~":"rems"}

def parse_req(line):
    pattern = re.compile("(\([^\)]*) ([^\)]*\))")
    while pattern.search(line) is not None:
        line = pattern.sub(r"\1,\2",line)
    pattern2 = re.compile(" +(<|>=?) +")
    while pattern2.search(line) is not None:
        line = pattern2.sub(r"\1",line)
    lsp = line.split()
    reqs = {a:[] for b,a in attrs.items()}
    for i in range(len(lsp)-1):
        for a,b in attrs.items():
            if lsp[i] == a:
                if a in ["?","?!"]:
                    lsp[i+1] = lsp[i+1].replace("(","")
                    lsp[i+1] = lsp[i+1].replace(")","")
                    reqs[b].append(lsp[i+1].split(","))
                else:
                    reqs[b].append(lsp[i+1])
    return reqs


class Item:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def get_name(self):
        if self.name in self.character.items:
            name = []
            for line in self.character.items[self.name][0]:
                if self.character.has(line['needs']) and self.character.unhas(line['unneeds']):
                    #self.character.add_items(line['adds'])
                    #self.character.remove_items(line['rems'])
                    name.append(line['name'])
            name = " ".join(name)
            if name != "":
                return name
        return self.name

    def is_hidden(self):
        if self.name in self.character.items:
            return self.character.items[self.name][1]
        return True

class Character:
    def __init__(self, screen):
        self.items = []
        self.screen = screen
        self.reset()

    def set_items(self, items):
        self.items = items
        self.reset_numbers()

    def reset_numbers(self):
        self.numbers = {}
        for i in self.items:
            if self.is_number(i):
                self.numbers[i] = [self.items[i][3],Item(i,self)]

    def reset(self):
        self.inventory = []
        self.name = ""
        self.reset_numbers()

    def _add_item(self, item):
        if self.is_number(item):
            self.numbers[item][0] += 1
        else:
            self.inventory.append(Item(item,self))

    def _remove_item(self, item):
        if self.is_number(item):
            self.numbers[item][0] -= 1
        elif item in self.inventory_ids():
            for a,b in enumerate(self.inventory):
                if b.name == item:
                    self.inventory = self.inventory[:a] + self.inventory[a+1:]
                    break

    def add_items(self, items):
        for item in items:
            self._add_item(item)

    def remove_items(self, items):
        for item in items:
            self._remove_item(item)

    def has(self, item):
        if type(item) == list:
            for a in item:
                for b in a:
                    if self._has(b):
                        break
                    if b[0]=="!" and not self._has(b[1:]):
                        break
                else:
                    return False
            return True
        return self._has(item)

    def _has(self, item):
        if self.is_number(item):
            if ">=" in item:
                return self.numbers[item.split(">=",1)[0]][0] >= int(item.split(">=",1)[1])
            elif "<=" in item:
                return self.numbers[item.split("<=",1)[0]][0] <= int(item.split("<=",1)[1])
            elif ">" in item:
                return self.numbers[item.split(">",1)[0]][0] > int(item.split(">",1)[1])
            elif "<" in item:
                return self.numbers[item.split("<",1)[0]][0] < int(item.split("<",1)[1])
            else:
                return self.numbers[item][0] > 0
        else:
            return item in self.inventory_ids()

    def unhas(self, item):
        if type(item) == list:
            for a in item:
                for b in a:
                    if not self._has(b):
                        break
                    if b[0]=="!" and self._has(b):
                        break
                else:
                    return False
            return True
        return not self._has(item)

    def is_number(self, item):
        if item in self.items:
            return self.items[item][2]
        for s in ["<",">"]:
            if item.split(s,1)[0] in self.items:
                return self.items[item.split(s,1)[0]][2]
        return False

    def show_inventory(self):
        inv = []
        for n,item in self.numbers.values():
            inv.append(item.get_name()+": "+str(n))
        for i in self.inventory:
            if not i.is_hidden():
                inv.append(i.get_name())
        self.screen.show_inventory(inv)

    def inventory_ids(self):
        return [item.name for item in self.inventory]

class AVE:
    def __init__(self, folder="games"):
        from screen import Screen
        self.screen = Screen()
        self.character = Character(self.screen)
        self.games = Games(folder, self.screen, self.character)

    def start(self):
        self.show_title_screen()

    def show_title_screen(self):
        self.screen.print_titles()
        game_to_load = self.screen.menu(self.games.titles()+["- user contributed games -"], 8, titles=True)
        if game_to_load == len(self.games.titles()):
            self.show_download_menu()
        else:
            the_game = self.games[game_to_load]
            self.run_the_game(the_game)

    def show_download_menu(self):
        try:
            def downloadavefile(file):
                return urllib2.urlopen("http://avegame.co.uk/download/"+file).readlines()

            self.screen.print_download()
            import json
            import urllib2
            try:
                the_json = json.load(urllib2.urlopen("http://avegame.co.uk/gamelist.json"))
                menu_items = []
                for key,value in the_json.items():
                    if 'user/' in key:#value['user']:
                        menu_items.append([value['title'],value['author'],key])
                game_n = self.screen.menu([a[0]+' by '+a[1] for a in menu_items],12)
                the_game = Game(downloadavefile, self.screen, self.character, menu_items[game_n][2])
                self.run_the_game(the_game)
            except urllib2.URLError:
                self.no_internet()
                raise AVEToMenu
        except AVEToMenu:
            self.show_title_screen()

    def no_internet(self):
        self.screen.no_internet()
        self.screen.menu([],1)

    def run_the_game(self, the_game):
        the_game.load()
        again = True
        while again:
            again = False
            try:
                the_game.begin()
            except AVEGameOver:
                next = self.screen.gameover()
                self.character.reset()
                if next == 0:
                    again = True
                if next == 2:
                    raise AVEQuit
            except AVEWinner:
                next = self.screen.winner()
                self.character.reset()
                if next == 0:
                    again = True
                if next == 2:
                    raise AVEQuit
            except AVEToMenu:
                pass

    def exit(self):
        self.screen.close()

class Games:
    def __init__(self, folder, screen, character):
        import os
        self.screen = screen
        self.character = character
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("..",folder))
        self.games = []
        def avefile(path):
            with open(path) as f:
                return f.readlines()
        for game in os.listdir(self.path):
            if ".ave" in game:
                g = Game(avefile, self.screen, self.character, os.path.join(self.path,game))
                if g.active:
                    self.games.append(g)

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
    def __init__(self, avefile, screen, character, *args):
        self.screen = screen
        self.character = character
        self.avefile = avefile
        self.title = ""
        self.description = ""
        self.author = ""
        self.active = True
        self.rooms = {}
        self.args = args
        for line in avefile(*args):
            line = clean(line)
            if len(line) > 0 and line[0] == "#":
                break
            if line[:2] == "==" == line[-2:]:
                self.title = clean(line[2:-2])
            if line[:2] == "--" == line[-2:]:
                self.description = clean(line[2:-2])
            if line[:2] == "**" == line[-2:]:
                self.author = clean(line[2:-2])
            if line[:2] == "~~" == line[-2:]:
                if clean(line[2:-2]) == "off":
                   self.active = False

    def load(self):
        self.screen.clear()
        rooms = {}
        items = {}
        preamb = True
        firstitem = True
        mode = "PREA"
        for line in self.avefile(*self.args) + ['#']:
                if line[0]=="#" or line[0] == '%':
                    if not preamb and mode == "ROOM" and len(c_options) > 0:
                        rooms[c_room] = Room(c_room, c_txt, c_options, self.screen, self.character)
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
                    elif line[0]=="%":
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
                    if clean(line.split(" ",1)[0]) == "__NUMBER__":
                        c_number = True
                        try:
                            c_default = int(line.split(" ",1)[1])
                        except:
                            c_default = 0
                    elif clean(line) != "":
                        c_hidden = False
                        next_item = parse_req(line)
                        text = line
                        for a in attrs:
                            text = text.split(" "+a)[0]
                        next_item['name'] = clean(text)
                        c_texts.append(next_item)
                elif mode == "ROOM":
                    if "=>" in line:
                        lsp = line.split("=>")
                        next_option = parse_req(line)
                        next_option['option'] = clean(lsp[0])
                        lsp = clean(lsp[1]).split()
                        next_option['id'] = clean(lsp[0])
                        c_options.append(next_option)
                    elif clean(line) != "":
                        next_line = parse_req(line)
                        text = line
                        for a in attrs:
                            text = text.split(" "+a)[0]
                        next_line['text'] = clean(text)
                        c_txt.append(next_line)
        self.rooms = rooms
        self.character.set_items(items)

    def __getitem__(self, id):
        return self.load_room(id)

    def load_room(self, id):
        if id == "__GAMEOVER__":
            raise AVEGameOver
        if id == "__WINNER__":
            raise AVEWinner
        if id in self.rooms:
            return self.rooms[id]
        else:
            return self.fail_room()

    def begin(self):
        import curses
        self.show_title()
        room = self['start']
        while True:
            self.screen.clear()
            self.screen.put_ave_logo()
            next = room.show()
            room = self[next]

    def fail_room(self):
        options = [{'id':"__GAMEOVER__",'option':"Continue",'needs':[],'unneeds':[],'adds':[],'rems':[]}]
        text = [{'text':"You fall off the edge of the game... (404 Error)",'needs':[],'unneeds':[],'adds':[],'rems':[]}]
        return Room("fail", text, options, self.screen, self.character)

    def show_title(self):
        self.screen.show_titles(self.title, self.description, self.author)

class Room:
    def __init__(self, id, text, options, screen, character):
        self.id = id
        self.text = text
        self.options = options
        self.screen = screen
        self.character = character

    def __str__(self):
        return "Room with id " + self.id

    def show(self):
        from core.screen import WIDTH
        included_lines = []
        for line in self.text:
            if self.character.has(line['needs']) and self.character.unhas(line['unneeds']):
                self.character.add_items(line['adds'])
                self.character.remove_items(line['rems'])
                included_lines.append(line['text'])
        y = 0
        x = 0
        stuff = []
        text = " ".join(included_lines)
        for item,value in self.character.numbers.items():
            text = str(value[0]).join(text.split("$"+item+"$"))
        for word in text.split():
            if word=="<newline>":
                y+= 1
                x = 0
            else:
                if x+len(word) > WIDTH-22:
                    y += 1
                    x = 0
                for i,c in enumerate(word):
                    stuff.append((y,x,c))
                    x += 1
                stuff.append((y,x," "))
                x += 1
        self.screen.type(stuff)

        opts = []
        adds = []
        rems = []
        ids = []
        for option in self.options:
            if self.character.has(option['needs']) and self.character.unhas(option['unneeds']):
                opts.append(option['option'])
                adds.append(option['adds'])
                rems.append(option['rems'])
                ids.append(option['id'])
        self.character.show_inventory()
        num = self.screen.menu(opts, add=adds, rem=rems, y=min(8,len(opts)), character=self.character)
        return ids[num]

