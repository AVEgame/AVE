"""Classes for running games."""

from . import config
from .components import TextWithRequirements, OptionWithRequirements
from .components.items import NumberItem
from .exceptions import AVEGameOver, AVEWinner, AVEVersionError
from .parsing.string_functions import finalise


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
            if isinstance(i, NumberItem):
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
        self.currency = "£"

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
        if not isinstance(item, str):
            raise ValueError("item must be a string")
        return item in self.numbers

    def get_inventory(self, items, currency):
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
                    display_name = finalise(name, self.numbers, currency)
                    if item.id != "money" or currency is None:
                        display_name += ": "
                    inv.append(display_name + str(n))
        for i in self.inventory:
            if i in items:
                item = items[i]
                if not item.hidden:
                    name = item.get_name(self)
                    if name is not None:
                        inv.append(finalise(item.get_name(self), self.numbers,
                                            currency))
        return [i for i in inv if i is not None and i != ""]


class Game:
    """The Game classes that stores all the data to run the game."""

    def __init__(self, file=None, url=None,
                 filename=None, title="untitled", number=None,
                 description="", author="anonymous",
                 version=1, ave_version=(0, 0),
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
        self.id = None
        if file is not None:
            self.id = file
        if url is not None:
            self.id = url
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
        self.currency = None
        self.rooms = None
        self.items = None
        self.frames = None

        self.options = []

    def room_type(self, id):
        if id in self.rooms:
            return "room"
        if id in self.frames:
            return "cutscene"
        return None

    def load(self):
        """Load the full game from the file or url."""
        if config.version_tuple < self.ave_version:
            raise AVEVersionError()
        if self.file is not None:
            from .parsing.game_loader import load_full_game_from_file
            self.rooms, self.items, self.frames = load_full_game_from_file(self.file)
        elif self.url is not None:
            from .parsing.game_loader import load_full_game_from_url
            self.rooms, self.items, self.frames = load_full_game_from_url(self.url)
        else:
            raise ValueError("One of url and file must be set to load a game.")

        if "money" in self.items:
            c = self.items["money"].names[0].text
            if c in ["$", "£"]:
                self.currency = c

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

    def get_room_info(self, character, currency):
        """Get the information about the character's current room.

        Parameters
        ----------
        character : ave.game.Character
            The character
        currency : str
            The currency symbol of the money variable

        Returns
        -------
        str
            The room text
        dict
            The available destination options that the character could take
        """
        room = self[character.location]
        rtype = room.room_type
        if rtype == "room":
            rinfo = room.get_text(character, currency)
        elif rtype == "cutscene":
            rinfo = room.get_frames(self.frames)

        options = room.get_options(character)
        return rtype, rinfo, {i: finalise(o.text, character.numbers, currency)
                              for i, o in options.items()}

    def fail_room(self):
        """Return a 404 error room."""
        return Room(
            "fail",
            [TextWithRequirements("You fall off the edge of the game... "
                                  "(404 Error)")],
            [OptionWithRequirements("Continue", "__GAMEOVER__")])


class BaseRoom:
    """A base class for game rooms."""

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


class Room(BaseRoom):
    """A room in a game."""

    def __init__(self, id=None, text="", options=[]):
        """Make the room."""
        self.room_type = "room"
        self.id = id
        self.text = text
        self.options = options

    def __str__(self):
        """Return a string."""
        return "Room with id " + self.id

    def get_text(self, character, currency):
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
        return finalise(" ".join([i for i in lines if i != ""]),
                        character.numbers, currency)


class CutsceneRoom(BaseRoom):
    """A cutscene."""

    def __init__(self, id=None, frames=[], options=[]):
        """Make the cutscene."""
        self.room_type = "cutscene"
        self.id = id
        self.frames = frames
        self.options = options

    def __str__(self):
        """Return a string."""
        return "Cutscene with id " + self.id

    def get_frames(self, frames):
        """Get the cutscene frames.

        Parameters
        ----------
        frames : list
            The animation frames

        Returns
        -------
        str
            The room text
        """
        return [frames[f] for f in self.frames]
