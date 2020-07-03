from math import isclose
from ave import numbers as no
from ave import item_giver as ig
from ave import requirements as rq
from ave import Character


def test_constant():
    c = Character()
    assert no.Constant(4).get_value(c) == 4


def test_sum():
    c = Character()
    n = no.Sum(no.Constant(1.5), no.Constant(2.5))
    assert isclose(n.get_value(c), 4)

    n = no.Sum(no.Constant(2), no.Constant(1), no.Constant(3))
    assert n.get_value(c) == 6


def test_product():
    c = Character()
    n = no.Product(no.Constant(2), no.Constant(5))
    assert n.get_value(c) == 10

    n = no.Product(no.Constant(2), no.Constant(5), no.Constant(2))
    assert n.get_value(c) == 20


def test_division():
    c = Character()
    n = no.Division(no.Constant(1), no.Constant(2))
    assert isclose(n.get_value(c), 0.5)


def text_negative():
    c = Character()
    assert no.Negative(no.Constant(2)).get_value(c) == -2


def test_variable():
    c = Character(numbers={"n": 4, "p": 5})
    assert no.Variable("n").get_value(c) == 4

    ig.Add("n", no.Constant(3)).give(c)
    assert no.Variable("n").get_value(c) == 7

    ig.Add("n", no.Variable("p")).give(c)
    assert no.Variable("n").get_value(c) == 12


def test_random():
    c = Character()

    r = no.Random()
    values = [r.get_value(c) for i in range(10)]
    assert 0 <= min(values) < max(values) <= 1

    r = no.Random(no.Constant(5))
    values = [r.get_value(c) for i in range(10)]
    assert 0 <= min(values) < max(values) <= 5

    r = no.Random(no.Constant(3), no.Constant(5))
    values = [r.get_value(c) for i in range(10)]
    assert 3 <= min(values) < max(values) <= 5


def test_items():
    c = Character()
    assert not c.has("hat")
    assert not rq.RequiredItem("hat").has(c)

    ig.Add("hat").give(c)
    assert c.has("hat")
    assert rq.RequiredItem("hat").has(c)
    assert not rq.RequiredItem("shoes").has(c)
    assert rq.Or(rq.RequiredItem("hat"),
                 rq.RequiredItem("shoes")).has(c)
    assert not rq.And(rq.RequiredItem("hat"),
                      rq.RequiredItem("shoes")).has(c)
    assert rq.Not(rq.RequiredItem("shoes")).has(c)

    ig.Add("hat").give(c)
    assert c.has("hat")

    ig.Remove("hat").give(c)
    assert not c.has("hat")

    ig.Remove("hat").give(c)
    assert not c.has("hat")


def test_numbers():
    c = Character(numbers={"n": 4})
    assert c.numbers["n"] == 4
    assert rq.RequiredNumber(no.Variable("n"), "=", no.Constant(4)).has(c)
    assert rq.RequiredNumber(no.Variable("n"), ">", no.Constant(3)).has(c)
    assert rq.RequiredNumber(no.Variable("n"), ">=", no.Constant(3)).has(c)
    assert rq.RequiredNumber(no.Variable("n"), ">=", no.Constant(4)).has(c)

    ig.Add("n").give(c)
    assert c.numbers["n"] == 5

    ig.Add("n", no.Constant(3)).give(c)
    assert c.numbers["n"] == 8

    ig.Remove("n").give(c)
    assert c.numbers["n"] == 7

    ig.Remove("n", no.Constant(2)).give(c)
    assert c.numbers["n"] == 5

    ig.Set("n", no.Constant(-1.5)).give(c)
    assert isclose(-1.5, c.numbers["n"])


def test_satisfied():
    c = Character()
    assert rq.Satisfied().has(c)
    assert not rq.Not(rq.Satisfied()).has(c)
