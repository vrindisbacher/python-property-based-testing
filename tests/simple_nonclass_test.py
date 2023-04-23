from pybt.core import pybt
from pybt.typing.complex_types import List, Dict, Any
from pybt.typing.basic_types import Str

from unittest import TestCase


def rev(l):
    return l[::-1]


class TestRevSimple(TestCase):
    @pybt
    def test_rev(self, l: List):
        assert rev(rev(l)) == l

    @pybt
    def test_rev_any(self, l: List[Any]):
        assert rev(rev(l)) == l

    @pybt
    def test_rev_dict(self, l: List[Dict]):
        assert rev(rev(l)) == l

    @pybt
    def test_rev_dict_no_key(self, l: List[Dict[Str, Any]]):
        assert rev(rev(l)) == l
