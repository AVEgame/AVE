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

class BadFile(BaseException):
    def __init__(self):
        pass
    def __str__(self):
        return "Game files must end in .ave"

def create_item_text(game):
    success = False
    text = ''
    with open(game, 'r') as f:
        for line in f:
            if line[0] == '%':
                success = True
            elif line[0] == '#':
                success = False
            if success:
                text += line
    return text

if len(sys.argv) < 2:
    raise BadArg("Please enter a type to build")
if sys.argv[1] not in ["python","emf","javascript"]:
    raise BadArg("Unknown type")

dir = os.path.dirname(os.path.realpath(__file__))
b_dir = os.path.join(dir,"build")

try:
    os.stat(b_dir)
except:
    os.mkdir(b_dir)

# empty /build
for f in os.listdir(b_dir):
    try:
        os.remove(os.path.join(b_dir,f))
    except:
        shutil.rmtree(os.path.join(b_dir,f))

# copy games
if sys.argv[1] == "emf":
    for f in os.listdir(os.path.join(dir,"games")):
        if f[-4:] == ".ave":
            shutil.copy(os.path.join(os.path.join(dir,"games"),f), b_dir)
            text = create_item_text(os.path.join(b_dir,f))
            with open(os.path.join(b_dir, f[:-4] + '.items'), 'w') as g:
                g.write(text)
elif sys.argv[1] == "javascript":
    from javascript import game_to_js
    os.mkdir(os.path.join(b_dir,"games"))
    gamelist = []
    for f in os.listdir(os.path.join(dir,"games")):
        if f[-4:] == ".ave":
            with open(os.path.join(os.path.join(dir,"games"),f)) as file:
                out,list_me = game_to_js(file.read())
            if list_me is not None:
                gamelist.append('"'+f[:-4]+'" : '+list_me)
            with open(os.path.join(os.path.join(b_dir,"games"),f[:-4]+".js"),"w") as file:
                file.write(out)
    with open(os.path.join(b_dir,"gamelist.js"),"w") as f:
        f.write("gameList={"+",".join(gamelist)+"};")
else:
    os.mkdir(os.path.join(b_dir,"games"))
    for f in os.listdir(os.path.join(dir,"games")):
        if f[-4:] == ".ave":
            shutil.copy(os.path.join(os.path.join(dir,"games"),f), os.path.join(b_dir,"games"))
    
# copy version specific files
if sys.argv[1] != "javascript":
    shutil.copy(os.path.join(dir,"VERSION"), os.path.join(b_dir,"VERSION"))

if sys.argv[1] == "javascript":
    shutil.copy(os.path.join(dir,"javascript/game.js"), b_dir)
    shutil.copy(os.path.join(dir,"javascript/game.php"), b_dir)
    shutil.copy(os.path.join(dir,"javascript/gameselect.js"), b_dir)
    shutil.copy(os.path.join(dir,"javascript/select.php"), b_dir)
    shutil.copy(os.path.join(dir,"javascript/sty.css"), b_dir)
    fromave = "function titleFromAVE(){return \""
    with open(os.path.join(dir,"javascript/title")) as f:
        fromave += "\\n".join(f.read().split("\n"))
    fromave += "\"}\nfunction creditsFromAVE(){return \""
    with open(os.path.join(dir,"javascript/credits")) as f:
        fromave += "\\n".join(f.read().split("\n"))
    fromave += "\"}\nfunction version(){return \""
    with open(os.path.join(dir,"VERSION")) as f:
        fromave += "\\n".join(f.read().split("\n"))
    fromave += "\"}"
    with open(os.path.join(b_dir,"fromave.js"),"w") as f:
        f.write(fromave)

if sys.argv[1] == "python":
    shutil.copy(os.path.join(dir,"python/run.py"), b_dir)
    shutil.copytree(os.path.join(dir,"python/core"), os.path.join(b_dir,"core"))
    shutil.copy(os.path.join(dir,"commoncore/errors.py"), os.path.join(b_dir,"core"))
    shutil.copy(os.path.join(dir,"commoncore/__init__.py"), os.path.join(b_dir,"core"))

if sys.argv[1] == "emf":
    with open(os.path.join(b_dir,"VERSION"),"a") as f:
        f.write("~")
    shutil.move(os.path.join(b_dir,"VERSION"),os.path.join(b_dir,"VERSION.ver"))
    shutil.copy(os.path.join(dir,"commoncore/errors.py"), b_dir)
    shutil.copy(os.path.join(dir,"commoncore/__init__.py"), b_dir)
    shutil.copy(os.path.join(dir,"emf/main.py"), b_dir)
    shutil.copy(os.path.join(dir,"emf/core/screen.py"), b_dir)
    shutil.copy(os.path.join(dir,"emf/core/ave.py"), b_dir)
    shutil.copy(os.path.join(dir,"emf/core/credits.tit"), b_dir)
    shutil.copy(os.path.join(dir,"emf/core/title.tit"), b_dir)
    shutil.copy(os.path.join(dir,"emf/core/screen.py"), b_dir)
    shutil.copy(os.path.join(dir,"emf/core/utils.py"), b_dir)
