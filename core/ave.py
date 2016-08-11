import pyb
import gc
import sys
sys.path.append("apps/mscroggs~ave")
from core import utils as u
from core import errors as e

HIDE_INV = False # Change this to toggle hiding the inventory
attrs = {"+":"adds","?":"needs","?!":"unneeds","~":"rems"}

class Item:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        text = self.character.game.find_item(name)
        if text and "__HIDDEN__" in text:
            self.hidden = True
        else:
            self.hidden = False
        if not self.hidden:
            if text [-1] != '\n':
                text += '\n'
            with open('apps/mscroggs~ave/games/current.items', 'a') as f:
                f.write(text)
        text = None
        gc.collect()

    def get_name(self):
        if not self.hidden:
            name = []
            for line in self.get_props():
                if self.character.has(line['needs']) and self.character.unhas(line['unneeds']):
                    name.append(line['name'])
            name = " ".join(name)
            if name != "":
                return name
        return self.name

    def get_props(self):
        text = self.character.game.find_item(self.name, path='apps/mscroggs~ave/games/current.items')
        props = []
        for line in text.split('\n')[1:]:
            if u.clean(line) == "__HIDDEN__":
                pass
            elif u.clean(line) != "":
                next_item = {'name':"",'needs':[],'unneeds':[],'adds':[],'rems':[]}
                text = line
                for a in attrs:
                    text = text.split(" "+a)[0]
                next_item['name'] = u.clean(text)
                lsp = line.split()
                for i in range(len(lsp)-1):
                    for a,b in attrs.items():
                        if lsp[i] == a:
                            next_item[b].append(lsp[i+1])
                props.append(next_item)
        text = None
        gc.collect()
        return props

    def is_hidden(self):
        return self.hidden

class Character:
    def __init__(self, screen):
        self.reset()
        self.screen = screen
        self.items = []

    def reset(self):
        self.inventory = []
        self.name = ""

    def set_game(self, game):
        self.game = game

    def _add_item(self, item):
        self.inventory.append(Item(item,self))

    def _remove_item(self, item):
        if item in self.inventory_ids():
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
                if a not in self.inventory_ids():
                    return False
            return True
        else:
            return item in self.inventory_ids()

    def unhas(self, item):
        if type(item) == list:
            for a in item:
                if a in self.inventory_ids():
                    return False
            return True
        else:
            return item not in self.inventory_ids()

    def show_inventory(self, show=False):
        if not HIDE_INV:
            show = True
        if show:
            inv = []
            for i in self.inventory:
                if not i.is_hidden():
                    inv.append(i.get_name())
        else:
            inv = ['<B> to show']
        self.screen.show_inventory(inv)

    def inventory_ids(self):
        return [item.name for item in self.inventory]

class AVE:
    def __init__(self, folder="games"):
        from core.screen import Screen
        self.screen = Screen()
        self.character = Character(self.screen)
        self.games = Games(folder, self.screen, self.character)

    def start(self):
        with open('apps/mscroggs~ave/games/current.items', 'w') as f:
            f.write('')
        self.screen.print_titles()
        game_to_load = self.screen.menu(self.games.titles(), 5, titles=True)
        self.games[game_to_load].load()
        again = True
        while again:
            again = False
            try:
                self.games[game_to_load].begin()
            except e.AVEGameOver:
                next = self.screen.gameover()
                self.character.reset()
                if next == 0:
                    again = True
                if next == 2:
                    raise e.AVEQuit
            except e.AVEWinner:
                next = self.screen.winner()
                self.character.reset()
                if next == 0:
                    again = True
                if next == 2:
                    raise e.AVEQuit
            except e.AVEToMenu:
                pass

    def exit(self):
        self.screen.close()
        pyb.hard_reset()

class Games:
    def __init__(self, folder, screen, character):
        import os
        self.screen = screen
        self.character = character
        self.path = "apps/mscroggs~ave/games"
        self.games = []
        for game in os.listdir(self.path):
            if ".ave" in game:
                g = MicroGame(self.path+"/"+game, self.screen, self.character)
                if g.active:
                    self.games.append(MicroGame(self.path+"/"+game, self.screen, self.character))

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

