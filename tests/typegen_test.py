from unittest import TestCase
from pybt.core import pybt
from pybt.typing.basic_types import Bool, Float, Int, Str, NoneType
from pybt.typing.complex_types import List, Tuple, Dict


class TestTypeGen(TestCase):
    @pybt
    def test_simple_list(self, l: List):
        assert type(l) == list

    @pybt
    def test_simple_tuple(self, t: Tuple):
        assert type(t) == tuple

    @pybt
    def test_simple_dict(self, d: Dict):
        assert type(d) == dict

    @pybt
    def test_simple_int(self, i: Int):
        assert type(i) == int

    @pybt
    def test_simple_float(self, f: Float):
        assert type(f) == float

    @pybt
    def test_simple_bool(self, b: Bool):
        assert type(b) == bool

    @pybt
    def test_simple_string(self, s: Str):
        assert type(s) == str

    @pybt
    def test_simple_union(self, s: Int | Float | Str | Bool):
        valid = [int, float, str, bool]
        assert type(s) in valid

    @pybt
    def test_list_simple_union(self, l: List[Int | Float | Str | Bool]):
        valid = [int, float, str, bool]
        assert type(l) == list
        for el in l:
            assert type(el) in valid

    @pybt
    def test_dict_simple_union(
        self, d: Dict[Int | Float | Str | Bool, Int | Float | Str | Bool]
    ):
        valid = [int, float, str, bool]
        assert type(d) == dict
        for key, value in d.items():
            assert type(key) in valid
            assert type(value) in valid

    @pybt
    def test_nested_list_types(self, l: List[List[Int | Float | Str | Bool]]):
        valid = [int, float, str, bool]
        assert type(l) == list
        for el in l:
            assert type(l) == list
            for e in el:
                assert type(e) in valid

    @pybt
    def test_nested_dict_types(
        self,
        d: Dict[Int | Str | Bool | Float, Dict[Int | Str | Bool | Float, List[Int]]],
    ):
        valid = [int, float, str, bool]
        assert type(d) == dict
        for key, value in d.items():
            assert type(key) in valid
            assert type(value) == dict
            for k, v in value.items():
                assert type(k) in valid
                assert type(v) == list
                for el in v:
                    assert type(el) == int

    @pybt
    def test_handles_none(self, p: Int | NoneType):
        assert p is None or type(p) == int

    @pybt
    def test_handles_none_in_complex_list(self, l: List[NoneType]):
        assert type(l) == list
        for el in l:
            assert el is None

    @pybt
    def test_handles_none_in_complex_dict(self, d: Dict[NoneType, NoneType]):
        assert type(d) == dict
        for key, val in d.items():
            assert key is None
            assert val is None