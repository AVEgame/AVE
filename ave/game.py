import re
from .exceptions import AVEGameOver, AVEWinner


class BaseItem:
    pass


class Number(BaseItem):
    def __init__(self, id=id, names=[], hidden=True, default=0):
        self.id = id
        self.hidden = hidden
        self.names = names
        self.default = default


class Item(BaseItem):
    def __init__(self, id=None, names=[], hidden=True):
        self.id = id
        self.hidden = hidden
        self.names = names


class Character:
    def __init__(self):
        self.items = []
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
            self.inventory.append(item)

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

    def get_inventory(self):
        inv = []
        for n, item in self.numbers.values():
            if not item.hidden:
                inv.append(item.get_name() + ": " + str(n))
        for i in self.inventory:
            if not i.hidden:
                inv.append(i.get_name())
        return inv

    def inventory_ids(self):
        return [item.id for item in self.inventory]


class Game:
    def __init__(self, file=None, url=None,
                 title="untitled", number=None,
                 description="", author="anonymous",
                 active=True, character=None, screen=None):
        self.file = file
        self.url = url
        self.number = number
        self.title = title
        self.description = description
        self.author = author
        self.active = active
        self.rooms = None
        self.character = character
        self.screen = screen

    def load(self):
        if self.file is not None:
            from .game_loader import load_full_game_from_file as lfg
            arg = self.file
        elif self.url is not None:
            from .game_loader import load_full_game_from_url as lfg
            arg = self.url
        else:
            raise ValueError("One of url and file must be set to load a game.")
        self.rooms, self.items = lfg(arg)

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
    def __init__(self, id=None, text="", options=[]):
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
        screen.show_inventory(character.get_inventory())
        num = screen.menu(opts, add=adds, rem=rems, y=min(8, len(opts)),
                          character=character)
        return ids[num]


class ThingWithRequirements:
    def __init__(self, adds=[], needs=[], unneeds=[], rems=[]):
        self.adds = adds
        self.needs = needs
        self.unneeds = unneeds
        self.rems = rems

    def has_requirements(self, character):
        for item in self.needs:
            if not character.has(item):
                return False
        if item in self.unneeds:
            if character.has(item):
                return False
        return True

    def get_items(self, character):
        for item in self.adds:
            character.add(item)
        for item in self.rems:
            character.remove(item)


class TextWithRequirements(ThingWithRequirements):
    def __init__(self, text, **kwargs):
        self.text = text
        super().__init__(**kwargs)


class OptionWithRequirements(ThingWithRequirements):
    def __init__(self, text, destination, random=None, **kwargs):
        self.text = text
        self.destination = destination
        if random is None:
            self.random = False
        else:
            self.random = True
            self.probabilities = random
        super().__init__(**kwargs)

    def get_destinations(self):
        if self.random:
            return self.destination
        else:
            return [self.destination]


class NameWithRequirements(ThingWithRequirements):
    def __init__(self, text, **kwargs):
        self.text = text
        super().__init__(**kwargs)
