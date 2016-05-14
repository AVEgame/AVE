import sys
import curses
from curses import panel

class Menu(object):

    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0,0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(('exit','exit'))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = '%d. %s' % (index, item[0])
                self.window.addstr(1+index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items)-1:
                    break
                else:
                    self.items[self.position][1]()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

class MyApp(object):

    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        submenu_items = [
                ('beep', curses.beep),
                ('flash', curses.flash)
                ]
        submenu = Menu(submenu_items, self.screen)

        main_menu_items = [
                ('beep', curses.beep),
                ('flash', curses.flash),
                ('submenu', submenu.display)
                ]
        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()

def AVE():
    screen=stdscreen
    curses.curs_set(0)
    Menu(list,stdscreen)

class MyException:
    pass

if len(sys.argv)==1:
    print("You need to pick a game")
    raise(MyException)

game={}
current=None

with open(sys.argv[1],'r') as f:
    for line in f.readlines():
      this_line=line.strip("\n")
      if this_line!="":
        if this_line[0]=='#':
            if this_line=='#title':
                pass
            else:
                current=this_line.strip('#')
                game[current]=['',[]]
        elif current!=None:
            if '=>' in this_line:
                sp=this_line.split(" => ")
                game[current][1].append((sp[0],sp[1]))
            else:
                game[current][0]+=this_line+"\n"

print game['start'][0]
for thing in game['start'][1]:
    print thing

#stdscr = curses.initscr()

curses.wrapper(AVE('start'))
