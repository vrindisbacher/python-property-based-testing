# from unittest import TestCase
# from pybt.core import pybt


# class TestRevSimple(TestCase):
#     def rev(self, l):
#         return l[::-1]

#     @pybt
#     def test_rev(self, l: list):
#         assert self.rev(self.rev(l)) == l

#     @pybt
#     def test_rev_any(self, l: list[any]):
#         assert self.rev(self.rev(l)) == l

#     @pybt
#     def test_rev_dict(self, l: list[dict]):
#         assert self.rev(self.rev(l)) == l

#     @pybt
#     def test_rev_dict_no_key(self, l: list[dict[str, any]]):
#         assert self.rev(self.rev(l)) == l
