# dimensions: (height) 45
#             (width) 80
from core.utils import *
from core.errors import *
import curses
import signal
HEIGHT = 25
WIDTH = 80

def catch_resize(dummy=None,dummy2=None):
    curses.resizeterm(HEIGHT,WIDTH)

signal.signal(signal.SIGWINCH, catch_resize)



class Screen:
    def __init__(self):
        print("\x1b[8;"+str(HEIGHT)+";"+str(WIDTH)+"t")
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, -1, curses.COLOR_RED)
        curses.init_pair(2, -1, curses.COLOR_GREEN)
        curses.init_pair(3, -1, curses.COLOR_BLUE)
        curses.init_pair(4, -1, curses.COLOR_YELLOW)
        curses.init_pair(5, -1, curses.COLOR_RED)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        curses.resizeterm(HEIGHT,WIDTH)
        self.stdscr.refresh()

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
        import os
        stuff = []
        stuff2 = []
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"title")) as f:
            y = 0
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
                        else:
                            stuff.append((y, x, c, curses.color_pair(0)))
                    y += 1
                elif comment(line) == "type":
                    self.show(stuff,y=y+1)
                    y_beg = y
                    stuff = []
                    y = 0
        self.type(stuff,py=y_beg,y=y)

    def type(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH):
        from time import sleep
        pad = self.newpad(y, x)
        for char in stuff:
            if char[2]!=" ":
                sleep(.01)
            if len(char)==3:
                pad.addch(char[0], char[1], char[2])
            if len(char)==4:
                pad.addch(char[0], char[1], char[2], char[3])
            pad.refresh(0,0, py,px, y+py,x+px)

    def show(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH):
        pad = self.newpad(y, x)
        for char in stuff:
            if len(char)==3:
                pad.addch(char[0], char[1], char[2])
            if len(char)==4:
                pad.addch(char[0], char[1], char[2], char[3])
        pad.refresh(0,0, py,px, y+py,x+px)

    def menu(self, ls, y=4, py=None, selected=0):
        if py is None:
            py = HEIGHT - y - 1
        self.show_menu(ls, y, py, selected)
        key = ""
        while key is not None:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER,ord("\n"),ord("\r")]:
                return selected
            if key == curses.KEY_UP:
                selected -= 1
                if selected < 0:
                    selected += len(ls)
                self.show_menu(ls, y, py, selected)
            if key == curses.KEY_DOWN:
                selected += 1
                if selected >= len(ls):
                    selected -= len(ls)
                self.show_menu(ls, y, py, selected)
            if key == ord('q'):
                raise AVEQuit

    def show_menu(self, ls, y, py, selected):
        start = min(max(0,selected-y/2),max(0,len(ls)-y))
        pad = self.newpad(y)
        for y_pos in range(y):
            if start + y_pos < len(ls):
                title = ls[start+y_pos]
            else:
                title = ""
            col = curses.color_pair(4)
            if y_pos+start == selected:
                col = curses.color_pair(5)
            pad.addstr(y_pos,1,title[:WIDTH-5] + " "*(WIDTH-5-len(title)),col)
        if start > 0:
            pad.addch(0,WIDTH-2,"^")
        if start < max(0,len(ls) - y):
            pad.addch(y-1,WIDTH-2,"v")
        pad.refresh(0,0, py,0, py+y,WIDTH)
