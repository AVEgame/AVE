"""Give and take items to/from a character."""

from . import numbers as no


class ItemGiver:
    """The ItemGiver class."""

    def give(self, character):
        """Give or take items."""
        raise NotImplementedError()


class Add(ItemGiver):
    """Add an item."""

    def __init__(self, item, value=no.Constant(1)):
        """Make an ItemGiver to add an item.

        Parameters
        ----------
        item : string
            An item or variable
        value : ave.numbers.Number
            The value to add to a variable
        """
        self.item = item
        self.value = value

    def give(self, character):
        """Give or take items."""
        character.add(self.item, self.value.get_value(character))


class Remove(ItemGiver):
    """Remove an item."""

    def __init__(self, item, value=no.Constant(1)):
        """Make an ItemGiver to take an item.

        Parameters
        ----------
        item : string
            An item or variable
        value : ave.numbers.Number
            The value to take from a variable
        """
        self.item = item
        self.value = value

    def give(self, character):
        """Give or take items."""
        character.remove(self.item, self.value.get_value(character))


class Set(ItemGiver):
    """Set a variable to a value."""

    def __init__(self, item, value):
        """Make an ItemGiver to set a variable to a value.

        Parameters
        ----------
        item : string
            The variable
        value : ave.numbers.Number
            The value to set it to
        """
        self.item = item
        self.value = value

    def give(self, character):
        """Give or take items."""
        character.set(self.item, self.value.get_value(character))
