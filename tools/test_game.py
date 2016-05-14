#!/usr/bin/env python
from __future__ import division
import sys
sys.path.insert(0,'..')
from core.ave import Game

game = Game(sys.argv[1],"",None)
game.load()
not_inc = []
for id in game.rooms:
    for key in game[id].options['id']:
        if key not in game.rooms and key != "__GAMEOVER__":
            not_inc.append(key)

if len(not_inc)>0:
    print "Rooms not defined:"
    for key in not_inc:
        print " ",key
else:
    print "Game contains no errors"
