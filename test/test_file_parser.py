import pytest
from ave.parsing import file_parsing as fp
from ave import Character


def test_requirement_parsing():
    c1 = Character()
    c2 = Character(inventory=["hat"])
    c3 = Character(inventory=["shoes"], numbers={"n": 4})

    r = fp._parse_rq("hat")
    assert not r.has(c1)
    assert r.has(c2)
    assert not r.has(c3)

    # This would be "(hat shoes)" but the parser enters the comma
    # before passing into this function.
    r = fp._parse_rq("(hat,shoes)")
    assert not r.has(c1)
    assert r.has(c2)
    assert r.has(c3)

    r = fp._parse_rq("(!hat,shoes)")
    assert r.has(c1)
    assert not r.has(c2)
    assert r.has(c3)

    r = fp._parse_rq("n")
    assert not r.has(c1)
    assert not r.has(c2)
    assert r.has(c3)

    r = fp._parse_rq("n==4")
    try:
        r.has(c1)
        assert False
    except KeyError:
        pass
    assert r.has(c3)

    r = fp._parse_rq("n>5")
    assert not r.has(c3)


@pytest.mark.parametrize(
    'txt,value', [
        ("0+1", 1),
        ("n+1", 5),
        ("n*p", 20),
        ("n*p+2*p+6", 36),
        ("n+1*p", 9),
        ("n+(1*p)", 9),
        ("n+(1)*(p)", 9),
        ("(n+1)*p", 25),
        ("(((n)+1)*p)", 25)])
def test_number_parsing(txt, value):
    c = Character(numbers={"n": 4, "p": 5})
    assert fp._parse_value(txt).get_value(c) == value


def test_random_number_parsing():
    c = Character(numbers={"n": 4, "p": 5})

    r = fp._parse_value("__R__+6")
    value = [r.get_value(c) for i in range(10)]
    assert 6 <= min(value) < max(value) <= 7

    r = fp._parse_value("__R__(4,6)+6")
    value = [r.get_value(c) for i in range(10)]
    assert 10 <= min(value) < max(value) <= 12


def test_item_giver_parsing():
    c = Character(numbers={"n": 0, "p": 1})

    assert not c.has("hat")
    fp._parse_ig_add("hat").give(c)
    assert c.has("hat")

    assert c.has("hat")
    fp._parse_ig_remove("hat").give(c)
    assert not c.has("hat")

    assert c.numbers["n"] == 0
    fp._parse_ig_add("n").give(c)
    assert c.numbers["n"] == 1
    fp._parse_ig_add("n+3").give(c)
    assert c.numbers["n"] == 4

    assert c.numbers["p"] == 1
    fp._parse_ig_add("n+p").give(c)
    assert c.numbers["p"] == 1
    assert c.numbers["n"] == 5
    fp._parse_ig_add("p-n").give(c)
    assert c.numbers["p"] == -4
    assert c.numbers["n"] == 5
    fp._parse_ig_add("p=5+6").give(c)
    assert c.numbers["p"] == 11


def test_requirement_line_parsing():
    c = Character(inventory=["hat"], numbers={"n": 2, "p": 0})

    items, needs = fp.parse_requirements("? hat + n")
    assert needs.has(c)
    items[0].give(c)
    assert c.numbers["n"] == 3

    items, needs = fp.parse_requirements("? hat ?! shoes ? (n=2 p=1)")
    assert not needs.has(c)
    items, needs = fp.parse_requirements("? hat ?! shoes ? (n=2 p=0)")
    assert needs.has(c)


def test_parse_line():
    c = Character(inventory=["hat"])

    text, items, needs = fp.parse_line("This is the text. ? hat ~ hat")
    assert text == "This is the text."
    assert needs.has(c)
    items[0].give(c)
    assert not needs.has(c)


def test_parse_option():
    c = Character()

    o = fp.parse_option("Go here => room ?! hat + shoes")
    assert o.get_destination() == "room"
    assert len(o.get_all_destinations()) == 1
    assert not c.has("shoes")
    o.get_items(c)
    assert c.has("shoes")

    o = fp.parse_option("Go here => __R__(room,garden,__GAMEOVER__)")
    assert len(o.get_all_destinations()) == 3
    for room in ["room", "garden", "__GAMEOVER__"]:
        for i in range(100):
            if o.get_destination() == room:
                break
        else:
            assert False
