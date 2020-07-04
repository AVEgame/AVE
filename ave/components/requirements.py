"""Conditions that are required to show a line, option or item name."""

from .numbers import Constant


class Requirement:
    """A base requirement."""

    def has(self, character):
        """Check if the character satisifies this."""
        raise NotImplementedError()

    def get_all(self):
        """Get all items involved in this requirement."""
        raise NotImplementedError()


class RequiredItem(Requirement):
    """The character must have an item."""

    def __init__(self, item):
        """Make the requirement."""
        self.item = item

    def has(self, character):
        """Check if the character satisifies this."""
        return character.has(self.item)

    def get_all(self):
        """Get all items involved in this requirement."""
        return [self.item]


class RequiredNumber(Requirement):
    """A numerical variable must satisfy a condition."""

    def __init__(self, v1, sign=">", v2=Constant(0)):
        """Make the requirement."""
        self.v1 = v1
        self.sign = sign
        self.v2 = v2

    def has(self, character):
        """Check if the character satisifies this."""
        v1 = self.v1.get_value(character)
        v2 = self.v2.get_value(character)
        if self.sign == ">":
            return v1 > v2
        if self.sign == "<":
            return v1 < v2
        if self.sign == ">=":
            return v1 >= v2
        if self.sign == "<=":
            return v1 <= v2
        if self.sign == "=" or self.sign == "==":
            return v1 == v2

    def get_all(self):
        """Get all items involved in this requirement."""
        return self.v1.get_all_variables() + self.v1.get_all_variables()


class Or(Requirement):
    """One of a set of Requirements must be satisfied."""

    def __init__(self, *items):
        """Make the requirement."""
        self.items = items

    def has(self, character):
        """Check if the character satisifies this."""
        for i in self.items:
            if i.has(character):
                return True
        return False

    def get_all(self):
        """Get all items involved in this requirement."""
        out = []
        for i in self.items:
            out += i.get_all()
        return out


class And(Requirement):
    """A set of Requirements must all be satisfied."""

    def __init__(self, *items):
        """Make the requirement."""
        self.items = items

    def has(self, character):
        """Check if the character satisifies this."""
        for i in self.items:
            if not i.has(character):
                return False
        return True

    def get_all(self):
        """Get all items involved in this requirement."""
        out = []
        for i in self.items:
            out += i.get_all()
        return out


class Not(Requirement):
    """The negation of another Requirement."""

    def __init__(self, item):
        """Make the requirement."""
        self.item = item

    def has(self, character):
        """Check if the character satisifies this."""
        return not self.item.has(character)

    def get_all(self):
        """Get all items involved in this requirement."""
        return self.item.get_all()


class Satisfied(Requirement):
    """This requirement is always satisfied."""

    def has(self, character):
        """Check if the character satisifies this."""
        return True

    def get_all(self):
        """Get all items involved in this requirement."""
        return []
