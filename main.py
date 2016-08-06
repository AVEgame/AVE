#!/usr/bin/env python
import sys
sys.path.append("apps/mscroggs~ave")

from core import ave as a
from core import errors as e
import os

started = False

try:
    ave = a.AVE()
    started = True
    ave.start()
except e.AVEQuit:
    ave.exit()
    print("Goodbye...")
finally:
    if started:
        ave.exit()
