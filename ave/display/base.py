"""Base class for displaying the game."""


class Screen:
    """The base Screen class."""

    def print_titles(self):
        """Print the AVE title page."""
        self.print_file("title")

    def print_download(self):
        """Print the game library page."""
        self.print_file("user")

    def print_credits(self):
        """Print the credits page."""
        self.print_file("credits")

    def no_internet(self):
        """Display a "You have no internet" message."""
        raise NotImplementedError()

    def clear(self):
        """Clear the screen."""
        raise NotImplementedError()

    def close(self):
        """Close the screen."""
        raise NotImplementedError()

    def put_ave_logo(self):
        """Print the AVE logo at the top of the screen."""
        raise NotImplementedError()

    def print_file(self, filename):
        """Print the contents of a text file."""

    def gameover(self):
        """Show the game over screen."""
        return self.gameend("GAME OVER")

    def winner(self):
        """Show the "you win" screen."""
        return self.gameend("YOU WIN!")

    def gameend(self, text):
        """Allow the user to play again or go back to the menu."""
        raise NotImplementedError()

    def show_inventory(self, inventory):
        """Display the inventory."""
        raise NotImplementedError()

    def type_room_text(self, text):
        """Type the room text."""
        raise NotImplementedError()

    def title_menu(self, ls, selected=0):
        """Let the user pick a built in game or go to download menu."""
        raise NotImplementedError()

    def download_menu(self, ls, selected=0):
        """Let the user pick a game from the online library."""
        raise NotImplementedError()

    def gameover_menu(self, ls, selected=0):
        """Give the user some options for what to do after game ends."""
        raise NotImplementedError()

    def menu(self, ls, selected=0):
        """Give the user some options for what to do next."""
        raise NotImplementedError()

    def wait_for_input(self, keys=['q']):
        """Wait for the user to press a key."""
        raise NotImplementedError()

    def show_titles(self, title, description, author, version):
        """Show the title screen for a game."""
        raise NotImplementedError()
