import os
from ave import config, load_game_from_file, Character
from ave.exceptions import AVEGameOver, AVEWinner
from random import choice


def test_website_move():
    numbers = {}
    inventory = []
    current_room = "test2"
    option_key = choice([0, 1, 2])
    game = load_game_from_file(os.path.join(config.root_folder,
                                            "test/games/test2.ave"))
    game.load()

    character = Character(numbers=numbers, inventory=inventory,
                          location=current_room)
    game.pick_option(option_key, character)
    try:
        rtype, text, options = game.get_room_info(character, game.currency)
    except AVEGameOver:
        return {"room": "__GAMEOVER__"}
    except AVEWinner:
        return {"room": "__WINNER__"}
    options_list = []
    for k, v in options.items():
        options_list.append((k, v))
    options_list = sorted(options_list, key=lambda x: x[0])
    inventory_text = character.get_inventory(game.items, game.currency)

    assert text == str(option_key) + " lead here"
    print(options_list)
    assert options_list[0][1] == "Continue"
    assert len(inventory_text) == 0
