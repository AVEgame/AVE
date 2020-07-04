"""Check that games are valid."""
from .error_handlers import (
    AVEFatalError, AVEError, AVEWarning, AVEInfo, AVENote)
from ..game import Character


def check_game(game):
    """Check a game for errors."""
    errors = []
    errors += check_first_room(game)
    errors += get_inaccessible_rooms(game)
    errors += get_undefined_rooms(game)
    errors += get_trapped_rooms(game)
    errors += get_undefined_numbers(game)
    errors += explore_items(game)
    return errors


def check_first_room(game):
    """Check that the first room of the game works."""
    errors = []
    if "start" not in game.rooms:
        return [AVEFatalError("There is no 'start' room.")]
    if len(game.rooms["start"].options) == 0:
        errors.append(AVEFatalError("You cannot leave the first room."))
    c = Character()
    c.reset(game.items)
    try:
        game["start"].get_text(c)
    except:  # noqa: F722
        errors.append(AVEFatalError("Could not load text for first room."))
    try:
        game["start"].get_options(c)
    except:  # noqa: F722
        errors.append(AVEFatalError("Could not load options for first room."))
    return errors


def get_inaccessible_rooms(game):
    """Find room that cannot be reached."""
    ach = {"start"}
    for room in game.rooms.values():
        for option in room.options:
            for d in option.get_all_destinations():
                ach.add(d)
    return [AVEWarning("The room '" + i + "' is not accessible.")
            for i in game.rooms if i not in ach]


def get_undefined_rooms(game):
    """Get rooms that can be reached but are not defined."""
    not_inc = set()
    for room in game.rooms.values():
        for option in room.options:
            for d in option.get_all_destinations():
                if d == "__GAMEOVER__" or d == "__WINNER__":
                    continue
                if d not in game.rooms:
                    not_inc.add(d)
    return [AVEError("The room '" + i + "' does not exist.")
            for i in not_inc]


def get_trapped_rooms(game):
    """Get rooms that there is no option to leave."""
    return [AVEError("There is no way to leave the room '" + id + "'.")
            for id, room in game.rooms.items() if len(room.options) == 0]


def get_undefined_numbers(game):
    """Get numbers that can be added to but are not defined."""
    not_def = set()
    c = Character()
    c.reset(game.items)
    for room in game.rooms.values():
        for thing in room.options + room.text:
            for item in thing.items:
                if not c.is_number(item.item) and item.value.get_value(c) != 1:
                    not_def.add(item.item)
    return [AVEWarning("The game wants to add a number to '" + i + "',"
                       " but it is not a variable.") for i in not_def]


def explore_items(game):
    """Look for items that are required but never added and other issues."""
    used = set()
    asked_for = set()
    c = Character()
    c.reset(game.items)
    for room in game.rooms.values():
        for thing in room.options + room.text:
            for item in thing.items:
                used.add(item.item)
            for item in thing.needs.get_all():
                asked_for.add(item)

    used_num = set()
    numbers = set()
    named_items = set()
    for i in game.items:
        if c.is_number(i):
            numbers.add(i)
            if i.default.get_value(c) != 0:
                used_num.add(i)
        else:
            named_items.add(i)

    errors = []
    errors += [AVEWarning("A line in your file requires '" + i + "',"
                          " but this item is never added.")
               for i in asked_for - used - used_num]
    errors += [AVEWarning("A line in your file asks about '" + i + "',"
                          " but this number is never changed.")
               for i in (asked_for - used).intersection(numbers)]
    errors += [AVEInfo("The number '" + i + "' is defined but is not "
                       "used in the game.")
               for i in numbers - used - asked_for]
    errors += [AVEInfo("The item '" + i + "' is named but is not "
                       "used in the game.")
               for i in named_items - used - asked_for]
    errors += [AVENote("The item '" + i + "' is not named, so will be hidden "
                       "from the inventory by default.")
               for i in used.union(asked_for) - named_items - numbers]
    return errors


# Info: unnamed items will default to hidden
