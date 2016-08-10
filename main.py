#!/usr/bin/env python
### reboot-before-run: True

import pyb

# This block may become unnecessary if the meta-tag above is implemented
import stm
if stm.mem8[0x40002850] == 0:
    with open("main.json", 'w') as f:
        f.write('{"main":"mscroggs~ave"}')
    stm.mem8[0x40002850] = 2
    pyb.hard_reset()
# end of block

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
        ave.exit()
    except e.AVEToMenu:
        started = False
