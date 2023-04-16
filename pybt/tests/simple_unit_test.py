from unittest import TestCase
from pybt.core.core import pybt


class TestRevSimple(TestCase):
    pybt_small = pybt(max_complex_arg_size=5, max_basic_arg_size=1000)

    def rev(self, l):
        return l[::-1]

    @pybt_small
    def test_rev(self, l: list):
        assert self.rev(self.rev(l)) == l

    @pybt_small
    def test_rev_any(self, l: list[any]):
        assert self.rev(self.rev(l)) == l

    @pybt_small
    def test_rev_dict(self, l: list[dict]):
        assert self.rev(self.rev(l)) == l

    @pybt_small
    def test_rev_dict_no_key(self, l: list[dict[str, any]]):
        assert self.rev(self.rev(l)) == l
