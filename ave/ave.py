"""The AVE and GameLibrary classes that run AVE in a terminal."""

import os
from .exceptions import (AVEGameOver, AVEWinner, AVEToMenu, AVEQuit,
                         AVENoInternet)
from .game import Character
from . import config


class AVE:
    """The AVE class that runs the Character, Screen and Game."""

    def __init__(self, screen=None):
        """Create an AVE class.

        Parameters
        ----------
        start_screen : bool
            Should the Screen be started?
        """
        self.screen = screen
        self.character = Character()
        self.games = None
        self.items = None

    def start(self):
        """Start running the main AVE loop."""
        if config.debug:
            self._debug_start()
        else:
            self._actual_start()

    def _debug_start(self):
        """Start AVE in debug mode.

        In debug mode, exceptions will be diaplayed on exit.
        """
        try:
            self.show_title_screen()
        except AVEQuit:
            self.exit()
            print("Goodbye...")
        finally:
            self.exit()

    def _actual_start(self):
        """Start AVE in standard mode."""
        while True:
            try:
                self.show_title_screen()
            except AVEQuit:
                self.exit()
                print("Goodbye...")
                break
            except:  # noqa: E722
                self.exit()
                break

    def show_title_screen(self):
        """Display the AVE title screen."""
        self.screen.print_titles()
        game_to_load = self.screen.menu(
            self.games.titles() + ["- user contributed games -"], 8,
            credits=True)
        if game_to_load == len(self.games.titles()):
            self.show_download_menu()
        else:
            the_game = self.games[game_to_load]
            self.run_the_game(the_game)

    def load_games(self, folder):
        """Load the metadata of games from a folder.

        Parameters
        ----------
        folder: str
            The folder
        """
        from .game_loader import load_game_from_file
        ordered_games = {}
        other_games = []
        for game in os.listdir(folder):
            if game[-4:] == ".ave":
                g = load_game_from_file(os.path.join(folder, game))
                g.filename = game
                if config.version_tuple < g.ave_version:
                    continue
                if g.active or config.debug:
                    if g.number is None:
                        other_games.append(g)
                    else:
                        assert g.number not in ordered_games
                        ordered_games[g.number] = g
        self.games = GameLibrary([
            ordered_games[i]
            for i in sorted(ordered_games.keys())] + other_games)

    def get_download_menu(self):
        """Get the list of games from the online library.

        Returns
        -------
        list
            A list of the title, author and local url for each game.
        """
        from .game_loader import load_library_json
        try:
            the_json = load_library_json()
        except AVENoInternet:
            self.no_internet()
            raise AVEToMenu
        menu_items = []
        for key, value in the_json.items():
            if 'user/' in key:
                menu_items.append([value['title'], value['author'],
                                   key])
        return menu_items

    def show_download_menu(self):
        """Show a menu of games from the online library."""
        from .game_loader import load_game_from_library

        try:
            self.screen.print_download()
            menu_items = self.get_download_menu()
            game_n = self.screen.menu(
                [a[0] + ' by ' + a[1] for a in menu_items], 12)
            the_game = load_game_from_library(menu_items[game_n][2])
            self.run_the_game(the_game)
        except AVEToMenu:
            self.show_title_screen()

    def no_internet(self):
        """Show a "you have no internet" notification."""
        self.screen.no_internet()
        self.screen.menu([], 1)

    def run_the_game(self, the_game):
        """Run a game.

        Parameters
        ----------
        the_game : ave.game.Game
            The game
        """
        the_game.load()
        again = True
        while again:
            again = False
            try:
                self.character.reset(the_game.items)
                self.screen.show_titles(
                    the_game.title,
                    the_game.description,
                    the_game.author,
                    the_game.version)
                self.game_loop(the_game)
            except AVEGameOver:
                next = self.screen.gameover()
                if next == 0:
                    again = True
                if next == 2:
                    raise AVEQuit
            except AVEWinner:
                next = self.screen.winner()
                if next == 0:
                    again = True
                if next == 2:
                    raise AVEQuit
            except AVEToMenu:
                pass

    def game_loop(self, the_game):
        """Run the game in a loop so it can be re-played.

        Parameters
        ----------
        the_game : ave.game.Game
            The game
        """
        while True:
            text, options = the_game.get_room_info(self.character)
            self.screen.clear()
            self.screen.put_ave_logo()
            self.screen.show_inventory(
                self.character.get_inventory(the_game.items))
            self.screen.type_room_text(text)
            next_id = self.screen.menu(
                list(options.values()),
                y=min(8, len(options)))
            the_game.pick_option(
                list(options.keys())[next_id],
                self.character)

    def exit(self):
        """Exit AVE."""
        self.screen.close()


class GameLibrary:
    """The GameLibrary class that stores the list of available games."""

    def __init__(self, games):
        """Make a GameLibrary.

        Parameters
        ----------
        games : list
            A list of games.
        """
        self.games = games

    def titles(self):
        """Get the title of each game.

        Returns
        -------
        list
            The title of each game
        """
        return [g.title for g in self.games]

    def descriptions(self):
        """Get the description of each game.

        Returns
        -------
        list
            The description of each game
        """
        return [g.description for g in self.games]

    def titles_and_descriptions(self):
        """Get the title and description of each game.

        Returns
        -------
        iterator
            The title and description of each game
        """
        return zip(self.titles(), self.descriptions())

    def game(self, n):
        """Get the nth game.

        Parameters
        ----------
        n : int
            n
        """
        return self.games[n]

    def __getitem__(self, n):
        """Get the nth game.

        Parameters
        ----------
        n : int
            n
        """
        return self.games[n]
