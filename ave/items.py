"""Items that can be held in the character's inventory."""

from .numbers import Constant


class BaseItem:
    """A base item class."""

    def get_name(self, character):
        """Get the name of the item.

        Parameters
        ----------
        character : ave.game.Character
            The character

        Returns
        -------
        string
            The name of the item.
        """
        if self.hidden:
            return None
        out = []
        for name in self.names:
            if name.has_requirements(character):
                out.append(name.text)
        if len(out) == 0:
            return None
        return " ".join(out)


class Number(BaseItem):
    """A numerical variable."""

    def __init__(self, id=id, names=[], hidden=True, default=Constant(0)):
        """Make the variable.

        Parameters
        ----------
        id : string
            The name of the variable
        names : list
            The names of the item (with requirements for possible alternative names)
        hidden : bool
            Should this item be hidden from the inventory list
        default : ave.numbers.Number
            The default value of the variable
        """
        self.id = id
        self.hidden = hidden
        self.names = names
        self.default = default


class Item(BaseItem):
    """An object."""

    def __init__(self, id=None, names=[], hidden=True):
        """Make the item.

        Parameters
        ----------
        id : string
            The name of the variable
        names : list
            The names of the item (with requirements for possible alternative names)
        hidden : bool
            Should this item be hidden from the inventory list
        """
        self.id = id
        self.hidden = hidden
        self.names = names
