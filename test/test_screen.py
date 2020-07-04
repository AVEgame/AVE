import pytest
from ave.display.curses_screen import CursesScreen


def test_start_and_close():
    s = CursesScreen()
    s.close()


def test_clear():
    s = CursesScreen()
    s.clear()
    s.close()


@pytest.mark.parametrize('file', ["credits", "title", "user"])
def test_print_file(file):
    s = CursesScreen()
    s.print_file(file)
    s.close()


@pytest.mark.parametrize('inventory', [
    [], ["hat", "shoes"], ["a" * 100], ["a"] * 100])
def test_show_inventory(inventory):
    s = CursesScreen()
    s.show_inventory([])
    s.show_inventory(["hat", "shoes"])
    s.show_inventory(["hat"] * 100)
    s.close()
