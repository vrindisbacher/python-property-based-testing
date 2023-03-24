from pybt.core.core import pybt
from unittest import TestCase


base_decorator = pybt(max_basic_arg_size=1000, max_complex_arg_size=10)


def factorial(x: str):
    fac = 1
    for i in range(1, x + 1):
        fac = fac * i
    return fac


@base_decorator
def test_factorial(x: int):
    a = factorial(x)
    pred = factorial(x - 1)
    assert a == x * pred


@base_decorator
def test_factorial_coerce(x: str):
    test_case = TestCase()
    with test_case.assertRaises(Exception) as context:
        factorial(x)

    assert context.exception is not None


def rev(l):
    return l[::-1]


@base_decorator
def test_rev(l: list[list[str]]):
    assert rev(rev(l)) == l


# test_factorial()
# test_factorial_coerce()
test_rev()
# test_dict_func()
