from unittest import TestCase
from pybt.core.core import pybt
from pybt.core.exception import InvalidArgs

class ParamTestCase(TestCase):
    @pybt
    def test_return_annotations(self, i: int) -> float:
        assert i == i

    @pybt
    def test_typed_func_vars_and_return_type(self, f: float) -> list:
        x: int = 1
        assert type(x) != type(f)

    @pybt
    def test_no_args(self):
        assert 1 == 1

    @pybt(generators={"i": lambda: 1})
    def test_multiple_args_with_gen(self, i: int, l: list[int]):
        assert i == 1
        assert type(l) == list

    @pybt(generators={"l": lambda: [1, 2, 3, 4]})
    def test_complex_type_gen(self, i: int, l: list):
        assert l == [1, 2, 3, 4]
        assert type(i) == int

    @pybt(hypotheses={"i": lambda i: i <= 100})
    def test_hypotheses(self, i: int):
        assert i <= 100

    def test_invalid_args(self):
        try: 
            pybt(n=0)
            pybt(generators=[])
            pybt(hypotheses=1)
            pybt(max_basic_arg_size=-50)
            pybt(max_complex_arg_size=0)

            raise Exception("These Should Not Pass!")
        except InvalidArgs:
            pass 