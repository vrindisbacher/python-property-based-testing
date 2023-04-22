from typing import Callable
from functools import wraps, partial

from pybt.core.core import MAX_BASE_SIZE, MAX_COMPLEX_SIZE

from pybt.core.exception import InvalidArgs

from pybt.core.core import _validate_and_return_args, _set_args, _drive_tests


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
    parameter hypotheses : hypotheses that the generated args must agree with
    parameter max_basic_arg_size : maximum arg size for strings, ints, float etc.
    parameter max_complex_arg_size : maximum size to use for all structures (list, dicts)
    """

    if n <= 0:
        raise InvalidArgs("You should run more than 0 iterations! Please set n > 0.")
    if generators and type(generators) != dict:
        raise InvalidArgs(
            "Invalid generators! Please try again with a dict of argument name to function"
        )
    if hypotheses and type(hypotheses) != dict:
        raise InvalidArgs(
            """
            Invalid hypotheses! Please try again with a dict of 
            argument name to function that returns a boolean
            """
        )
    if max_basic_arg_size <= 0:
        raise InvalidArgs("Please set a max basic arg size greater than 0")
    if max_complex_arg_size <= 0:
        raise InvalidArgs("Please set a max complex arg size greater than 0")

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
        self_ref = None
        if len(args) > 0:
            self_ref = args[0]

        type_hints = _validate_and_return_args(f)

        arg_to_generator_map = {}
        _set_args(
            arg_to_generator_map=arg_to_generator_map,
            type_hints=type_hints,
            generators=generators,
            max_basic_arg_size=max_basic_arg_size,
            max_complex_arg_size=max_complex_arg_size,
        )

        _drive_tests(arg_to_generator_map, f, type_hints, n, hypotheses, self_ref)

    return wrapper
