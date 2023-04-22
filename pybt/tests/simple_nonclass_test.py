from pybt.core import pybt
from unittest import TestCase


def rev(l):
    return l[::-1]


class TestRevSimple(TestCase):

    @pybt
    def test_rev(self, l: list):
        assert rev(rev(l)) == l

    @pybt
    def test_rev_any(self, l: list[any]):
        assert rev(rev(l)) == l

    @pybt
    def test_rev_dict(self, l: list[dict]):
        assert rev(rev(l)) == l

    @pybt
    def test_rev_dict_no_key(self, l: list[dict[str, any]]):
        assert rev(rev(l)) == l
