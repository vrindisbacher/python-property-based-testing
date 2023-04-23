from unittest import TestCase

from pybt.typing.basic_types import Str
from pybt.core import pybt


class TestStr(TestCase):

    def test_neg_arg(self):
        try:
            _ = Str[-1]

            self.fail("Negative max len is illegal. This should fail.")
        except TypeError:
            pass

    @pybt
    def test_no_args(self):
        _ = Str[100]
        s = Str 
        gen = s.generate(s)
        assert len(gen) <= 100 and len(gen) >= 0
        assert type(gen) == str