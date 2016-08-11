### Author: mscroggs
### Description: AVE text game
### Category: Game
### License: MIT
### Appname: AVE
### reboot-before-run: True

import sys
sys.path.append("apps/mscroggs~ave")

from core import errors as e
from core.ave import AVE
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
        if 'current.items' in os.listdir('apps/mscroggs~ave/games'):
            os.remove('apps/mscroggs~ave/games/current.items')
        ave.exit()
        break
    except e.AVEToMenu:
        started = False
    finally:
        if 'current.items' in os.listdir('apps/mscroggs~ave/games'):
            os.remove('apps/mscroggs~ave/games/current.items')
