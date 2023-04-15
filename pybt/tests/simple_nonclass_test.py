from pybt.core.core import pybt
from unittest import TestCase


def rev(l):
    return l[::-1]


class TestRevSimple(TestCase):
    pybt_small = pybt(max_complex_arg_size=5, max_basic_arg_size=1000)

    @pybt_small
    def test_rev(self, l: list):
        assert rev(rev(l)) == l

    @pybt_small
    def test_rev_any(self, l: list[any]):
        assert rev(rev(l)) == l

    @pybt_small
    def test_rev_dict(self, l: list[dict]):
        assert rev(rev(l)) == l

    @pybt_small
    def test_rev_dict_no_key(self, l: list[dict[str, any]]):
        assert rev(rev(l)) == l
