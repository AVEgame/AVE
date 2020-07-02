from . import numbers as no


class ItemGiver:
    def give(self, character):
        raise NotImplementedError()


class Add(ItemGiver):
    def __init__(self, item, value=no.Constant(1)):
        self.item = item
        self.value = value

    def give(self, character):
        character.add(self.item, self.value.get_value(character))


class Remove(ItemGiver):
    def __init__(self, item, value=no.Constant(1)):
        self.item = item
        self.value = value

    def give(self, character):
        character.remove(self.item, self.value.get_value(character))


class Set(ItemGiver):
    def __init__(self, item, value):
        self.item = item
        self.value = value

    def give(self, character):
        character.set(self.item, self.value.get_value(character))
