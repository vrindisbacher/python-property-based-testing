from pybt.core.core import pybt
from unittest import TestCase


def factorial(x: str):
    fac = 1
    for i in range(1, x + 1):
        fac = fac * i
    return fac


@pybt(hypotheses={"x": lambda x: 1 <= x <= 100})
def test_factorial(x: int):
    a = factorial(x)
    pred = factorial(x - 1)
    assert a == x * pred


@pybt
def test_factorial_coerce(x: str):
    test_case = TestCase()
    with test_case.assertRaises(Exception) as context:
        factorial(x)

    assert context.exception is not None


def rev(l):
    return l[::-1]


@pybt(hypotheses={"l": lambda l: len(l) <= 10})
def test_rev(l: list[str | int | bool | list[bool | str | list[str]  | list[dict[str, list[dict[str,str]]]]]]):
    assert rev(rev(l)) == l



# test_factorial()
# test_factorial_coerce()
test_rev()
# test_dict_func()