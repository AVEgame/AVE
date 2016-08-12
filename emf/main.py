### Author: mscroggs
### Description: AVE text game
### Category: Game
### License: MIT
### Appname: AVE
### reboot-before-run: True

import sys
sys.path.append("apps/mscroggs~ave")

import errors as e
from ave import AVE
import os

import buttons
buttons.init()

started = False
while True:
    ave = AVE()
    try:
        started = True
        ave.start()
    except e.AVEQuit:
        ave.exit()
        break
    except e.AVEToMenu:
        started = False
