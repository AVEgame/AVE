"""Classes that make up the parsed game data."""

from random import randrange
from .requirements import Satisfied


class ThingWithRequirements:
    """A thing that needs requirements to be satisfied to be shown."""

    def __init__(self, items=[], needs=Satisfied()):
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
