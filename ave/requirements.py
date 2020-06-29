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
        if self.sign == ">":
            return n > self.value
        if self.sign == "<":
            return n < self.value
        if self.sign == ">=":
            return n >= self.value
        if self.sign == "<=":
            return n <= self.value
        if self.sign == "=" or self.sign == "==":
            return n == self.value


class ReqOr(Requirement):
    def __init__(self, *items):
        self.items = items

    def has(self, character):
        for i in self.items:
            if character.has(i):
                return True
        return False


class ReqAnd(Requirement):
    def __init__(self, *items):
        self.items = items

    def has(self, character):
        for i in self.items:
            if not character.has(i):
                return False
        return True


class ReqNot(Requirement):
    def __init__(self, item):
        self.item = item

    def has(self, character):
        return not character.has(self.item)
