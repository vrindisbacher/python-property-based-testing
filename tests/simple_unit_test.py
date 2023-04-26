from unittest import TestCase
from pybt.core import pybt
from pybt.typing.type_declarations import List, Dict, Any, Str


class TestRevSimple(TestCase):
    def rev(self, l):
        return l[::-1]

    @pybt
    def test_rev(self, l: List):
        assert self.rev(self.rev(l)) == l

    @pybt
    def test_rev_any(self, l: List[Any]):
        assert self.rev(self.rev(l)) == l

    @pybt
    def test_rev_dict(self, l: List[Dict]):
        assert self.rev(self.rev(l)) == l

    @pybt
    def test_rev_dict_no_key(self, l: List[Dict[Str, Any]]):
        assert self.rev(self.rev(l)) == l
