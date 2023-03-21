import typing
from typing import Callable
from functools import wraps, partial


from pybt.core.util import gen_int, gen_float, gen_str, gen_bool
from pybt.core.util import is_base_type


BASIC_TYPE_MAP = {
    int: gen_int,
    float: gen_float,
    str: gen_str,
    bool: gen_bool,
}


def _validate_args(f, type_hints):
    if not len(type_hints):
        raise Exception("No type annotations provided")

    if not len(type_hints) == f.__code__.co_argcount:
        raise Exception("You did not provide type hints for all variables")


def _set_args(arg_to_generator_map, type_hints, generators):
    for arg_name, arg_type in type_hints.items():
        if is_base_type(arg_type):
            if generators and (gen := generators.get(arg_name)):
                arg_to_generator_map[arg_name] = gen
            else:
                arg_to_generator_map[arg_name] = BASIC_TYPE_MAP[arg_type]
        else:
            raise Exception("Only base types are supported")
            # base_type = typing.get_origin(arg_type)
            # sub_types = typing.get_args(arg_type)
            # print(base_type, sub_types)


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
            print(f"Args passed : {[x for x in args_to_pass]}")
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

