"""Error handlers."""


class AVEErrorHandler:
    """Class to store errors found when checking games."""

    def __init__(self, description, error_type, error_value):
        """Make the error handler."""
        self.description = description
        self.error_type = error_type
        self.error_value = error_value

    def __str__(self):
        """Return a string describing the error."""
        return self.error_type + ": " + self.description


class AVEFatalError(AVEErrorHandler):
    """This error is so bad that the game will not run."""

    def __init__(self, description):
        """Make the error handler."""
        super().__init__(description, "Fatal Error", 5)


class AVEError(AVEErrorHandler):
    """There is an error but part of the game will still run."""

    def __init__(self, description):
        """Make the error handler."""
        super().__init__(description, "Error", 4)


class AVEWarning(AVEErrorHandler):
    """The game will run, but there may is a small problem."""

    def __init__(self, description):
        """Make the error handler."""
        super().__init__(description, "Warning", 3)


class AVEInfo(AVEErrorHandler):
    """The game will run, but there maybe is a small problem."""

    def __init__(self, description):
        """Make the error handler."""
        super().__init__(description, "Info", 2)


class AVENote(AVEErrorHandler):
    """The game will run, but there maybe is a tiny problem."""

    def __init__(self, description):
        """Make the error handler."""
        super().__init__(description, "Note", 1)
