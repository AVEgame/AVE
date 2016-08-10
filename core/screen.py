# dimensions: (height) 240
#             (width)  320
import sys
sys.path.append("apps/mscroggs~ave")

from core import utils as u
from core import errors as e
import ugfx
import buttons
import pyb
REPEATRATE = 331
HEIGHT = 20
WIDTH = 36

DX=9
DY=12

buttons.init()

s=ugfx.Style()

s.set_background(ugfx.BLACK)
s.set_enabled([ugfx.WHITE,ugfx.WHITE,ugfx.WHITE,ugfx.WHITE])
s.set_disabled([ugfx.WHITE,ugfx.WHITE,ugfx.WHITE,ugfx.WHITE])
s.set_pressed([ugfx.WHITE,ugfx.WHITE,ugfx.WHITE,ugfx.WHITE])
s.set_focus(ugfx.WHITE)

def get_colors(n):
    if n == 1:  return ugfx.BLACK,ugfx.RED
    if n == 2:  return ugfx.BLACK,ugfx.GREEN
    if n == 3:  return ugfx.BLACK,ugfx.BLUE
    if n == 4:  return ugfx.BLACK,ugfx.YELLOW
    if n == 5:  return ugfx.BLACK,ugfx.RED
    if n == 6:  return ugfx.RED,None
    if n == 7:  return ugfx.GREEN,None
    if n == 8: return ugfx.BLUE, None
    if n == 9:  return ugfx.BLACK,ugfx.BLUE
    if n == 10: return ugfx.BLACK,ugfx.BLUE
    return ugfx.WHITE,None

class DummyScreen:
    def clear(self):
        pass

