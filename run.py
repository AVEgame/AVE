#!/usr/bin/env python
from ave import Games

g = Games("games")

print g.titles_and_descriptions()

g.game(0).load()
print g.game(0).rooms