class Room:
    def __init__(self, id, text, options, screen, character):
        self.id = id
        self.text = text
        self.options = options
        self.screen = screen
        self.character = character

    def __str__(self):
        return "Room with id " + self.id

    def show(self, show_inv=False):
        from core.screen import WIDTH
        included_lines = []
        for line in self.text:
            if self.character.has(line['needs']) and self.character.unhas(line['unneeds']):
                self.character.add_items(line['adds'])
                self.character.remove_items(line['rems'])
                included_lines.append(line['text'])
        text = " ".join(included_lines)
        self.screen.type(text)

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
        self.character.show_inventory(show=show_inv)
        num = self.screen.menu(opts, add=adds, rem=rems, y=min(8,len(opts)), character=self.character)
        if num == "inv":
            return None
        return ids[num]

class MicroGame:
    def __init__(self, path, screen, character):
        self.screen = screen
        self.character = character
        self.path = path
        self.title = ""
        self.description = ""
        self.author = ""
        self.active = True
        with open(path, 'r') as f:
            for line in f:
                line = u.clean(line)
                if len(line) > 0 and line[0] == "#":
                    break
                if line[:2] == "==" == line[-2:]:
                    self.title = u.clean(line[2:-2])
                if line[:2] == "--" == line[-2:]:
                    self.description = u.clean(line[2:-2])
                if line[:2] == "**" == line[-2:]:
                    self.author = u.clean(line[2:-2])
                if line[:2] == "~~" == line[-2:]:
                    if u.clean(line[2:-2]) == "off":
                        self.active = False

    def __getitem__(self, room_id):
        return self.build_room(room_id)

    def find_room(self, room_id):
        return self._find_id(room_id, '#')

    def find_item(self, item_id, path=None):
        if path is None:
            path = self.path
        return self._find_id(item_id, '%', path=path)

    def _find_id(self, obj_id, key, path=None):
        if path is None:
            path = self.path
        text = ''
        success = False
        with open(path, 'r') as f:
            for line in f:
                line = u.clean(line)
                if success and len(line) > 0:
                    if not line[0] in ['#', '%']:
                        text += line + '\n'
                    else:
                        break
                if len(line) > 0 and line[0] == key and line.split()[1] == obj_id:
                    text += line + '\n'
                    success = True
            if not(success) and key == '#':
                return False
        return text

    def build_room(self, room_id):
        text = self.find_room(room_id)
        if room_id == "__GAMEOVER__":
            raise e.AVEGameOver
        if room_id == "__WINNER__":
            raise e.AVEWinner
        elif text is False:
            return self.fail_room()
        else:
            c_txt = []
            c_options = []
            for line in text.split('\n')[1:]:
                line = u.clean(line)
                if "=>" in line:
                    lsp = line.split("=>")
                    next_option = {'id':"",'option':"",'needs':[],'unneeds':[],'adds':[],'rems':[]}
                    next_option['option'] = u.clean(lsp[0])
                    lsp = u.clean(lsp[1]).split()
                    next_option['id'] = u.clean(lsp[0])
                    for i in range(1,len(lsp),2):
                        for a,b in attrs.items():
                            if lsp[i] == a:
                                next_option[b].append(lsp[i+1])
                    c_options.append(next_option)
                elif u.clean(line) != "":
                    next_line = {'text':"",'needs':[],'unneeds':[],'adds':[],'rems':[]}
                    text = line
                    for a in attrs:
                        text = text.split(" "+a)[0]
                    next_line['text'] = u.clean(text)
                    lsp = line.split()
                    for i in range(len(lsp)-1):
                        for a,b in attrs.items():
                            if lsp[i] == a:
                                next_line[b].append(lsp[i+1])
                    c_txt.append(next_line)
            return Room(room_id, c_txt, c_options, self.screen, self.character)

    def load(self):
        self.screen.clear()

    def begin(self):
        self.character.set_game(self)
        self.show_title()
        room = self['start']
        while True:
            self.screen.clear()
            self.screen.put_ave_logo()
            next = room.show()
            while next is None:
                next = room.show(show_inv=True)
            room = self[next]

    def fail_room(self):
        options = [{'id':"__GAMEOVER__",'option':"Continue",'needs':[],'unneeds':[],'adds':[],'rems':[]}]
        text = [{'text':"You fall off the edge of the game... (404 Error)",'needs':[],'unneeds':[],'adds':[],'rems':[]}]
        return Room("fail", text, options, self.screen, self.character)

    def show_title(self):
        self.screen.show_titles(self.title, self.description, self.author)
