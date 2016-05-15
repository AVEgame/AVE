# dimensions: (height) 45
#             (width)  80
from __future__ import division
from core.utils import *
from core.errors import *
import curses
import signal
HEIGHT = 25
WIDTH = 80

def catch_resize(dummy=None,dummy2=None):
    curses.resizeterm(HEIGHT,WIDTH)

signal.signal(signal.SIGWINCH, catch_resize)

class DummyScreen:
    def clear(self):
        pass

class Screen:
    def __init__(self):
        print("\x1b[8;"+str(HEIGHT)+";"+str(WIDTH)+"t")
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()

        # @ in title and credits
        curses.init_pair(1, -1, curses.COLOR_RED)
        # ^ in title and credits
        curses.init_pair(2, -1, curses.COLOR_GREEN)
        # = in title and credits
        curses.init_pair(3, -1, curses.COLOR_BLUE)
        # menu unselected
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        # menu selected
        curses.init_pair(5, -1, curses.COLOR_RED)
        # A in title
        curses.init_pair(6, curses.COLOR_RED, -1)
        # V in title
        curses.init_pair(7, curses.COLOR_GREEN, -1)
        # E in title
        curses.init_pair(8, curses.COLOR_BLUE, -1)
        # inventory
        curses.init_pair(9, -1, curses.COLOR_BLUE)
        # gameover
        curses.init_pair(10, -1, curses.COLOR_BLUE)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        curses.resizeterm(HEIGHT,WIDTH)
        self.stdscr.refresh()

    def clear(self):
        pad = self.newpad()
        pad.refresh(0,0, 0,0, HEIGHT,WIDTH)

    def close(self):
        curses.nocbreak()
        curses.curs_set(1)
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def print_room_desc(self,desc):
        print desc

    def print_options(self,options,n):
        print options

    def newpad(self, y=HEIGHT, x=WIDTH):
        return curses.newpad(y, x)

    def print_titles(self):
        self.print_file("title")

    def print_credits(self):
        self.print_file("credits")

    def print_file(self, filename):
        import os
        stuff = []
        stuff2 = []
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)) as f:
            y = 0
            y_beg = None
            for line in f.readlines():
                if line[0]!="#":
                    line = clean_newlines(line)
                    for x,c in enumerate(line):
                        if c == "@":
                            stuff.append((y, x, " ", curses.color_pair(1)))
                        elif c == "^":
                            stuff.append((y, x, " ", curses.color_pair(2)))
                        elif c == "=":
                            stuff.append((y, x, " ", curses.color_pair(3)))
                        elif c == "A" and len(line) > x+1 and line[x+1] == "V" and len(line) > x+2 and line[x+2] == "E":
                            stuff.append((y, x, "A", curses.color_pair(6)))
                        elif x >= 1 and line[x-1] == "A" and c == "V" and len(line) > x+1 and line[x+1] == "E":
                            stuff.append((y, x, "V", curses.color_pair(7)))
                        elif x >= 2 and line[x-2] == "A" and line[x-1] == "V" and c == "E":
                            stuff.append((y, x, "E", curses.color_pair(8)))
                        else:
                            stuff.append((y, x, c, curses.color_pair(0)))
                    y += 1
                elif comment(line) == "type":
                    self.show(stuff,y=y+1,x=WIDTH)
                    y_beg = y
                    stuff = []
                    y = 0
        if y_beg is None:
            self.show(stuff,y=y+1,x=WIDTH)
        else:
            self.type(stuff,py=y_beg,y=y,x=WIDTH, title=True)

    def gameover(self):
        pad = self.newpad(8, WIDTH-20)
        gst = " "*((WIDTH-29)//2) + "GAME OVER"
        gst += " " * (WIDTH - len(gst))
        pad.addstr(0,0," "*(WIDTH-20),curses.color_pair(10))
        pad.addstr(1,0,gst,curses.color_pair(10))
        pad.addstr(2,0," "*(WIDTH-20),curses.color_pair(10))
        pad.addstr(3,0," "*(WIDTH-20),curses.color_pair(10))
        pad.addstr(4,0," "*(WIDTH-20),curses.color_pair(10))
        pad.addstr(5,0," "*(WIDTH-20),curses.color_pair(10))
        pad.addstr(6,0," "*(WIDTH-20),curses.color_pair(10))
        pad.refresh(0,0, 3,10, 9,WIDTH-10)
        return self.menu(["Play again","Play another game","Quit"], 3, 6, wx=WIDTH-30, controls=False)
        
    def show_inventory(self, inventory):
        pad = self.newpad(14, 20)
        pad.addstr(0,0,"INVENTORY" + " "*11,curses.color_pair(9))
        for i in range(12):
            if i < len(inventory):
                item = inventory[i]
                pad.addstr(i+1,0,"  " + item[:18] + " " * (18-len(item)),curses.color_pair(9))
            else:
                pad.addstr(i+1,0," " * 20,curses.color_pair(9))
        pad.refresh(0,0, 1,WIDTH-20, 13,WIDTH)
        
    def type(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH-21, title=False):
        from time import sleep
        pad = self.newpad(y, x)
        delay = True
        self.stdscr.nodelay(1)
        for char in stuff:
            if self.stdscr.getch() != -1:
                delay = False
            if char[2]!=" " and (delay or title):
                sleep(.01)
            if len(char)==3:
                pad.addch(char[0], char[1], char[2])
            if len(char)==4:
                pad.addch(char[0], char[1], char[2], char[3])
            pad.refresh(0,0, py,px, y+py,x+px)
        self.stdscr.nodelay(0)

    def show(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH-21):
        pad = self.newpad(y, x)
        for char in stuff:
            if len(char)==3:
                pad.addch(char[0], char[1], char[2])
            if len(char)==4:
                pad.addch(char[0], char[1], char[2], char[3])
        pad.refresh(0,0, py,px, y+py,x+px)

    def credit_menu(self):
        key = ""
        while key is not None:
            key = self.stdscr.getch()
            if key == ord('q') or key == ord('c'):
                break
        self.print_titles()

    def menu(self, ls, y=4, py=None, selected=0, wx=WIDTH, controls=True, add=None, rem=None, character=None, titles=False):
        if py is None:
            py = HEIGHT - y - 1
        self.show_menu(ls, y, py, selected, wx, controls)
        key = ""
        while key is not None:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER,ord("\n"),ord("\r")]:
                if character is not None and add is not None:
                    character.add_items(add[selected])
                if character is not None and rem is not None:
                    character.remove_items(rem[selected])
                return selected
            if key == curses.KEY_UP:
                selected -= 1
                if selected < 0:
                    selected += len(ls)
                self.show_menu(ls, y, py, selected, wx, controls)
            if key == curses.KEY_DOWN:
                selected += 1
                if selected >= len(ls):
                    selected -= len(ls)
                self.show_menu(ls, y, py, selected, wx, controls)
            if key == ord('q'):
                if titles:
                    raise AVEQuit
                else:
                    raise AVEToMenu
            if key == ord('c') and titles:
                self.print_credits()
                self.credit_menu()
                self.show_menu(ls, y, py, selected, wx, controls)

    def show_menu(self, ls, y, py, selected, wx, controls):
        if controls:
            wide = wx-4
        else:
            wide = wx
        start = min(max(0,selected-y//2),max(0,len(ls)-y))
        pad = self.newpad(y+1,wx)
        for y_pos in range(y):
            if start + y_pos < len(ls):
                title = ls[start+y_pos]
            else:
                title = ""
            col = curses.color_pair(4)
            if y_pos+start == selected:
                col = curses.color_pair(5)
            pad.addstr(y_pos,0," "+title[:wide-1] + " "*(wide-1-len(title)),col)
        if controls:
            if start > 0:
                pad.addch(0,wx-2,"^")
            if start < max(0,len(ls) - y):
                pad.addch(y-1,wx-2,"v")
        pad.refresh(0,0, py,(WIDTH-wx)//2, py+y-1,wx+(WIDTH-wx)//2)
