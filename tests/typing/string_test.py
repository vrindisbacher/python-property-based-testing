from unittest import TestCase

from pybt.typing.basic_types import Str
from pybt.core import pybt


class TestStr(TestCase):
    def test_neg_arg(self):
        try:

            @pybt
            def _test(s: Str[-1]):
                print(s)

            _test()
            self.fail("Negative max len is illegal. This should fail.")
        except TypeError:
            pass

    @pybt
    def test_no_args(self, s: Str[100]):
        assert len(s) <= 100 and len(s) >= 0
        assert type(s) == str
