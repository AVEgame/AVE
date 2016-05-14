#!/usr/bin/env python
from core.ave import AVE
from curses import wrapper
from core.errors import *
try:
    ave = AVE()
    ave.start()
except AVEQuit:
    ave.exit()
    print("Goodbye...")
finally:
    ave.exit()
