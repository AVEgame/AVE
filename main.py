#!/usr/bin/env python
import pyb
with open('/flash/main.json', 'w') as f:
    f.write('{"main":"apps/mscroggs~ave/run.py"}')
