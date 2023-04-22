import traceback
import typing
from functools import partial
from types import UnionType
from typing import Any, Callable

from pybt.core.exception import (
    MistypedDict,
    MistypedSignature,
    PyBTTestFail,
)
from pybt.core.util import (
    gen_any,
    gen_bool,
    gen_dict,
    gen_float,
    gen_int,
    gen_list,
    gen_str,
    is_base_type,
)

MAX_BASE_SIZE = 1000000
MAX_COMPLEX_SIZE = 100


BASIC_TYPE_MAP = {
    int: lambda size: partial(gen_int, size),
    float: lambda size: partial(gen_float, size),
    str: lambda size: partial(gen_str, size),
    bool: lambda _: gen_bool,
}

DATA_STRUCT_TYPE_MAP = {
    dict: lambda size, dict_type_gen: partial(gen_dict, size, dict_type_gen),
    list: lambda size, list_type_gen: partial(gen_list, size, list_type_gen),
}


def _validate_args(f: callable, type_hints: dict[str, type]) -> bool:
    """
    Validates that the function passed has complete type annotations

    parameter f : the function to run tests on
    parameter type_hints : the type hints provided by the user (from typing.get_type_hints)

    returns : a boolean indicating whether the function has complete type annotations
    """
    all_vars = set(f.__code__.co_varnames).difference(set(["self"]))
    if not set(type_hints.keys()).difference(all_vars) == set():
        raise MistypedSignature("Please provide type hints for all variables")


def _get_complex_args_helper(
    arg_type: type,
    arg_struct: list[callable],
    max_basic_arg_size: int,
    max_complex_arg_size: int,
) -> list[callable]:
    """
    Generates a list of functions handling complex types.

    parameter arg_type : the type we need to handle (generate a function for)
    parameter arg_struct : the list of generators we build recursively
    parameter max_basic_arg_size : the max size for basic datatypes
    parameter max_complex_arg_size : the max size for complex types

    returns : a list of callable which is the generator for our arg type
    """
    base_type = typing.get_origin(arg_type)
    sub_types = typing.get_args(arg_type)

    if base_type == dict and sub_types:
        if sub_types[0] not in BASIC_TYPE_MAP and type(sub_types[0]) is not UnionType:
            raise MistypedDict(
                """
                Your dict is not well typed. Please provide an immutable type for key.\n
                If you provided dict[any,any], just use dict. Otherwise, explicitly type the 
                key. 
                """
            )

    if not base_type:
        if b := BASIC_TYPE_MAP.get(arg_type):
            return b(max_basic_arg_size)
        else:
            if arg_type in [any, Any]:
                complex_type = gen_any(max_complex_arg_size)
            else:
                complex_type = gen_any(max_complex_arg_size, arg_type)

            base_type = typing.get_origin(complex_type)
            sub_types = typing.get_args(complex_type)
            if not base_type and (b := BASIC_TYPE_MAP.get(complex_type)):
                return b(max_basic_arg_size)
            elif not base_type:
                raise NotImplementedError(f"type {arg_type} Not Implemented")

    sub_type_struct_list = list(
        map(
            lambda x: _get_complex_args_helper(
                x, [], max_basic_arg_size, max_complex_arg_size
            ),
            sub_types,
        )
    )

    if len(sub_type_struct_list) == 1 and type(sub_type_struct_list[0]) is list:
        sub_type_struct_list = sub_type_struct_list[0]

    if base_type is UnionType:
        return sub_type_struct_list
    else:
        if base_type in DATA_STRUCT_TYPE_MAP:
            arg_struct.append(
                DATA_STRUCT_TYPE_MAP[base_type](
                    max_complex_arg_size, sub_type_struct_list
                )
            )
        else:
            raise NotImplementedError(f"{base_type} Is Not Implemented")

        return arg_struct


def _get_complex_args(
    arg_type: type, max_basic_arg_size: int, max_complex_arg_size: int
) -> callable:
    """
    Generates a list of functions handling complex types.

    parameter arg_type : the type we need to handle (generate a function for)
    parameter max_basic_arg_size : the max size for basic datatypes
    parameter max_complex_arg_size : the max size for complex types

    returns : a callable which is the generator for arg_type
    """

    return _get_complex_args_helper(
        arg_type, [], max_basic_arg_size, max_complex_arg_size
    )[0]


def _set_args(
    arg_to_generator_map: dict[str, callable],
    type_hints: dict[str, type],
    generators: dict[str, callable],
    max_basic_arg_size: int,
    max_complex_arg_size: int,
) -> None:
    """
    Generates a list of functions handling complex types.

    This updates arg_to_generator_map in place, setting the proper generator
    for each value.

    parameter arg_to_generator_map : a map to store generators for variables
    parameter type_hints : the type hints from typing.get_type_hints
    parameter generators : User provided generators for function arguments
    parameter max_basic_arg_size : the max size for basic datatypes
    parameter max_complex_arg_size : the max size for complex types

    returns : Nothing
    """
    for arg_name, arg_type in type_hints.items():
        found = False
        if is_base_type(arg_type) or generators:
            if generators and (gen := generators.get(arg_name)):
                arg_to_generator_map[arg_name] = gen
                found = True
            elif is_base_type(arg_type):
                arg_to_generator_map[arg_name] = BASIC_TYPE_MAP[arg_type](
                    max_basic_arg_size
                )
                found = True
        if not found:
            complex_generator_map = _get_complex_args(
                arg_type, max_basic_arg_size, max_complex_arg_size
            )
            arg_to_generator_map[arg_name] = complex_generator_map


def _drive_tests(
    arg_to_generator_map: dict[str, callable],
    f: callable,
    type_hints: dict[str, type],
    n: int,
    hypotheses: dict[str, Callable[..., bool]],
    self_=None,
) -> None:
    """
    Executes n calls of the function f on random arguments

    parameter arg_to_generator_map : a map to store generators for variables
    parameter f : the function to test
    parameter type_hints : the type hints from typing.get_type_hints
    parameter n : the number of tests to run
    parameter hypotheses : User provided restrictions for function arguments

    returns : Nothing. Fails with PyBTTestFail if an error is raised.
    """
    for i in range(n):
        args_to_pass = []

        hypothesis = lambda _: True

        for name in type_hints.keys():
            if hypotheses and (h := hypotheses.get(name)):
                hypothesis = h

            arg = arg_to_generator_map[name]()
            while not hypothesis(arg):
                arg = arg_to_generator_map[name]()
            args_to_pass.append(arg)

        try:
            if self_:
                f(self_, *args_to_pass)
            else:
                f(*args_to_pass)
        except Exception:
            raise PyBTTestFail(
                f"""
                Failed on iteration {i + 1}\n 
                
                Args Passed : {",".join([str(x) for x in args_to_pass])}\n 

                Exception: \n\n\n 
                {traceback.format_exc()}
                """
            )

    print(f"+++ {n} tests passed +++")
