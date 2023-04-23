# from pybt.core import pybt
# from unittest import TestCase

# from typing import Callable
# from pybt.core.util import gen_any


# def fold(f: Callable[..., int], l, initial):
#     initial = 0
#     for el in l:
#         initial = f(initial, el)
#     return initial


# @pybt
# def test_fold_without_unittest(f: Callable[..., int], l: list[int]):
#     assert type(fold(f, l, 0)) == int


# class TestFold(TestCase):
#     @pybt
#     def test_fold(self, f: Callable[..., int], l: list[int]):
#         assert type(fold(f, l, 0)) == int

#     def test_fold_without_fixture(self):
#         test_fold_without_unittest()

#     def test_gen_any(self):
#         gen_any(2,list)