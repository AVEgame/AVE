from random import randrange
from .exceptions import AVEGameOver, AVEWinner
from .escaping import more_unescape
from .items import Number


def finalise(txt, character):
    for i, n in character.numbers.items():
        txt = txt.replace("$" + i + "$", str(n))
    return more_unescape(txt)


class Character:
    def __init__(self, inventory=[], numbers={}, location=None):
        self.inventory = inventory
        self.numbers = numbers
        self.location = location

    def reset(self, items):
        self.inventory = []
        self.numbers = {}
        for i in items.values():
            if isinstance(i, Number):
                self.numbers[i.id] = i.default
        self.location = "start"

    def has(self, item):
        if item in self.numbers:
            return self.numbers[item] > 0
        else:
            return item in self.inventory

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
        elif item in self.inventory:
            self.inventory.remove(item)

    def is_number(self, item):
        return isinstance(item, Number)

    def get_inventory(self, items):
        inv = []
        for i, n in self.numbers.items():
            item = items[i]
            if not item.hidden:
                inv.append(finalise(item.get_name(self), self) + ": " + str(n))
        for i in self.inventory:
            if i in items:
                item = items[i]
                if not item.hidden:
                    inv.append(finalise(item.get_name(self), self))
        return [i for i in inv if i is not None and i != ""]


class Game:
    def __init__(self, file=None, url=None,
                 title="untitled", number=None,
                 description="", author="anonymous",
                 active=True):
        self.file = file
        self.url = url
        self.number = number
        self.title = title
        self.description = description
        self.author = author
        self.active = active
        self.rooms = None

        self.options = []

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
        if id in self.rooms:
            return self.rooms[id]
        else:
            return self.fail_room()

    def pick_option(self, key, character):
        room = self[character.location]
        o = room.options[key]
        o.get_items(character)
        character.location = o.get_destination()

    def get_room_info(self, character):
        room = self[character.location]
        text = room.get_text(character)
        options = room.get_options(character)
        return text, {i: finalise(o.text, character)
                      for i, o in options.items()}

    def fail_room(self):
        options = [{'id': "__GAMEOVER__", 'option': "Continue",
                    'needs': [], 'unneeds': [], 'adds': [], 'rems': []}]
        text = [{'text': "You fall off the edge of the game... (404 Error)",
                 'needs': [], 'unneeds': [], 'adds': [], 'rems': []}]
        return Room("fail", text, options)


class Room:
    def __init__(self, id=None, text="", options=[]):
        self.id = id
        self.text = text
        self.options = options

    def __str__(self):
        return "Room with id " + self.id

    def get_text(self, character):
        lines = []
        for line in self.text:
            if line.has_requirements(character):
                line.get_items(character)
                lines.append(line.text)
        return finalise(" ".join(lines), character)

    def get_options(self, character):
        return {i: o for i, o in enumerate(self.options)
                if o.has_requirements(character)}


class ThingWithRequirements:
    def __init__(self, items=[], needs=[]):
        self.items = items
        self.needs = needs

    def has_requirements(self, character):
        return self.needs.has(character)

    def get_items(self, character):
        for item in self.items:
            item.give(character)


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

    def get_all_destinations(self):
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
