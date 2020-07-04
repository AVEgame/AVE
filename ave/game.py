"""Classes for running games."""

from . import config
from .components import TextWithRequirements, OptionWithRequirements
from .components.items import NumberItem
from .exceptions import AVEGameOver, AVEWinner, AVEVersionError
from .parsing.string_functions import more_unescape


def finalise(txt, character):
    """Insert variables into text, then unescape final characters."""
    for i, n in character.numbers.items():
        txt = txt.replace("$" + i + "$", str(n))
    return more_unescape(txt)


class Character:
    """The character playing the game."""

    def __init__(self, inventory=None, numbers=None, location=None):
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
        if inventory is None:
            inventory = []
        if numbers is None:
            numbers = {}
        self.inventory = inventory
        self.numbers = numbers
        self.location = location

    def reset(self, items={}):
        """Reset the character."""
        self.inventory = []
        self.numbers = {}
        for i in items.values():
            if self.is_number(i):
                self.numbers[i.id] = i.default.get_value(self)
        self.location = "start"

    def has(self, item):
        """Check if the character has an item."""
        if item in self.numbers:
            return self.numbers[item] > 0
        else:
            return item in self.inventory

    def add(self, item, value=1):
        """Add an item or add to a number.

        Parameters
        ----------
        item : string
            The item or variable
        value : ave.numbers.NumberItem
            The value to add
        """
        if item in self.numbers:
            self.numbers[item] += value
        elif item not in self.inventory:
            self.inventory.append(item)

    def set(self, item, value):
        """Set a number equal to a value.

        Parameters
        ----------
        item : string
            The variable
        value : ave.numbers.NumberItem
            The value to set it to
        """
        self.numbers[item] = value

    def remove(self, item, value=1):
        """Remove an item or take from a number.

        Parameters
        ----------
        item : string
            The item or variable
        value : ave.numbers.NumberItem
            The value to take
        """
        if item in self.numbers:
            self.numbers[item] -= value
        elif item in self.inventory:
            self.inventory.remove(item)

    def is_number(self, item):
        """Check if item is a NumberItem."""
        return isinstance(item, NumberItem)

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
                name = item.get_name(self)
                if name is not None:
                    inv.append(finalise(name, self) + ": " + str(n))
        for i in self.inventory:
            if i in items:
                item = items[i]
                if not item.hidden:
                    name = item.get_name(self)
                    if name is not None:
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
        self.filename = filename
        self.url = url
        self.number = number
        self.title = title
        self.description = description
        self.author = author
        self.active = active
        self.version = version
        self.ave_version = tuple(ave_version)
        self.rooms = None

        self.options = []

    def load(self):
        """Load the full game from the file or url."""
        if config.version_tuple < self.ave_version:
            raise AVEVersionError()
        if self.file is not None:
            from .parsing.game_loader import load_full_game_from_file
            self.rooms, self.items = load_full_game_from_file(self.file)
        elif self.url is not None:
            from .parsing.game_loader import load_full_game_from_url
            self.rooms, self.items = load_full_game_from_url(self.url)
        else:
            raise ValueError("One of url and file must be set to load a game.")

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
        return Room(
            "fail",
            [TextWithRequirements("You fall off the edge of the game... "
                                  "(404 Error)")],
            [OptionWithRequirements("Continue", "__GAMEOVER__")])


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
