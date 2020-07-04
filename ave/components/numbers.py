"""Number classes."""

import random


class Number:
    """Base number class."""

    def get_value(self, character):
        """Get the value of the Number."""
        raise NotImplementedError()

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        raise NotImplementedError()


class Constant(Number):
    """A constant."""

    def __init__(self, value):
        """Make the number."""
        self.value = value

    def get_value(self, character):
        """Get the value of the Number."""
        return self.value

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        return []


class Sum(Number):
    """The sum of multiple Numbers."""

    def __init__(self, *items):
        """Make the number."""
        self.items = items

    def get_value(self, character):
        """Get the value of the Number."""
        return sum(i.get_value(character) for i in self.items)

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        out = []
        for i in self.items:
            out += i.get_all_variables()
        return out


class Product(Number):
    """The product of multiple Numbers."""

    def __init__(self, *items):
        """Make the number."""
        self.items = items

    def get_value(self, character):
        """Get the value of the Number."""
        out = 1
        for i in self.items:
            out *= i.get_value(character)
        return out

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        out = []
        for i in self.items:
            out += i.get_all_variables()
        return out


class Division(Number):
    """The result of a division."""

    def __init__(self, value, *items):
        """Make the number."""
        self.value = value
        self.items = items

    def get_value(self, character):
        """Get the value of the Number."""
        out = self.value.get_value(character)
        for i in self.items:
            out /= i.get_value(character)
        return out

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        out = []
        for i in self.items:
            out += i.get_all_variables()
        return out


class Negative(Number):
    """The negative of another Number."""

    def __init__(self, item):
        """Make the number."""
        self.item = item

    def get_value(self, character):
        """Get the value of the Number."""
        return -self.item.get_value(character)

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        return self.item.get_all_variables()


class Variable(Number):
    """The value of a variable."""

    def __init__(self, item):
        """Make the number."""
        self.item = item

    def get_value(self, character):
        """Get the value of the Number."""
        return character.numbers[self.item]

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        return [self.item]


class Random(Number):
    """A random number."""

    def __init__(self, *args):
        """Make the number."""
        if len(args) == 0:
            self.start = Constant(0)
            self.end = Constant(1)
        elif len(args) == 1:
            self.start = Constant(0)
            self.end = args[0]
        elif len(args) == 2:
            self.start = args[0]
            self.end = args[1]

    def get_value(self, character):
        """Get the value of the Number."""
        start = self.start.get_value(character)
        end = self.end.get_value(character)
        size = end - start
        return start + random.random() * size

    def get_all_variables(self):
        """Get a list of all variables used in this expression."""
        return self.start.get_all_variables() + self.end.get_all_variables()
