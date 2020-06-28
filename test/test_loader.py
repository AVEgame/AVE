import pytest
import re
from ave.game_loader import escape, unescape


@pytest.mark.parametrize('string', [
    "",
    "This is an option => gohere ? hat",
    "This option has an escape <| => |> gohere ?! hat",
    "A<|???|> B C <|D=>E|>"
])
def test_unescape_escape_string(string):
    assert unescape(escape(string)) == re.sub(r"<\|(.*)\|>", r"\1", string)


def test_escape_string():
    assert "=>" not in escape("test <|=>|> escaping")
    assert "=>" in escape("test => escaping")
