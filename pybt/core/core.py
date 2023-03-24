import typing
from typing import Callable
from types import UnionType
from functools import wraps, partial


from pybt.core.util import gen_int, gen_float, gen_str, gen_bool, gen_list, gen_dict
from pybt.core.util import is_base_type


MAX_BASE_SIZE = 1000000
MAX_COMPLEX_SIZE = 100


BASIC_TYPE_MAP = {
    int: lambda s: partial(gen_int, s),
    float: lambda _: gen_float,
    str: lambda s: partial(gen_str, s),
    bool: lambda _: gen_bool,
}

DATA_STRUCT_TYPE_MAP = {
    # these are really just a list of type generators to use
    dict: lambda s, d: partial(gen_dict, s, d),
    list: lambda s, l: partial(gen_list, s, l),
}


def _validate_args(f, type_hints):
    if not len(type_hints):
        raise Exception("No type annotations provided")

    if not len(type_hints) == f.__code__.co_argcount:
        raise Exception("Please provide type hints for all variables")


def _get_complex_args_helper(
    arg_type, arg_struct, max_basic_arg_size, max_complex_arg_size
):
    base_type = typing.get_origin(arg_type)

    if not base_type:
        if b := BASIC_TYPE_MAP.get(arg_type):
            return b(max_basic_arg_size)
        else:
            raise Exception(
                f"Type {arg_type} unhandled. Please use a custom generator."
            )
    else:
        sub_types = typing.get_args(arg_type)
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
                raise Exception("Not Implemented")

            return arg_struct


def _get_complex_args(arg_type, max_basic_arg_size, max_complex_arg_size):
    # generates a list of functions handling complex types.
    # for example the following type argument
    # list[int | list[bool]] will generate the
    # following structure
    # function with arg [int, function with arg [bool]]
    return _get_complex_args_helper(
        arg_type, [], max_basic_arg_size, max_complex_arg_size
    )[0]


def _set_args(
    arg_to_generator_map,
    type_hints,
    generators,
    max_basic_arg_size,
    max_complex_arg_size,
):
    for arg_name, arg_type in type_hints.items():
        if is_base_type(arg_type):
            if arg_type == any:
                raise Exception("Please explicitly type your tests")

            if generators and (gen := generators.get(arg_name)):
                arg_to_generator_map[arg_name] = gen
            else:
                arg_to_generator_map[arg_name] = BASIC_TYPE_MAP[arg_type]
        else:
            complex_generator_map = _get_complex_args(
                arg_type, max_basic_arg_size, max_complex_arg_size
            )
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
        except Exception as e:
            print(f"Failed on iteration {i + 1}\n")
            print("Args passed : ", sep=" ")
            for arg in args_to_pass:
                print(arg, sep=", ")
            failed = True
            print("With Exception\n", e)
            break

    if not failed:
        print(f"+++ {n} tests passed +++")


def pybt(
    f=None,
    n: int = 1000,
    generators: dict[str, Callable] = None,
    hypotheses: dict[str, Callable[[any], bool]] = None,
    max_basic_arg_size: int = MAX_BASE_SIZE,
    max_complex_arg_size: int = MAX_COMPLEX_SIZE,
):
    """
    A decorator to use as entry point for pb-testing all functions

    parameter f : the function that the decorator sits on and the function that defines the test spec
    parameter n : the number of tests to run
    parameter generators : user provided generators for function arguments (passed as a dictionary)
    paramater hypotheses : hypotheses that the generated args must agree with
    parameter max_basic_arg_size : maximum arg size for strings, ints, float etc.
    parameter max_complex_arg_size : maximum size to use for all structures (list, dicts)
    """
    if f is None:
        return partial(
            pybt,
            n=n,
            generators=generators,
            hypotheses=hypotheses,
            max_basic_arg_size=max_basic_arg_size,
            max_complex_arg_size=max_complex_arg_size,
        )

    @wraps(f)
    def wrapper(*args, **kwargs):
        type_hints = typing.get_type_hints(f)
        _validate_args(f, type_hints)

        arg_to_generator_map = {}
        _set_args(
            arg_to_generator_map=arg_to_generator_map,
            type_hints=type_hints,
            generators=generators,
            max_basic_arg_size=max_basic_arg_size,
            max_complex_arg_size=max_complex_arg_size,
        )

        _drive_tests(arg_to_generator_map, f, type_hints, n, hypotheses)

        return f

    return wrapper
