from .numbers import Constant


class Requirement:
    def has(self, character):
        raise NotImplementedError()


class RequiredItem(Requirement):
    def __init__(self, item):
        self.item = item

    def has(self, character):
        return character.has(self.item)


class RequiredNumber(Requirement):
    def __init__(self, v1, sign=">", v2=Constant(0)):
        self.v1 = v1
        self.sign = sign
        self.v2 = v2

    def has(self, character):
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


class Or(Requirement):
    def __init__(self, *items):
        self.items = items

    def has(self, character):
        for i in self.items:
            if i.has(character):
                return True
        return False


class And(Requirement):
    def __init__(self, *items):
        self.items = items

    def has(self, character):
        for i in self.items:
            if not i.has(character):
                return False
        return True


class Not(Requirement):
    def __init__(self, item):
        self.item = item

    def has(self, character):
        return not self.item.has(character)


class Satisfied(Requirement):
    def has(self, character):
        return True
