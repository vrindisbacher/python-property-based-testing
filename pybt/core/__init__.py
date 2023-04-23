from functools import wraps, partial

from pybt.core.exception import InvalidArgs

from pybt.core.core import _validate_and_return_args, _drive_tests


def pybt(f=None, n: int = 1000, hypotheses: dict[str, any] = None):
    """
    A decorator to use as entry point for pb-testing all functions

    parameter f : the function that the decorator sits on and the function that defines the test spec
    parameter n : the number of tests to run
    parameter hypotheses : hypotheses that the generated args must agree with
    """

    if n <= 0:
        raise InvalidArgs("You should run more than 0 iterations! Please set n > 0.")

    if hypotheses and type(hypotheses) != dict:
        raise InvalidArgs(
            """
            Invalid hypotheses! Please try again with a dict of 
            argument name to function that returns a boolean
            """
        )

    if f is None:
        return partial(
            pybt,
            n=n,
            hypotheses=hypotheses,
        )

    @wraps(f)
    def wrapper(*args, **kwargs):
        self_ref = None
        if len(args) > 0:
            self_ref = args[0]

        type_hints = _validate_and_return_args(f)

        _drive_tests(f, type_hints, n, hypotheses, self_ref)

    return wrapper
