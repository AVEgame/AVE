"""Classes for running games."""

from random import randrange
from .exceptions import AVEGameOver, AVEWinner, AVEVersionError
from .escaping import more_unescape
from .items import Number
from .numbers import Constant
from . import config


def finalise(txt, character):
    """Insert variables into text, then unescape final characters."""
    for i, n in character.numbers.items():
        txt = txt.replace("$" + i + "$", str(n))
    return more_unescape(txt)


class Character:
    """The character playing the game."""

    def __init__(self, inventory=[], numbers={}, location=None):
        """Create the character.

        Parameters
        ----------
        inventory : list
            A list of items the character has
        numbers : dict
            The value of all numerical variables
        location : string
            The location of the character
        """
        self.inventory = inventory
        self.numbers = numbers
        self.location = location

    def reset(self, items):
        """Reset the character."""
        self.inventory = []
        self.numbers = {}
        for i in items.values():
            if isinstance(i, Number):
                self.numbers[i.id] = i.default.get_value(self)
        self.location = "start"

    def has(self, item):
        """Check if the character has an item."""
        if item in self.numbers:
            return self.numbers[item] > 0
        else:
            return item in self.inventory

    def add(self, item, value=Constant(1)):
        """Add an item or add to a number.

        Parameters
        ----------
        item : string
            The item or variable
        value : ave.numbers.Number
            The value to add
        """
        if item in self.numbers:
            self.numbers[item] += value.get_value(self)
        elif item not in self.inventory:
            self.inventory.append(item)

    def set(self, item, value):
        """Set a number equal to a value.

        Parameters
        ----------
        item : string
            The variable
        value : ave.numbers.Number
            The value to set it to
        """
        self.numbers[item] = value.get_value(self)

    def remove(self, item, value=1):
        """Remove an item or take from a number.

        Parameters
        ----------
        item : string
            The item or variable
        value : ave.numbers.Number
            The value to take
        """
        if item in self.numbers:
            self.numbers[item] -= value
        elif item in self.inventory:
            self.inventory.remove(item)

    def is_number(self, item):
        """Check if item is a Number."""
        return isinstance(item, Number)

    def get_inventory(self, items):
        """Get the names of the character's inventory.

        Returns
        -------
        list
            The (non-hidden) items the character has
        """
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
    """The Game classes that stores all the data to run the game."""

    def __init__(self, file=None, url=None,
                 filename=None, title="untitled", number=None,
                 description="", author="anonymous",
                 version=0, ave_version=(0, 0),
                 active=True):
        """Make the class.

        Parameters
        ----------
        file : string
            The full path and filename filename of the .ave file of this game
        url : string
            The url of the .ave file of this game
        filename : string
            The filename of the .ave file of this game
        title : string
            The title of the game
        number : int
            The position in the game list where this game should appear
        description : string
            A short description of the game
        author : string
            The author(s) of the game
        version : int
            The version of the game
        ave_version : tuple
            The minimum AVE version required to run this game
        active : bool
            If False, this game will only be shown in debug mode
        """
        self.file = file
        self.url = url
        self.number = number
        self.title = title
        self.description = description
        self.author = author
        self.active = active
        self.version = version
        self.ave_version = ave_version
        self.rooms = None

        self.options = []

    def load(self):
        """Load the full game from the file or url."""
        if config.version_tuple < self.ave_version:
            raise AVEVersionError()
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
        """Get a room with given id."""
        return self.load_room(id)

    def load_room(self, id):
        """Get a room with given id."""
        if id == "__GAMEOVER__":
            raise AVEGameOver
        if id == "__WINNER__":
            raise AVEWinner
        if id in self.rooms:
            return self.rooms[id]
        else:
            return self.fail_room()

    def pick_option(self, key, character):
        """Follow a destination option from the character's current room.

        Parameters
        ----------
        key : int
            The number of the option chosen
        character : ave.game.Character
            The character
        """
        room = self[character.location]
        o = room.options[key]
        o.get_items(character)
        character.location = o.get_destination()

    def get_room_info(self, character):
        """Get the information about the character's current room.

        Parameters
        ----------
        character : ave.game.Character
            The character

        Returns
        -------
        str
            The room text
        dict
            The available destination options that the character could take
        """
        room = self[character.location]
        text = room.get_text(character)
        options = room.get_options(character)
        return text, {i: finalise(o.text, character)
                      for i, o in options.items()}

    def fail_room(self):
        """Return a 404 error room."""
        options = [{'id': "__GAMEOVER__", 'option': "Continue",
                    'needs': [], 'unneeds': [], 'adds': [], 'rems': []}]
        text = [{'text': "You fall off the edge of the game... (404 Error)",
                 'needs': [], 'unneeds': [], 'adds': [], 'rems': []}]
        return Room("fail", text, options)


class Room:
    """A room in a game."""

    def __init__(self, id=None, text="", options=[]):
        """Make the room."""
        self.id = id
        self.text = text
        self.options = options

    def __str__(self):
        """Return a string."""
        return "Room with id " + self.id

    def get_text(self, character):
        """Get the text for the room.

        Parameters
        ----------
        character : ave.game.Character
            The character

        Returns
        -------
        str
            The room text
        """
        lines = []
        for line in self.text:
            if line.has_requirements(character):
                line.get_items(character)
                lines.append(line.text)
        return finalise(" ".join(lines), character)

    def get_options(self, character):
        """Get the character's current destination options.

        Parameters
        ----------
        character : ave.game.Character
            The character

        Returns
        -------
        dict
            The available destination options that the character could take
        """
        return {i: o for i, o in enumerate(self.options)
                if o.has_requirements(character)}


class ThingWithRequirements:
    """A thing that needs requirements to be satisfied to be shown."""

    def __init__(self, items=[], needs=[]):
        """Make the thing."""
        self.items = items
        self.needs = needs

    def has_requirements(self, character):
        """Check is requirements are satisfied."""
        return self.needs.has(character)

    def get_items(self, character):
        """Give the character the items for and/or take items away."""
        for item in self.items:
            item.give(character)


class TextWithRequirements(ThingWithRequirements):
    """A line of test that needs requirements to be satisfied to be shown."""

    def __init__(self, text, **kwargs):
        """Make the thing."""
        self.text = text
        super().__init__(**kwargs)


class OptionWithRequirements(ThingWithRequirements):
    """An option that needs requirements to be satisfied to be shown."""

    def __init__(self, text, destination, random=None, **kwargs):
        """Make the thing."""
        self.text = text
        self.destination = destination
        if random is None:
            self.random = False
        else:
            self.random = True
            self.probabilities = random
        super().__init__(**kwargs)

    def get_all_destinations(self):
        """Get a list of all destinations that this options could lead to.

        Randomness will lead to multiple destinations from a single option.
        """
        if self.random:
            return self.destination
        else:
            return [self.destination]

    def get_destination(self):
        """Get the destination when this option is chosen."""
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
    """The name of an item that needs requirements to be satisfied."""

    def __init__(self, text, **kwargs):
        """Make the thing."""
        self.text = text
        super().__init__(**kwargs)
