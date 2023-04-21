from unittest import TestCase
from pybt.core.core import pybt


class TestTypeGen(TestCase):
    pybt_small = pybt(max_basic_arg_size=100, max_complex_arg_size=10)

    @pybt_small
    def test_simple_list(self, l: list):
        assert type(l) == list

    @pybt_small
    def test_simple_dict(self, d: dict):
        assert type(d) == dict

    @pybt_small
    def test_simple_int(self, i: int):
        assert type(i) == int

    @pybt_small
    def test_simple_float(self, f: float):
        assert type(f) == float

    @pybt_small
    def test_simple_bool(self, b: bool):
        assert type(b) == bool

    @pybt_small
    def test_simple_string(self, s: str):
        assert type(s) == str

    @pybt_small
    def test_simple_union(self, s: int | float | str | bool):
        valid = [int, float, str, bool]
        assert type(s) in valid

    @pybt_small
    def test_list_simple_union(self, l: list[int | float | str | bool]):
        valid = [int, float, str, bool]
        assert type(l) == list
        for el in l:
            assert type(el) in valid

    @pybt_small
    def test_dict_simple_union(
        self, d: dict[int | float | str | bool, int | float | str | bool]
    ):
        valid = [int, float, str, bool]
        assert type(d) == dict
        for key, value in d.items():
            assert type(key) in valid
            assert type(value) in valid

    @pybt_small
    def test_nested_list_types(self, l: list[list[int | float | str | bool]]):
        valid = [int, float, str, bool]
        assert type(l) == list
        for el in l:
            assert type(l) == list
            for e in el:
                assert type(e) in valid

    @pybt_small
    def test_nested_dict_types(
        self,
        d: dict[int | str | bool | float, dict[int | str | bool | float, list[int]]],
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
