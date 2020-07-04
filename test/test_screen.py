import pytest
from ave.display.curses_screen import CursesScreen


def make_screen():
    try:
        return CursesScreen()
    except:  # noqa: E722
        return CursesScreen(False)


def close_screen(s):
    try:
        s.close()
    except:  # noqa: E722
        s.close(False)


def test_start_and_close():
    s = make_screen()
    close_screen(s)


def test_clear():
    s = make_screen()
    s.clear()
    close_screen(s)


@pytest.mark.parametrize('file', ["credits", "title", "user"])
def test_print_file(file):
    s = make_screen()
    s.print_file(file)
    s.close(False)


@pytest.mark.parametrize('inventory', [
    [], ["hat", "shoes"], ["a" * 100], ["a"] * 100])
def test_show_inventory(inventory):
    s = make_screen()
    s.show_inventory([])
    s.show_inventory(["hat", "shoes"])
    s.show_inventory(["hat"] * 100)
    close_screen(s)
