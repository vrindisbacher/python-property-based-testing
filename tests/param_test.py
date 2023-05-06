from unittest import TestCase
from pybt.core import pybt
from pybt.typing.type_declarations import Int, Str, Float, List
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

    def test_invalid_int_params(self):
        try:

            @pybt
            def _test(i: int):
                ...

            _test()
            self.fail("This is an int which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_str_params(self):
        try:

            @pybt
            def _test(i: str):
                ...

            _test()
            self.fail("This is a str which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_bool_params(self):
        try:

            @pybt
            def _test(i: bool):
                ...

            _test()
            self.fail("This is a bool which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_float_params(self):
        try:

            @pybt
            def _test(i: float):
                ...

            _test()
            self.fail("This is a float which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_list_params(self):
        try:

            @pybt
            def _test(i: list):
                ...

            _test()
            self.fail("This is a list which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_dict_params(self):
        try:

            @pybt
            def _test(i: dict):
                ...

            _test()
            self.fail("This is a dict which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_tuple_params(self):
        try:

            @pybt
            def _test(i: tuple):
                ...

            _test()
            self.fail("This is a tuple which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_function_params(self):
        try:

            @pybt
            def _test(i: callable):
                ...

            _test()
            self.fail("This is a callable which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_any_params(self):
        try:

            @pybt
            def _test(i: any):
                ...

            _test()
            self.fail("This is any which is not a PyBT type. This should fail")
        except MistypedSignature:
            ...

    def test_invalid_union_params(self):
        try:

            @pybt
            def _test(i: List[int | str | list[bool]]):
                ...

            _test()
            self.fail(
                "This is an invalid union type because it has an int, str, and list of booleans, which are not PyBT types. This should fail"
            )
        except MistypedSignature:
            ...
