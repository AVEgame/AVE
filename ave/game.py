from random import randrange
from .exceptions import AVEGameOver, AVEWinner
from .escaping import more_unescape


def finalise(txt, character):
    # TODO: put this in options and var names
    for i, n in character.numbers.items():
        txt = txt.replace("$" + i + "$", str(n))
    return more_unescape(txt)


class BaseItem:
    def get_name(self, character):
        if self.hidden:
            return None
        out = []
        for name in self.names:
            if name.has_requirements(character):
                out.append(name.text)
        if len(out) == 0:
            return None
        return finalise(" ".join(out), character)


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
        self.inventory = []
        self.numbers = {}

    def reset(self, items):
        self.inventory = []
        self.numbers = {}
        for i in items.values():
            if self.is_number(i):
                self.numbers[i.id] = i.default

    def add(self, item, value=1):
        if item in self.numbers:
            self.numbers[item] += value
        elif item not in self.inventory:
            self.inventory.append(item)

    def set(self, item, value):
        self.numbers[item] = value

    def remove(self, item, value=1):
        if item in self.numbers:
            self.numbers[item] -= value
        else:
            self.inventory.append(item)

    def has(self, item):
        if item in self.numbers:
            return self.numbers[item] > 0
        else:
            return item in self.inventory

    def has_one(self, items):
        for item in items:
            if self.has(item):
                return True
        return False

    def is_number(self, item):
        return isinstance(item, Number)

    def get_inventory(self, items):
        inv = []
        for i, n in self.numbers.values():
            item = items[i]
            if not item.hidden:
                inv.append(item.get_name(self) + ": " + str(n))
        for i in self.inventory:
            if i in items:
                item = items[i]
                if not item.hidden:
                    inv.append(item.get_name(self))
        return [i for i in inv if i is not None and i != ""]

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
        self.enter_room("start")

    def enter_room(self, id):
        room = self[id]

        self.screen.clear()
        self.screen.put_ave_logo()
        self.screen.show_inventory(self.character.get_inventory(self.items))
        self.screen.type_room_text(room.get_text(self.character))

        opts = room.get_options(self.character)
        next = opts[self.screen.menu(
            [finalise(o.text, self.character) for o in opts],
            y=min(8, len(opts)))]

        next.get_items(self.character)
        self.enter_room(next.get_destination())

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

    def get_text(self, character):
        # TODO: $variable$
        lines = []
        for line in self.text:
            if line.has_requirements(character):
                line.get_items(character)
                lines.append(line.text)
        return finalise(" ".join(lines), character)

    def get_options(self, character):
        return [o for o in self.options if o.has_requirements(character)]


class ThingWithRequirements:
    def __init__(self, adds=[], needs=[], unneeds=[], rems=[]):
        self.adds = adds
        self.needs = needs
        self.unneeds = unneeds
        self.rems = rems

    def has_requirements(self, character):
        for item in self.needs:
            if not character.has_one(item):
                return False
        for item in self.unneeds:
            if character.has_one(item):
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

    def get_destination(self):
        if self.random:
            n = randrange(sum(self.probabilities))
            total = 0
            for d, i in zip(self.destination, self.probabilities):
                total += i
                if total > n:
                    return d
        else:
            return self.destination


class NameWithRequirements(ThingWithRequirements):
    def __init__(self, text, **kwargs):
        self.text = text
        super().__init__(**kwargs)
