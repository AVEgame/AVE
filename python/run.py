#!/usr/bin/env python
from __future__ import division
from core.ave import AVE
from curses import wrapper
from core.errors import *
import os

if os.getenv("DEBUG"):
    try:
            ave = AVE()
            ave.start()
    except AVEQuit:
            ave.exit()
            print("Goodbye...")
    finally:
            ave.exit()
else:
    while True:
        try:
            ave = AVE()
            ave.start()
        except AVEQuit:
            ave.exit()
            print("Goodbye...")
            break
        except:
            ave.exit()
            break

