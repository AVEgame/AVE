#!/usr/bin/env python
from __future__ import division
import sys
sys.path.insert(0,'..')
from core.ave import Game,Character
from core.screen import DummyScreen

ds = DummyScreen()
c = Character(ds)

def avefile():
    with open(sys.argv[1]) as f:
                return f.readlines()

game = Game(avefile,ds,c)
game.load()
not_inc = []
ach = ["start"]
for id in game.rooms:
    for key in game[id].options:
        if key['id'] not in ach:
            ach.append(key['id'])
        if key['id'] not in game.rooms and key['id'] != "__GAMEOVER__" and key['id'] != "__WINNER__" and key['id'] not in not_inc:
            not_inc.append(key['id'])

not_ach = [i for i in game.rooms if i not in ach]

if len(not_inc)>0 or len(not_ach)>0:
    if len(not_inc)>0:
        print "Rooms not defined:"
        for key in not_inc:
            print " ",key
    if len(not_ach)>0:
        print "Rooms not accessible:"
        for key in not_ach:
            print " ",key
else:
    print "Game contains no errors"
