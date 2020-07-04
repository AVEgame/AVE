"""Exceptions used by AVE."""

class AVEQuit(BaseException):
    """Quit AVE."""


class AVEAgain(BaseException):
    """Play the same game again."""


class AVEToMenu(BaseException):
    """Leave to the main menu."""


class AVEGameOver(BaseException):
    """Game over."""


class AVEWinner(BaseException):
    """You win."""


class AVEVersionError(BaseException):
    """Your version of AVE cannot play this game."""


class AVENoInternet(BaseException):
    """AVE could not load an online resource."""