class Screen:
    def __init__(self):
        ugfx.init()
        buttons.init()
        self.clear()

    def clear(self):
        ugfx.clear(ugfx.BLACK)

    def close(self):
        pass

    def print_room_desc(self,desc):
        print(desc)

    def print_options(self,options,n):
        print(options)

    def print_titles(self):
        self.print_file("title")

    def print_credits(self):
        self.print_file("credits")

    def put_ave_logo(self):
        ugfx.text(320-DX*3,1,"A",ugfx.RED)
        ugfx.text(320-DX*2,1,"V",ugfx.GREEN)
        ugfx.text(320-DX,  1,"E",ugfx.BLUE)

    def print_file(self, filename):
        import os
        self.clear()
        stuff = []
        stuff2 = []
        with open("apps/mscroggs~ave/core/"+filename) as f:
            y = 0
            for line in f:
                if line[0]!="#":
                    line = u.clean_newlines(line)
                    for x,c in enumerate(line):
                        if x>=WIDTH:
                            break
                        if c == "@":
                            ugfx.area(DX*x,DY*y,DX,DY,ugfx.RED)
                        elif c == "^":
                            ugfx.area(DX*x,DY*y,DX,DY,ugfx.GREEN)
                        elif c == "=":
                            ugfx.area(DX*x,DY*y,DX,DY,ugfx.BLUE)
                    line = " ".join(line.split("@"))
                    line = " ".join(line.split("^"))
                    line = " ".join(line.split("="))
                    ugfx.text(0,DY*y+1,line,ugfx.WHITE)
                    y += 1

    def gameover(self):
        return self.gameend("GAME OVER")

    def winner(self):
        return self.gameend("YOU WIN!")

    def gameend(self,text):
        ugfx.text(1,1,text,ugfx.WHITE)
        return self.menu(["Play again","Play another game","Quit"], 3, wx=WIDTH-30, controls=False, titles=True)

    def show_inventory(self, inventory):
        ugfx.area(220,0,100,13*DY,ugfx.BLUE)
        ugfx.text(220,1,"INVENTORY",ugfx.WHITE)
        for i in range(12):
            if i<len(inventory):
                ugfx.text(220,1+DY*(1+i),inventory[i],ugfx.WHITE)

    def type(self, text, py=0, px=0, y=HEIGHT, x=WIDTH-21, title=False):
        ugfx.Label(0,0,215,13*DY,text,style=s,justification=ugfx.Label.LEFTTOP)

    def credit_menu(self):
        while True:
            pyb.wfi()
            if buttons.is_pressed("BTN_A") or buttons.is_pressed("BTN_B"):
                pyb.delay(REPEATRATE)
                break
        self.print_titles()

    def menu(self, ls, y=4, selected=0, wx=WIDTH, controls=True, add=None, rem=None, character=None, titles=False):
        pyb.delay(REPEATRATE)
        self.show_menu(ls, y, selected, wx, controls)

        while True:
            pyb.wfi()
            if buttons.is_pressed("BTN_A"):
                if character is not None and add is not None:
                    character.add_items(add[selected])
                if character is not None and rem is not None:
                    character.remove_items(rem[selected])
                self.clear()
                pyb.delay(REPEATRATE)
                return selected
            if buttons.is_pressed("JOY_DOWN"):
                selected -= 1
                if selected < 0:
                    selected += len(ls)
                self.show_menu(ls, y, selected, wx, controls)
                pyb.delay(REPEATRATE)
            if buttons.is_pressed("JOY_UP"):
                selected += 1
                if selected >= len(ls):
                    selected -= len(ls)
                self.show_menu(ls, y, selected, wx, controls)
                pyb.delay(REPEATRATE)
            if buttons.is_pressed("BTN_MENU"):
                if titles:
                    raise e.AVEQuit
                else:
                    raise e.AVEToMenu
            if buttons.is_pressed("BTN_B") and titles:
                pyb.delay(REPEATRATE)
                self.print_credits()
                self.credit_menu()
                self.show_menu(ls, y, selected, wx, controls)
            elif buttons.is_pressed("BTN_B"):
                pyb.delay(REPEATRATE)
                return "inv"

    def show_menu(self, ls, y, selected, wx, controls):
        if controls:
            wide = wx-4
        else:
            wide = wx
        ugfx.area(0,240-y*DY,320,y*DY,ugfx.YELLOW)

        start = min(max(0,selected-y//2),max(0,len(ls)-y))
        for y_pos in range(y):
            if start + y_pos < len(ls):
                title = ls[start+y_pos]
            else:
                title = ""
            col = (4)
            if y_pos+start == selected:
                col = (5)
                ugfx.area(0,240-y*DY+y_pos*DY,320,DY,ugfx.RED)
                ugfx.text(6,1+240-y*DY+y_pos*DY,title,ugfx.WHITE)
            else:
                ugfx.text(6,1+240-y*DY+y_pos*DY,title,ugfx.BLACK)

        if controls:
            if start > 0:
                ugfx.text(320-DX-1,240-y*DY+1,"^",ugfx.WHITE)
            if start < max(0,len(ls) - y):
                ugfx.text(320-DX-1,240-DY+1,"v",ugfx.WHITE)

    def show_titles(self, title, description, author):
        stuff = []
        y = 0
        for y in range(HEIGHT):
            if y == 0 or y == HEIGHT-1:
                xs = range(0,WIDTH-3,4)
            else:
                xs = [0,WIDTH - 4]
            for x in xs:
                ugfx.text(x*DX,y*DY,"A",ugfx.RED)
                ugfx.text(x*DX+DX,y*DY,"V",ugfx.GREEN)
                ugfx.text(x*DX+2*DX,y*DY,"E",ugfx.BLUE)

        stuff = []
        ugfx.Label(DX*4,DY,(WIDTH-8)*DX,DY,title,justification=ugfx.Label.CENTER,style=s)
        ugfx.Label(DX*4,2*DY,(WIDTH-8)*DX,DY,"By: "+author,justification=ugfx.Label.CENTER,style=s)
        ugfx.Label(DX*4,4*DY,(WIDTH-8)*DX,(HEIGHT-6)*DY,description,justification=ugfx.Label.LEFTTOP,style=s)
        ugfx.Label(DX*4,(HEIGHT-2)*DY,(WIDTH-8)*DX,DY,"<A> begin  <B> menu",justification=ugfx.Label.CENTER,style=s)

        while True:
            pyb.wfi()
            if buttons.is_pressed("BTN_A"):
                pyb.delay(REPEATRATE)
                break
            if buttons.is_pressed("BTN_MENU"):
                pyb.delay(REPEATRATE)
                raise e.AVEToMenu
