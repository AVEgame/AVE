class Number:
    def get_value(self, character):
        raise NotImplementedError()


class Constant(Number):
    def __init__(self, value):
        self.value = value

    def get_value(self, character):
        return self.value


class Sum(Number):
    def __init__(self, *items):
        self.items = items

    def get_value(self, character):
        return sum(i.get_value(character) for i in self.items)


class Negative(Number):
    def __init__(self, item):
        self.item = item

    def get_value(self, character):
        return -self.item.get_value(character)


class Variable(Number):
    def __init__(self, item):
        self.item = item

    def get_value(self, character):
        return character.numbers[item]
