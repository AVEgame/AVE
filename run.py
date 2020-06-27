#!/usr/bin/python
from ave import AVE
from ave.exceptions import AVEQuit
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
