class Requirement:
    def has(self, character):
        raise NotImplementedError()


class RequiredItem(Requirement):
    def __init__(self, item):
        self.item = item

    def has(self, character):
        return character.has(self.item)


class RequiredNumber(Requirement):
    def __init__(self, item, sign=">", value=0):
        self.item = item
        self.sign = sign
        self.value = value

    def has(self, character):
        n = character.numbers[self.item]
        v = self.value.get_value(character)
        if self.sign == ">":
            return n > v
        if self.sign == "<":
            return n < v
        if self.sign == ">=":
            return n >= v
        if self.sign == "<=":
            return n <= v
        if self.sign == "=" or self.sign == "==":
            return n == v


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
