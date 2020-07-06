"""Use curses to display the game in terminal."""

from ..exceptions import AVEToMenu, AVEQuit
from .. import config
from ..parsing.string_functions import clean_newlines
from .base import Screen
import curses

HEIGHT = 25
WIDTH = 80


class CursesScreen(Screen):
    """The Screen class that looks after curses."""

    def __init__(self, cbreak=True):
        """Make the screen."""
        self.stdscr = curses.initscr()

        try:
            # Resize terminal iff it is too small
            y, x = self.stdscr.getmaxyx()
            if y < HEIGHT or x < WIDTH:
                print("\x1b[8;" + str(HEIGHT + 2) + ";" + str(WIDTH + 2) + "t")
                curses.resizeterm(HEIGHT + 2, WIDTH + 2)
        except AttributeError:
            # Windows
            pass

        curses.start_color()
        curses.use_default_colors()
        # curses.assume_default_colors(-1, curses.COLOR_MAGENTA)

        bg_color = curses.COLOR_BLACK
        if curses.can_change_color():
            curses.init_color(curses.COLOR_MAGENTA, 190, 40, 140)
            bg_color = curses.COLOR_MAGENTA

        # @ in title and credits
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        # ^ in title and credits
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        # = in title and credits
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
        # menu unselected
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        # menu selected
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
        # A in title
        curses.init_pair(6, curses.COLOR_RED, bg_color)
        # V in title
        curses.init_pair(7, curses.COLOR_GREEN, bg_color)
        # E in title
        curses.init_pair(8, curses.COLOR_BLUE, bg_color)
        # inventory
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLUE)
        # gameover
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLUE)
        # blank
        curses.init_pair(11, curses.COLOR_WHITE, bg_color)

        curses.noecho()
        if cbreak:
            curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        self.stdscr.refresh()

    def no_internet(self):
        """Display a "You have no internet" message."""
        stuff = []
        for i, c in enumerate("Unable to load from the internet. "
                              "Press <q> to go back."):
            stuff.append((0, i, c, curses.color_pair(8)))
        self.show(stuff, 15, 5, 1, 56)

    def clear(self):
        """Clear the screen."""
        pad = self.newpad()
        pad.refresh(0, 0, 1, 1, HEIGHT, WIDTH)

    def close(self, cbreak=True):
        """Close the curses screen."""
        if cbreak:
            curses.nocbreak()
        curses.curs_set(1)
        self.stdscr.keypad(0)
        curses.echo()
        if cbreak:
            curses.endwin()

    def newpad(self, y=HEIGHT, x=WIDTH):
        """Make a new pad to write to the screen."""
        pad = curses.newpad(y + 1, x)
        for ypos in range(y):
            pad.addstr(ypos, 0, " " * x, curses.color_pair(11))
        return pad

    def put_ave_logo(self):
        """Print the AVE logo at the top of the screen."""
        stuff = [(0, 0, "A", curses.color_pair(6)),
                 (0, 1, "V", curses.color_pair(7)),
                 (0, 2, "E", curses.color_pair(8))]
        self.show(stuff, 0, WIDTH - 3, 2, 3)

    def print_file(self, filename):
        """Print the contents of a text file."""
        import os
        self.clear()
        stuff = []
        with open(os.path.join(config.screens_folder, filename)) as f:
            y = 0
            y_beg = None
            for line in f.readlines():
                if line[0] != "#":
                    line = clean_newlines(line)
                    for x, c in enumerate(line):
                        if x >= WIDTH:
                            break
                        if c == "@":
                            stuff.append((y, x, " ", curses.color_pair(1)))
                        elif c == "^":
                            stuff.append((y, x, " ", curses.color_pair(2)))
                        elif c == "=":
                            stuff.append((y, x, " ", curses.color_pair(3)))
                        elif c == "A" and len(line) > x + 1 \
                                and line[x + 1] == "V" \
                                and len(line) > x + 2 and line[x + 2] == "E":
                            stuff.append((y, x, "A", curses.color_pair(6)))
                        elif x >= 1 and line[x - 1] == "A" and c == "V" \
                                and len(line) > x + 1 and line[x + 1] == "E":
                            stuff.append((y, x, "V", curses.color_pair(7)))
                        elif x >= 2 and line[x - 2] == "A" \
                                and line[x - 1] == "V" and c == "E":
                            stuff.append((y, x, "E", curses.color_pair(8)))
                        else:
                            stuff.append((y, x, c, curses.color_pair(11)))
                    y += 1
                    if y >= HEIGHT:
                        y -= 1
                        break
                elif "# type" in line:
                    self.show(stuff, y=y + 1, x=WIDTH)
                    y_beg = y
                    stuff = []
                    y = 0
        if y_beg is None:
            self.show(stuff, y=y + 1, x=WIDTH)
        else:
            self.type(stuff, py=y_beg, y=y, x=WIDTH, title=True)

    def gameover(self):
        """Show the game over screen."""
        return self.gameend("GAME OVER")

    def winner(self):
        """Show the "you win" screen."""
        return self.gameend("YOU WIN!")

    def gameend(self, text):
        """Allow the user to play again or go back to the menu."""
        pad = self.newpad(10, WIDTH - 19)
        gst = " " * ((WIDTH - 29) // 2) + text
        gst += " " * (WIDTH - len(gst))
        gst = gst[:WIDTH - 20]
        pad.addstr(1, 0, " " * (WIDTH - 20), curses.color_pair(10))
        pad.addstr(2, 0, gst, curses.color_pair(10))
        pad.addstr(3, 0, " " * (WIDTH - 20), curses.color_pair(10))
        pad.addstr(4, 0, " " * (WIDTH - 20), curses.color_pair(10))
        pad.addstr(5, 0, " " * (WIDTH - 20), curses.color_pair(10))
        pad.addstr(6, 0, " " * (WIDTH - 20), curses.color_pair(10))
        pad.addstr(7, 0, " " * (WIDTH - 20), curses.color_pair(10))
        pad.refresh(0, 0, 4, 11, 12, WIDTH - 9)
        return self.gameover_menu(["Play again", "Play another game", "Quit"])

    def show_inventory(self, inventory):
        """Display the inventory."""
        pad = self.newpad(14, 20)
        pad.addstr(0, 0, "INVENTORY" + " " * 10, curses.color_pair(9))
        for i in range(12):
            if i < len(inventory):
                item = inventory[i]
                pad.addstr(
                    i + 1, 0,
                    "  " + item[:17] + " " * (17 - len(item)),
                    curses.color_pair(9))
            else:
                pad.addstr(i + 1, 0, " " * 19, curses.color_pair(9))
        pad.refresh(0, 0, 2, WIDTH - 19, 14, WIDTH)

    def type_room_text(self, text):
        """Type the room text."""
        y = 0
        x = 0
        stuff = []
        text = text.replace("\n", " \n ")
        for word in text.split(" "):
            if word == "\n":
                y += 1
                x = 0
            elif word != "":
                if x + len(word) > WIDTH - 22:
                    y += 1
                    x = 0
                for i, c in enumerate(word):
                    stuff.append((y, x, c))
                    x += 1
                stuff.append((y, x, " "))
                x += 1
        self.type(stuff)

    def type(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH - 21,
             title=False):
        """Type some text."""
        from time import sleep
        pad = self.newpad(y, x)
        delay = True
        self.stdscr.nodelay(1)
        for char in stuff:
            if char[0] < y and char[1] < x:
                if self.stdscr.getch() != -1:
                    delay = False
                if char[2] != " " and (delay or title):
                    sleep(.01)
                if len(char) == 3:
                    pad.addch(char[0], char[1], char[2], curses.color_pair(11))
                if len(char) == 4:
                    pad.addch(char[0], char[1], char[2], char[3])
                pad.refresh(0, 0, py + 1, px + 1, y + py, x + px)
        self.stdscr.nodelay(0)

    def show(self, stuff, py=0, px=0, y=HEIGHT, x=WIDTH - 21):
        """Add a pad to the screen."""
        pad = self.newpad(y, x)
        for char in stuff:
            if char[0] < y and char[1] < x:
                if len(char) == 3:
                    pad.addch(char[0], char[1], char[2], curses.color_pair(11))
                if len(char) == 4:
                    pad.addch(char[0], char[1], char[2], char[3])
        pad.refresh(0, 0, py + 1, px + 1, y + py, x + px)

    def title_menu(self, ls, selected=0):
        """Let the user pick a built in game or go to download menu."""
        return self._internal_menu(ls, 8, selected=selected, credits=True)

    def download_menu(self, ls, selected=0):
        """Let the user pick a game from the online library."""
        return self._internal_menu(ls, 12, selected=selected)

    def gameover_menu(self, ls, selected=0):
        """Give the user some options for what to do after game ends."""
        return self._internal_menu(
            ls, 3, 6, wx=WIDTH - 30, selected=selected, controls=False,
            credits=True)

    def menu(self, ls, selected=0):
        """Give the user some options for what to do next."""
        return self._internal_menu(ls, min(8, len(ls)), selected=selected)

    def wait_for_input(self, keys=['q']):
        """Wait for the user to press a key."""
        key = ""
        keys = [ord(i) for i in keys]
        while key is not None:
            key = self.stdscr.getch()
            if key in keys:
                return

    def _internal_menu(self, ls, y=4, py=None, selected=0, wx=WIDTH,
                       controls=True, credits=False):
        """Give the user some options, and return the selected option."""
        if py is None:
            py = HEIGHT - y - 1
        self.show_menu(ls, y, py, selected, wx, controls)
        key = ""
        while key is not None:
            key = self.stdscr.getch()
            if key in [curses.KEY_ENTER, ord("\n"), ord("\r")]:
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
                if credits:
                    raise AVEQuit
                else:
                    raise AVEToMenu
            if key == ord('c') and credits:
                self.print_credits()
                self.wait_for_input(["q", "c"])
                self.print_titles()
                self.show_menu(ls, y, py, selected, wx, controls)

    def show_menu(self, ls, y, py, selected, wx, controls):
        """Display the menu."""
        if controls:
            wide = wx - 4
        else:
            wide = wx
        start = min(max(0, selected - y // 2), max(0, len(ls) - y))
        pad = self.newpad(y + 1, wx)
        for y_pos in range(y):
            if start + y_pos < len(ls):
                title = ls[start + y_pos]
            else:
                title = ""
            col = curses.color_pair(4)
            if y_pos + start == selected:
                col = curses.color_pair(5)
            pad.addstr(
                y_pos, 0,
                " " + title[: wide - 1] + " " * (wide - 1 - len(title)), col)
        if controls:
            if start > 0:
                pad.addch(0, wx - 2, "^", curses.color_pair(11))
            if start < max(0, len(ls) - y):
                pad.addch(y - 1, wx - 2, "v", curses.color_pair(11))
        pad.refresh(0, 0, py + 1, (WIDTH - wx) // 2 + 1, py + y,
                    wx + (WIDTH - wx) // 2)

    def show_titles(self, title, description, author, version):
        """Show the title screen for a game."""
        stuff = []
        y = 0
        for y in range(HEIGHT):
            if y == 0 or y == HEIGHT - 1:
                xs = range(0, WIDTH - 3, 4)
            else:
                xs = [0, WIDTH - 4]
            for x in xs:
                stuff.append((y, x, "A", curses.color_pair(6)))
                stuff.append((y, x + 1, "V", curses.color_pair(7)))
                stuff.append((y, x + 2, "E", curses.color_pair(8)))
        self.show(stuff, x=WIDTH)

        stuff = []
        pad, y, x = self.pad_with_coloured_dashes(
            title, 0, 0, HEIGHT - 2, WIDTH - 11)
        stuff += pad
        txt = "v" + str(version)
        for x, c in enumerate(txt):
            stuff.append((y - 1, WIDTH - 9 - len(txt) + x, c))
        y += 1
        txt = "Written by: " + author
        for st in range(0, len(txt), WIDTH - 9):
            for x, c in enumerate(txt[st: st + WIDTH - 9]):
                stuff.append((y, x, c))
            y += 1
        y += 1
        x = 0
        for word in description.split():
            if x + len(word) > WIDTH - 9:
                x = 0
                y += 1
                if y > HEIGHT - 5:
                    break
            for c in word:
                stuff.append((y, x, c))
                x += 1
            x += 1
        pad, y, x = self.pad_with_coloured_dashes(
            "Press <Enter> to begin. Press <q> to return to the menu.",
            HEIGHT - 4, 0, HEIGHT - 2, WIDTH - 11)
        stuff += pad

        self.show(stuff, x=WIDTH - 9, y=HEIGHT - 2, px=4, py=1)
        key = ""
        while key not in [curses.KEY_ENTER, ord("\n"), ord("\r")]:
            key = self.stdscr.getch()
            if key == ord('q'):
                raise AVEToMenu

    def pad_with_coloured_dashes(self, text, y=0, x=0, yw=HEIGHT, xw=WIDTH):
        """Pad text with coloured dashed to fill a row."""
        temp_stuff = []
        text = [" " + text[st: st + WIDTH - 11] + " "
                for st in range(0, len(text), xw)]
        cols = [curses.color_pair(6), curses.color_pair(7),
                curses.color_pair(8)]
        for t in text[: yw]:
            half = (WIDTH - 9 - len(t)) // 2
            for x in range(WIDTH - 9):
                if half <= x < half + len(t):
                    temp_stuff.append((y, x, t[x - half]))
                elif x % 4 != 3:
                    temp_stuff.append((y, x, "~", cols[x % 4]))
                else:
                    temp_stuff.append((y, x, " "))
            y += 1
        return temp_stuff, y, x
