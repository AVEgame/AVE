#!/usr/bin/env python
<<<<<<< HEAD
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
        print("Goodbye...")
        break
    finally:
        if started:
            ave.exit()
        break
=======
import pyb
with open('/flash/main.json', 'w') as f:
    f.write('{"main":"apps/mscroggs~ave/run.py"}')
>>>>>>> origin/emf-gin
