#!/usr/bin/env python
from __future__ import division
import os
import os.path
import shutil
import sys

class BadArg(BaseException):
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string

if len(sys.argv) < 2:
    raise BadArg("Please enter a type to build")
if sys.argv[1] not in ["python","emf"]:
    raise BadArg("Unknown type")

dir = os.path.dirname(os.path.realpath(__file__))
b_dir = os.path.join(dir,"build")
# empty /build
for f in os.listdir(b_dir):
    try:
        os.remove(os.path.join(b_dir,f))
    except:
        shutil.rmtree(os.path.join(b_dir,f))

# copy games
shutil.copytree(os.path.join(dir,"games"), os.path.join(b_dir,"games"))
shutil.copy(os.path.join(dir,"VERSION"), os.path.join(b_dir,"VERSION"))

# copy version specific files
if sys.argv[1] == "python":
    shutil.copy(os.path.join(dir,"python/run.py"), b_dir)
    shutil.copytree(os.path.join(dir,"python/core"), os.path.join(b_dir,"core"))

if sys.argv[1] == "emf":
    with open(os.path.join(b_dir,"VERSION"),"a") as f:
        f.write("~")
    with open(os.path.join(b_dir,"__init__.py"),"w") as f:
        pass
    shutil.copy(os.path.join(dir,"emf/main.py"), b_dir)
    shutil.copytree(os.path.join(dir,"emf/core"), os.path.join(b_dir,"core"))

# copy common files
shutil.copy(os.path.join(dir,"commoncore/errors.py"), os.path.join(b_dir,"core"))
