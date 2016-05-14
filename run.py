#!/usr/bin/env python
from ave import AVE
from time import sleep
from curses import wrapper
from errors import AVEQuit
try:
    ave = AVE()
    ave.start()
except AVEQuit:
    pass
finally:
    ave.exit()
