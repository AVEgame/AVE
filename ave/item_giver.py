class ItemGiver:
    def give(self, character):
        raise NotImplementedError()


class Add(ItemGiver):
    def __init__(self, item, value=1):
        self.item = item
        self.value = value

    def give(self, character):
        character.add(self.item, self.value)


class Remove(ItemGiver):
    def __init__(self, item, value=1):
        self.item = item
        self.value = value

    def give(self, character):
        character.remove(self.item, self.value)


class Set(ItemGiver):
    def __init__(self, item, value):
        self.item = item
        self.value = value

    def give(self, character):
        character.set(self.item, self.value.get_value(character))
