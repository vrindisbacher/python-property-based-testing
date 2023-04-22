from unittest import TestCase
from pybt.core import pybt
from pybt.core.exception import InvalidArgs, MistypedSignature


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

            self.fail("Invalid args to pybt. This should fail.")
        except InvalidArgs:
            pass

    @pybt
    def test_keyword_args(self, i: int, keyword=None):
        assert keyword == None
        assert type(i) == int

    def test_raises_signature_error(self):
        try:

            @pybt
            def _test(i, keyword):
                pass

            _test()
            self.fail("No type annotations provided, this should fail")

        except MistypedSignature:
            pass

    def test_raises_signature_error2(self):
        try:

            @pybt
            def _test(i: int, keyword):
                pass

            _test()
            self.fail("No type annotations provided, this should fail")

        except MistypedSignature:
            pass

    @pybt
    def test_ignores_body_types(self, i: int):
        x: int = i
        assert type(i) == int

    @pybt
    def test_ignores_return_types(self, i: int) -> str:
        pass

    @pybt
    def test_ignores_typed_keywords(self, keyword: str | None = None):
        assert keyword == None

    @pybt
    def test_ignores_all_unneeded_types(self, i: int, keyword: str = None) -> None:
        x: int = i
        assert type(i) == int
        assert keyword == None
