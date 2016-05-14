#!/usr/bin/env python
from __future__ import division
from core.ave import AVE
from curses import wrapper
from core.errors import *

#while True:
#    try:
#        ave = AVE()
#        ave.start()
#    except AVEQuit:
#        ave.exit()
#        print("Goodbye...")
#        break
#    except:
#        ave.exit()
#        break
try:
        ave = AVE()
        ave.start()
except AVEQuit:
        ave.exit()
        print("Goodbye...")
finally:
        ave.exit()
