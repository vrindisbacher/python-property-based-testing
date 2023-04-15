from pybt.core.core import pybt
from unittest import TestCase


def rev(l):
    return l[::-1]


class TestRevSimple(TestCase):
    pybt_small = pybt(max_complex_arg_size=5, max_basic_arg_size=1000)

    @staticmethod
    @pybt_small
    def rev_test(l: list):
        assert rev(rev(l)) == l

    @staticmethod
    @pybt_small
    def rev_test_types(l: list[any]):
        assert rev(rev(l)) == l

    @staticmethod
    @pybt_small
    def rev_test_wrong(l: list[dict[any, any]]):
        assert rev(rev(l)) == l

    @staticmethod
    @pybt_small
    def rev_rest_no_pipe(l: list[dict[any]]):
        assert rev(rev(l)) == l
