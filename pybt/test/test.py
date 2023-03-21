from pybt.core.core import pybt


def factorial(x):
    fac = 1
    for i in range(1, x + 1):
        fac = fac * i
    return fac


@pybt(hypotheses={"x": lambda x: 1 <= x <= 100})
def test_factorial(x: int):
    a = factorial(x)
    pred = factorial(x - 1)
    assert a == x * pred


test_factorial()
