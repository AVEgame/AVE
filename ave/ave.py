"""The AVE and GameLibrary classes that run AVE in a terminal."""

import os
import json

from . import config
from .exceptions import (AVEGameOver, AVEWinner, AVEToMenu, AVEQuit,
                         AVENoInternet)
from .game import Game
from .parsing.game_loader import (
    load_game_from_file, load_library_json, load_game_from_library)


class AVE:
    """The AVE class that runs the Character, Screen and Game."""

    def __init__(self, screen=None, character=None):
        """Create an AVE class.

        Parameters
        ----------
        screen : ave.display.base.Screen
            The screen that will display the game
        character : ave.game.Character
            The character playing the game
        """
        self.screen = screen
        self.character = character
        self.games = None
        self.items = None
        self._unsorted_games = []

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
        game_to_load = self.screen.title_menu(
            self.games.titles() + ["- user contributed games -"])
        if game_to_load == len(self.games.titles()):
            self.show_download_menu()
        else:
            the_game = self.games[game_to_load]
            self.run_the_game(the_game)

    def sort_games(self):
        """Remove disabled games and sort the games by number."""
        ordered_games = {}
        other_games = []
        for g in self._unsorted_games:
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

    def load_games(self, folder, prefix=""):
        """Load the metadata of games from a folder.

        Parameters
        ----------
        folder: str
            The folder
        """
        for game in os.listdir(folder):
            if game[-4:] == ".ave":
                g = load_game_from_file(os.path.join(folder, game),
                                        game)
                g.title = prefix + g.title
                self.add_game(g)
        self.sort_games()

    def add_game(self, game):
        """Add a game to the (unsorted) game list."""
        if game.file is not None:
            for g in self._unsorted_games:
                if g.file == game.file:
                    return
        if game.url is not None:
            for g in self._unsorted_games:
                if g.url == game.url:
                    return
        self._unsorted_games.append(game)

    def load_games_from_json(self, json_file):
        """Load the metadata of games from a json.

        Parameters
        ----------
        json_file: str
            The location of the json file
        """
        with open(json_file) as f:
            gamelist = json.load(f)
        for game in gamelist:
            self.add_game(Game(
                file=os.path.join(config.games_folder, game["filename"]),
                title=game["title"], number=game["number"],
                description=game["desc"],
                author=game["author"], active=game["active"],
                version=game["version"], filename=game["filename"],
                ave_version=game["ave_version"]))
        self.sort_games()

    def get_download_menu(self):
        """Get the list of games from the online library.

        Returns
        -------
        list
            A list of the title, author and local url for each game.
        """
        try:
            library = load_library_json()
        except AVENoInternet:
            self.no_internet()
            raise AVEToMenu
        return [(game["title"], game["author"], i)
                for i, game in enumerate(library)]

    def show_download_menu(self):
        """Show a menu of games from the online library."""
        try:
            self.screen.print_download()
            menu_items = self.get_download_menu()
            game_n = self.screen.download_menu(
                [a[0] + ' by ' + a[1] for a in menu_items])
            the_game = load_game_from_library(menu_items[game_n][2])
            self.run_the_game(the_game)
        except AVEToMenu:
            self.show_title_screen()

    def no_internet(self):
        """Show a "you have no internet" notification."""
        self.screen.no_internet()
        self.screen.wait_for_input()

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
            next_id = self.screen.menu(list(options.values()))
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
