import random


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


class Random(Number):
    def __init__(self, *args):
        if len(args) == 0:
            self.start = Constant(0)
            self.size = Constant(1)
        elif len(args) == 1:
            self.start = Constant(0)
            self.size = args[0]
        elif len(args) == 2:
            self.start = args[0]
            self.size = args[1]

    def get_value(self, character):
        return self.start.get_value(character) \
             + self.size.get_value(character) * random.random()
