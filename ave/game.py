import re
from .exceptions import AVEGameOver, AVEWinner

attrs = {"+": "adds", "?": "needs", "?!": "unneeds", "~": "rems"}


class Item:
    def __init__(self, name, character):
        self.name = name
        self.character = character

    def get_name(self):
        if self.name in self.character.items:
            name = []
            for line in self.character.items[self.name][0]:
                if self.character.has(line['needs']) \
                        and self.character.unhas(line['unneeds']):
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
                self.numbers[i] = [self.items[i][3], Item(i, self)]

    def reset(self):
        self.inventory = []
        self.name = ""
        self.reset_numbers()

    def _add_item(self, item):
        if "=" in item and self.is_number(item.split("=", 1)[0]):
            self.numbers[item.split("=", 1)[0]][0] = self._parse_number(
                item.split("=", 1)[1])
        elif "+" in item and self.is_number(item.split("+", 1)[0]):
            self.numbers[item.split("+", 1)[0]][0] += self._parse_number(
                item.split("+", 1)[1])
        elif "-" in item and self.is_number(item.split("-", 1)[0]):
            self.numbers[item.split("-", 1)[0]][0] -= self._parse_number(
                item.split("-", 1)[1])
        elif self.is_number(item):
            self.numbers[item][0] += 1
        else:
            self.inventory.append(Item(item, self))

    def _remove_item(self, item):
        if self.is_number(item):
            self.numbers[item][0] -= 1
        elif item in self.inventory_ids():
            for a, b in enumerate(self.inventory):
                if b.name == item:
                    self.inventory = self.inventory[:a] \
                        + self.inventory[a + 1:]
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
                    if b[0] == "!" and not self._has(b[1:]):
                        break
                else:
                    return False
            return True
        return self._has(item)

    def _split_up(self, item):
        for s, f in [
            ("==", lambda a, b: a == b),
            (">=", lambda a, b: a >= b),
            ("<=", lambda a, b: a <= b),
            ("<", lambda a, b: a < b),
            (">", lambda a, b: a > b),
            ("=", lambda a, b: a == b)
        ]:
            if s in item:
                return item.split(s, 1)[0], f, item.split(s, 1)[1]
        return item, None, None

    def _parse_number(self, num):
        try:
            return int(num)
        except ValueError:
            try:
                return float(num)
            except ValueError:
                if "__R__" in num:
                    import random
                    if num == "__R__":
                        return random.random()
                    if re.match(r"__R__[0-9]", num):
                        return random.random() * int(num.split("__R__", 1)[1])
                else:
                    return self.numbers[num][0]

    def _has(self, item):
        item_, f, against = self._split_up(item)
        if "__R__" in item_ or self.is_number(item_):
            if f is None:
                return self._parse_number(item_) > 0
            else:
                return f(self._parse_number(item_),
                         self._parse_number(against))
        else:
            if item == "__PYTHON__":
                return True
            return item in self.inventory_ids()

    def unhas(self, item):
        if type(item) == list:
            for a in item:
                for b in a:
                    if not self._has(b):
                        break
                    if b[0] == "!" and self._has(b):
                        break
                else:
                    return False
            return True
        return not self._has(item)

    def is_number(self, item):
        if item in self.items:
            return self.items[item][2]
        for s in ["<", ">", "="]:
            if item.split(s, 1)[0] in self.items:
                return self.items[item.split(s, 1)[0]][2]
        return False

    def show_inventory(self):
        inv = []
        for n, item in self.numbers.values():
            if not item.is_hidden():
                inv.append(item.get_name() + ": " + str(n))
        for i in self.inventory:
            if not i.is_hidden():
                inv.append(i.get_name())
        self.screen.show_inventory(inv)

    def inventory_ids(self):
        return [item.name for item in self.inventory]


class Game:
    def __init__(self, file, title="untitled", number=None,
                 description="", author="anonymous",
                 active=True, character=None, screen=None):
        self.number = number
        self.file = file
        self.title = title
        self.description = description
        self.author = author
        self.active = active
        self.rooms = None
        self.character = character
        self.screen = screen

    def load(self):
        if self.rooms is None:
            from .file_handler import load_rooms_and_items_from_file
            self.rooms, self.character.items = load_rooms_and_items_from_file(
                self.file)

    def __getitem__(self, id):
        return self.load_room(id)

    def load_room(self, id):
        if id == "__GAMEOVER__":
            raise AVEGameOver
        if id == "__WINNER__":
            raise AVEWinner
        if "__R__" in id:
            id = self._parse_random(id)
        if id in self.rooms:
            return self.rooms[id]
        else:
            return self.fail_room()

    def _parse_random(self, id):
        import random
        rooms = id.split("(", 1)[1].split(")", 1)[0].split(",")
        if "[" in id:
            ls = []
            nums = [int(i) for i
                    in id.split("[", 1)[1].split("]", 1)[0].split(",")]
            for r, n in zip(rooms, nums):
                ls += [r] * n
            return random.choice(ls)
        else:
            return random.choice(rooms)

    def begin(self):
        self.show_title()
        room = self['start']
        while True:
            self.screen.clear()
            self.screen.put_ave_logo()
            next = room.show(self.character, self.screen)
            room = self[next]

    def fail_room(self):
        options = [{'id': "__GAMEOVER__", 'option': "Continue",
                    'needs': [], 'unneeds': [], 'adds': [], 'rems': []}]
        text = [{'text': "You fall off the edge of the game... (404 Error)",
                 'needs': [], 'unneeds': [], 'adds': [], 'rems': []}]
        return Room("fail", text, options)

    def show_title(self):
        self.screen.show_titles(self.title, self.description, self.author)


class Room:
    def __init__(self, id, text, options):
        self.id = id
        self.text = text
        self.options = options

    def __str__(self):
        return "Room with id " + self.id

    def show(self, character, screen):
        from .screen import WIDTH
        included_lines = []
        for line in self.text:
            if character.has(line['needs']) \
                    and character.unhas(line['unneeds']):
                character.add_items(line['adds'])
                character.remove_items(line['rems'])
                included_lines.append(line['text'])
        y = 0
        x = 0
        stuff = []
        text = " ".join(included_lines)
        com = False
        text = re.sub(r"([^ ])<\|", r"\1 <|", text)
        text = re.sub(r"\|>([^ ])", r"|> \1", text)
        for word in text.split():
            if word[:2] == "<|":
                com = True
                word = word[2:].strip()
            if word[-2:] == "|>":
                com = False
                word = word[:-2].strip()
            if not com and "$" in word:
                for item, value in character.numbers.items():
                    word = str(value[0]).join(word.split("$" + item + "$"))
            if not com and word == "<newline>":
                y += 1
                x = 0
            elif word != "":
                if x + len(word) > WIDTH - 22:
                    y += 1
                    x = 0
                for i, c in enumerate(word):
                    stuff.append((y, x, c))
                    x += 1
                stuff.append((y, x, " "))
                x += 1
        screen.type(stuff)

        opts = []
        adds = []
        rems = []
        ids = []
        for option in self.options:
            if character.has(option['needs']) \
                    and character.unhas(option['unneeds']):
                opts.append(option['option'])
                adds.append(option['adds'])
                rems.append(option['rems'])
                ids.append(option['id'])
        character.show_inventory()
        num = screen.menu(opts, add=adds, rem=rems, y=min(8, len(opts)),
                          character=character)
        return ids[num]
