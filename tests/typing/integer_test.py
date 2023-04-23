from unittest import TestCase

from pybt.typing.basic_types import Int
from pybt.core import pybt


class TestStr(TestCase):
    @pybt
    def test_no_args(self, i: Int):
        assert i <= 1000 and i >= -1000
        assert type(i) == int

    @pybt
    def test_min_arg_only(self, i: Int[0]):
        assert i <= 1000 and i >= 0
        assert type(i) == int

    @pybt
    def test_min_and_max_arg(self, i: Int[0, 10]):
        assert i <= 10 and i >= 0
        assert type(i) == int

    @pybt
    def test_string_type(self):
        try:

            def _test(h: Int["hello"]):
                print(h)

            _test()
            self.fail("String are not a valid int. This should fail.")
        except TypeError:
            pass
