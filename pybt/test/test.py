from pybt.core.core import pybt


def factorial(x : str):
    fac = 1
    for i in range(1, x + 1):
        fac = fac * i
    return fac


@pybt(hypotheses={"x": lambda x: 1 <= x <= 100})
def test_factorial(x: int):
    a = factorial(x)
    pred = factorial(x - 1)
    assert a == x * pred


def rev(l):
    return l[::-1]

@pybt(hypotheses={"l": lambda l : len(l) <= 10 })
def test_rev(l : list[str | int | bool]):
    assert(rev(rev(l)) == l)


# test_factorial()
# test_complex()
test_rev()