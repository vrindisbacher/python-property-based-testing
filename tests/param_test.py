from unittest import TestCase
from pybt.core import pybt
from pybt.typing.type_declarations import Int, Str, Float 
from pybt.core.exception import InvalidArgs, MistypedSignature


class ParamTestCase(TestCase):
    @pybt
    def test_return_annotations(self, i: Int) -> float:
        assert i == i

    @pybt
    def test_typed_func_vars_and_return_type(self, i: Float) -> list:
        x: int = 1
        assert type(x) != type(i)

    @pybt
    def test_no_args(self):
        assert 1 == 1

    def test_invalid_args(self):
        try:
            pybt(n=0)
            pybt(hypotheses=1)

            self.fail("Invalid args to pybt. This should fail.")
        except InvalidArgs:
            pass

    @pybt
    def test_keyword_args(self, i: Int, keyword=None):
        assert keyword is None
        assert type(i) == int

    def test_raises_signature_error(self):
        try:

            @pybt
            def _test(i: Int, keyword):
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
    def test_no_arg_type(self, i: Int):
        ...

    @pybt
    def test_arg_type(self, i: Int[1, 2]):
        ...

    @pybt
    def test_ignores_body_types(self, i: Int):
        x: int = i
        assert type(i) == int
        assert type(x) == int

    @pybt
    def test_ignores_return_types(self, i: Int) -> str:
        ...

    @pybt
    def test_ignores_typed_keywords(self, keyword: Str = None):
        assert keyword is None

    @pybt
    def test_ignores_all_unneeded_types(self, i: Int, keyword: Str = None) -> None:
        x: int = i
        assert type(x) == int
        assert type(i) == int
        assert keyword is None