from unittest import TestCase

from pybt.typing.basic_types import Float
from pybt.core import pybt


class TestFloat(TestCase):
    @pybt
    def test_no_args(self, f: Float):
        assert f <= 1000 and f >= -1000
        assert type(f) == float

    @pybt
    def test_min_arg_only(self, f: Float[0]):
        assert f <= 1000 and f >= 0
        assert type(f) == float

    @pybt
    def test_min_and_max_arg(self, f: Float[0, 10]):
        assert f <= 10 and f >= 0
        assert type(f) == float

    @pybt
    def test_string_type(self):
        try:

            def _test(f: Float["hello"]):
                print(f)

            _test()
            self.fail("String are not a valid int. This should fail.")
        except TypeError:
            pass
