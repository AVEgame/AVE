class BaseItem:
    def get_name(self, character):
        if self.hidden:
            return None
        out = []
        for name in self.names:
            if name.has_requirements(character):
                out.append(name.text)
        if len(out) == 0:
            return None
        return " ".join(out)


class Number(BaseItem):
    def __init__(self, id=id, names=[], hidden=True, default=0):
        self.id = id
        self.hidden = hidden
        self.names = names
        self.default = default


class Item(BaseItem):
    def __init__(self, id=None, names=[], hidden=True):
        self.id = id
        self.hidden = hidden
        self.names = names
