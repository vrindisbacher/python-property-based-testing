import traceback
import inspect

from pybt.core.exception import MistypedSignature, PyBTTestFail
from pybt.typing.core import BaseType


def _validate_and_return_args(f: callable) -> dict[str, type]:
    """
    Validates that the function passed has complete type annotations
    and returns the args to generate.

    parameter f : the function to run tests on

    returns : A dict of str to types representing the args that need to be generated
    """
    type_hints = {}
    signature = inspect.signature(f)
    params = signature.parameters
    for key, val in params.items():
        # ignore if the key is self
        if key == "self":
            continue

        annot = val.annotation
        default_arg = val.default
        if annot == inspect._empty and default_arg == inspect._empty:
            raise MistypedSignature(
                f"""
                Variable {key} is not annotated, and is not a keyword argument or self. 
                Please type all non-keyword arguments.
                """
            )

        if default_arg == inspect._empty:
            type_hints[key] = annot

    return type_hints


def _drive_tests(
    f: callable,
    type_hints: dict[str, BaseType],
    n: int,
    hypotheses: dict[str, any],
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

        for name, val in type_hints.items():
            if hypotheses and (h := hypotheses.get(name)):
                hypothesis = h

            arg = val.generate(val)
            while not hypothesis(arg):
                arg = val.generate(val)
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
