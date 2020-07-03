import pytest
import re
import ave
from ave import string_functions as sf


@pytest.mark.parametrize('txt', [
    "",
    "This is an option => gohere ? hat",
    "This option has an escape <| => |> gohere ?! hat",
    "A<|???|> B C <|D=>E|>"
])
def test_unescape_escape_string(txt):
    assert sf.unescape(sf.escape(txt)) == re.sub(r"<\|(.*?)\|>", r"\1", txt)


def test_escape_string():
    assert "=>" not in sf.escape("test <|=>|> escaping")
    assert "=>" in sf.escape("test => escaping")
    assert "=>" in sf.escape("test <|a|> => <|???|>escaping")


def test_between():
    assert sf.between("abcde(fgh)", "(", ")") == "fgh"
    assert sf.between("abcde(fgh)ijk(lmn)", "(", ")") == "fgh"


def test_replacements():
    assert sf._replacements("ab %v%") == "ab " + ave.__version__


def test_more_unescape():
    assert sf.unescape(sf.escape("$var$")) == "$var$"
    assert sf.unescape(sf.escape("<|$var$|>")) != "$var$"
    assert sf.more_unescape(sf.escape("<|$var$|>")) == "$var$"
