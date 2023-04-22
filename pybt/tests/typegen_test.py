from typing import Callable

from unittest import TestCase
from pybt.core import pybt


class TestTypeGen(TestCase):
    @pybt
    def test_simple_list(self, l: list):
        assert type(l) == list

    @pybt
    def test_simple_dict(self, d: dict):
        assert type(d) == dict

    @pybt
    def test_simple_int(self, i: int):
        assert type(i) == int

    @pybt
    def test_simple_float(self, f: float):
        assert type(f) == float

    @pybt
    def test_simple_bool(self, b: bool):
        assert type(b) == bool

    @pybt
    def test_simple_string(self, s: str):
        assert type(s) == str

    @pybt
    def test_simple_union(self, s: int | float | str | bool):
        valid = [int, float, str, bool]
        assert type(s) in valid

    @pybt
    def test_list_simple_union(self, l: list[int | float | str | bool]):
        valid = [int, float, str, bool]
        assert type(l) == list
        for el in l:
            assert type(el) in valid

    @pybt
    def test_dict_simple_union(
        self, d: dict[int | float | str | bool, int | float | str | bool]
    ):
        valid = [int, float, str, bool]
        assert type(d) == dict
        for key, value in d.items():
            assert type(key) in valid
            assert type(value) in valid

    @pybt
    def test_nested_list_types(self, l: list[list[int | float | str | bool]]):
        valid = [int, float, str, bool]
        assert type(l) == list
        for el in l:
            assert type(l) == list
            for e in el:
                assert type(e) in valid

    @pybt
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

    @pybt
    def test_handles_none(self, p: int | None):
        assert p is None or type(p) == int

    @pybt
    def test_handles_none_in_complex_list(self, l: list[None]):
        assert type(l) == list
        for el in l:
            assert el is None

    @pybt
    def test_handles_none_in_complex_dict(self, d: dict[None, None]):
        assert type(d) == dict
        for key, val in d.items():
            assert key is None
            assert val is None

    @pybt
    def test_handles_none_in_unioned_complex_dict(
        self, d: dict[str | int, None | list[None] | int]
    ):
        assert type(d) == dict
        for key, val in d.items():
            assert type(key) in [str, int]
            assert val is None or type(val) in [list, int]
            if type(val) == list:
                for el in val:
                    assert el is None

    @pybt
    def test_handles_none_in_unioned_complex_list(
        self, l: list[str | None | dict[int, None]]
    ):
        assert type(l) == list
        for el in l:
            assert el is None or type(el) in [str, dict]
            if type(el) == dict:
                for key, val in el.items():
                    assert type(key) == int
                    assert val is None

    @pybt
    def test_handles_callable_with_explicit_args(
        self, f: Callable[[int, int], bool], x: int, y: int
    ):
        assert type(f(x, y)) == bool

    @pybt
    def test_handles_callable_with_implicit_args(
        self, f: Callable[..., bool], x: int, y: int
    ):
        assert type(f(x, y)) == bool

    @pybt
    def test_handles_callable_with_union(
        self, f: Callable[[int, int], list | int | str], x: int, y: int
    ):
        assert type(f(x, y)) in [list, int, str]

    @pybt
    def test_handles_callable_with_nested_union(
        self,
        f: Callable[[int, int], list[int | str | list[int]] | int | str],
        x: int,
        y: int,
    ):
        ret = f(x, y)
        assert type(ret) == list
        for el in ret:
            assert type(el) in [int, str, list]
            if type(el) == list:
                for el_ in el:
                    assert type(el_) == int

    @pybt
    def test_handles_callable_with_list(self, f: Callable[..., list], x: int, y: int):
        assert type(f(x, y)) == list

    @pybt
    def test_handles_callable_with_dict(self, f: Callable[..., dict], x: int, y: int):
        assert type(f(x, y)) == dict

    @pybt
    def test_handles_callable_with_any_and_lower_case_callable(
        self, f: callable, x: int, y: int
    ):
        f(x, y)

    @pybt
    def test_handles_callable_with_any_and_upper_case_callable(
        self, f: Callable, x: int, y: int
    ):
        f(x, y)
