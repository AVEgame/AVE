#!/usr/bin/env python
from __future__ import division
import sys
sys.path.insert(0,'..')
from core.ave import Game,Character
from core.screen import DummyScreen

ds = DummyScreen()
c = Character(ds)

game = Game(sys.argv[1],ds,c)
game.load()
not_inc = []
for id in game.rooms:
    for key in game[id].options:
        if key['id'] not in game.rooms and key['id'] != "__GAMEOVER__" and key['id'] not in not_inc:
            not_inc.append(key['id'])

if len(not_inc)>0:
    print "Rooms not defined:"
    for key in not_inc:
        print " ",key
else:
    print "Game contains no errors"
