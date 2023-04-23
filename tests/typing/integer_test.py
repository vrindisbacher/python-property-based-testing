from unittest import TestCase

from pybt.typing.basic_types import Int
from pybt.core import pybt


class TestStr(TestCase):
    @pybt
    def test_no_args(self):
        i = Int
        gen = i.generate(i)
        assert gen <= 1000 and gen >= -1000
        assert type(gen) == int

    @pybt
    def test_min_arg_only(self):
        i = Int[0]
        gen = i.generate(i)
        assert gen <= 1000 and gen >= 0
        assert type(gen) == int

    @pybt
    def test_min_and_max_arg(self):
        i = Int[0, 10]
        gen = i.generate(i)
        assert gen <= 10 and gen >= 0
        assert type(gen) == int

    @pybt
    def test_string_type(self):
        try:
            _ = Int["hello"]
            self.fail("String are not a valid int. This should fail.")
        except TypeError:
            pass
