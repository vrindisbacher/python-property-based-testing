from unittest import TestCase
from pybt.core.core import pybt


class TestRevSimple(TestCase):
    pybt_small = pybt(max_complex_arg_size=5, max_basic_arg_size=1000)

    def rev(self, l):
        return l[::-1]

    @pybt_small
    def rev_test(self, l: list):
        assert self.rev(self.rev(l)) == l

    @pybt_small
    def rev_test_types(self, l: list[any]):
        assert self.rev(self.rev(l)) == l

    @pybt_small
    def rev_test_wrong(self, l: list[dict[any, any]]):
        assert self.rev(self.rev(l)) == l

    @pybt_small
    def rev_rest_no_pipe(self, l: list[dict[any]]):
        assert self.rev(self.rev(l)) == l
