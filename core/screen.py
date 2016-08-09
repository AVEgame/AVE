# dimensions: (height) 45
#             (width)  80
import sys
sys.path.append("apps/mscroggs~ave")

from core import utils as u
from core import errors as e
import ugfx
import buttons
import pyb
REPEATRATE = 331
HEIGHT = 21
WIDTH = 36

DX=9
DY=11

buttons.init()

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
        stuff = [(0,0,"A",(6)), (0,1,"V",(7)), (0,2,"E",(8))]
        self.show(stuff,0,WIDTH-3,2,3)

    def print_file(self, filename):
        import os
        self.clear()
        stuff = []
        stuff2 = []
        with open("apps/mscroggs~ave/core/"+filename) as f:
            y = 0
            for line in f.readlines():
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
                
    def type(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH-21, title=False):
        linelen = 0
        y = 0
        line = ""
        for word in stuff.split(" "):
            linelen += 1+len(word)
            if linelen < 30:
                line += " "+word
            else:
                ugfx.text(1,1+y*DY,line,ugfx.WHITE)
                y += 1
                line = word
                linelen = 0
        if linelen > 0:
            ugfx.text(1,1+y*DY,line,ugfx.WHITE)

    def show(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH-21):
        for char in stuff:
            if len(char)==3:
                ugfx.text(DX*(char[1]+px)+1,DY*(char[0]+py)+1,char[2],ugfx.WHITE)
            if len(char)==4:
                col = get_colors(char[3])
                if col[1] is not None:
                    ugfx.area(DX*(char[1]+px),DY*(char[0]+py)+1,DX,DY,col[1])
                ugfx.text(DX*(char[1]+px)+1,DY*(char[0]+py)+1,char[2],col[0])

    def credit_menu(self):
        key = ""
        while key is not None:
            key = self.stdscr.getch()
            if key == ord('q') or key == ord('c'):
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
                stuff.append((y, x, "A", (6)))
                stuff.append((y, x+1, "V", (7)))
                stuff.append((y, x+2, "E", (8)))
        self.show(stuff, x=WIDTH)

        stuff = []
        pad, y, x = self.pad_with_coloured_dashes(title,0,0,HEIGHT-2,WIDTH-11)
        stuff += pad
        y += 1
        txt = "By: "+author
        for st in range(0,len(txt),WIDTH-9):
            for x,c in enumerate(txt[st:st+WIDTH-9]):
                stuff.append((y, x, c))
            y += 1
        y += 1
        x = 0
        for word in description.split():
            if x + len(word) > WIDTH-9:
                x = 0
                y += 1
                if y > HEIGHT-5:
                    pyb.delay(REPEATRATE)
                    break
            for c in word:
                stuff.append((y, x, c))
                x += 1
            x += 1
        pad, y, x = self.pad_with_coloured_dashes("<A> begin  <B> menu",HEIGHT-4,0,HEIGHT-2,WIDTH-11)
        stuff += pad

        self.show(stuff,x=WIDTH-9,y=HEIGHT-2,px=4,py=1)


        while True:
            pyb.wfi()
            if buttons.is_pressed("BTN_A"):
                break
            if buttons.is_pressed("BTN_MENU"):
                raise e.AVEToMenu

    def pad_with_coloured_dashes(self, text, y=0, x=0, yw=HEIGHT, xw=WIDTH):
        temp_stuff = []
        text = [" "+text[st:st+WIDTH-11]+ " " for st in range(0,len(text),xw)]
        cols = [(6), (7), (8)]
        for t in text[:yw]:
            half = (WIDTH-9-len(t))//2
            for x in range(WIDTH-9):
                if half <= x < half + len(t):
                    temp_stuff.append((y, x, t[x-half]))
                elif x%4 != 3:
                    temp_stuff.append((y, x, "~", cols[x%4]))
                else:
                    temp_stuff.append((y, x, " "))
            y += 1
        return temp_stuff, y, x

