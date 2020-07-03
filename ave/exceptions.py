"""Exceptions used by AVE."""

from urllib.error import HTTPError as AVENoInternet  # noqa: F401


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
