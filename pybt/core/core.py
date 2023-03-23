import typing
from typing import Callable
from types import UnionType
from functools import wraps, partial


from pybt.core.util import gen_int, gen_float, gen_str, gen_bool, gen_list
from pybt.core.util import is_base_type


BASIC_TYPE_MAP = {
    int: gen_int,
    float: gen_float,
    str: gen_str,
    bool: gen_bool,
}

DATA_STRUCT_TYPE_MAP = {
    # these are really just a list of type generators to use
    dict: lambda d: gen_list(d),  # something here
    list: lambda l: gen_list(l),
}


def _validate_args(f, type_hints):
    if not len(type_hints):
        raise Exception("No type annotations provided")

    if not len(type_hints) == f.__code__.co_argcount:
        raise Exception("You did not provide type hints for all variables")


def _get_complex_args_helper(arg_type, arg_struct):
    base_type = typing.get_origin(arg_type)

    if not base_type:
        if b := BASIC_TYPE_MAP.get(arg_type):
            return b
        else:
            raise Exception(
                f"Type {arg_type} unhandled. Please use a custom generator."
            )
    else:
        sub_types = typing.get_args(arg_type)
        sub_type_struct_list = list(
            map(lambda x: _get_complex_args_helper(x, []), sub_types)
        )

        if len(sub_type_struct_list) == 1:
            sub_type_struct_list = sub_type_struct_list[0]

        if base_type is UnionType:
            # ignore the base type
            return sub_type_struct_list
        else:
            if base_type in DATA_STRUCT_TYPE_MAP:
                arg_struct.append(
                    partial(DATA_STRUCT_TYPE_MAP[base_type], sub_type_struct_list)
                )
            else:
                raise Exception("Not Implemented")

            return arg_struct


def _get_complex_args(arg_type):
    # generates a list of types for complex types.
    # for example the following type argument
    # list[int | list[bool]] will generate the
    # following structure
    # [{list : [int, {list : bool}]}]
    return _get_complex_args_helper(arg_type, [])[0]


def _set_args(arg_to_generator_map, type_hints, generators):
    for arg_name, arg_type in type_hints.items():
        if is_base_type(arg_type):
            if generators and (gen := generators.get(arg_name)):
                arg_to_generator_map[arg_name] = gen
            else:
                arg_to_generator_map[arg_name] = BASIC_TYPE_MAP[arg_type]
        else:
            complex_generator_map = _get_complex_args(arg_type)
            arg_to_generator_map[arg_name] = complex_generator_map


def _drive_tests(arg_to_generator_map, f, type_hints, n, hypotheses):
    for i in range(n):
        args_to_pass = []
        hypothesis = lambda x: True
        failed = False
        for name in type_hints.keys():
            if hypotheses and (h := hypotheses.get(name)):
                hypothesis = h

            arg = arg_to_generator_map[name]()
            while not hypothesis(arg):
                arg = arg_to_generator_map[name]()
            args_to_pass.append(arg)

        try:
            f(*args_to_pass)
        except AssertionError as e:
            print(f"Failed on iteration {i + 1}\n")
            print("Args passed : ", sep=" ")
            for arg in args_to_pass:
                print(arg, sep=", ")
            failed = True
            break

    if not failed:
        print(f"+++ {n} tests passed +++")


def pybt(
    f=None,
    n=1000,
    generators: dict[str, Callable] = None,
    hypotheses: dict[str, Callable[[any], bool]] = None,
):
    """
    A decorator to use as entry point for pb-testing all functions

    parameter f : the function that the decorator sits on and the function that defines the test spec
    parameter n : the number of tests to run
    parameter generators : user provided generators for function arguments (passed as a dictionary)
    paramater hypotheses : hypotheses that the generated args must agree with
    """
    if f is None:
        return partial(pybt, n=n, generators=generators, hypotheses=hypotheses)

    @wraps(f)
    def wrapper(*args, **kwargs):
        type_hints = typing.get_type_hints(f)
        _validate_args(f, type_hints)

        arg_to_generator_map = {}
        _set_args(arg_to_generator_map, type_hints, generators)

        _drive_tests(arg_to_generator_map, f, type_hints, n, hypotheses)

        return f

    return wrapper
