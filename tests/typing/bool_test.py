from unittest import TestCase

from pybt.typing.basic_types import Bool
from pybt.core import pybt


class TestBool(TestCase):
    @pybt
    def test_no_args(self, b: Bool):
        assert type(b) == bool

    @pybt
    def test_arged_bool(self):
        try:

            def _test(h: Bool["hello"]):
                print(h)

            _test()
            self.fail("Bools don't have params. This should fail")
        except TypeError:
            pass
