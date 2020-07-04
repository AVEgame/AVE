import pytest
import os
from ave.display.curses_screen import CursesScreen

winskip = pytest.mark.skipif(
    os.name == "nt", reason="CircleCI cannot run this test on windows")


@winskip
def make_screen():
    try:
        return CursesScreen()
    except:  # noqa: E722
        return CursesScreen(False)


@winskip
def close_screen(s):
    try:
        s.close()
    except:  # noqa: E722
        s.close(False)


@winskip
def test_start_and_close():
    s = make_screen()
    close_screen(s)


@winskip
def test_clear():
    s = make_screen()
    s.clear()
    close_screen(s)


@winskip
@pytest.mark.parametrize('file', ["credits", "title", "user"])
def test_print_file(file):
    s = make_screen()
    s.print_file(file)
    s.close(False)


@winskip
@pytest.mark.parametrize('inventory', [
    [], ["hat", "shoes"], ["a" * 100], ["a"] * 100])
def test_show_inventory(inventory):
    s = make_screen()
    s.show_inventory([])
    s.show_inventory(["hat", "shoes"])
    s.show_inventory(["hat"] * 100)
    close_screen(s)
