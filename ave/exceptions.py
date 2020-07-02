from urllib.error import HTTPError as AVENoInternet  # noqa: F401


class AVEQuit(BaseException):
    pass


class AVEAgain(BaseException):
    pass


class AVEToMenu(BaseException):
    pass


class AVEGameOver(BaseException):
    pass


class AVEWinner(BaseException):
    pass
