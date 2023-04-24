from pybt.typing.core import _type_check

import random
import string

""" 
This file defines pybt types for none, int, str, bool, and float
"""

_DEFAULT_MIN = -1000
_DEFAULT_MAX = 1000
_DEFAULT_MAX_LEN = 10


class NoneType:
    def __init__(self):
        super().__init__()

    def generate(self) -> None:
        return None

    def __str__(self):
        return "pybt.types.None"


class Int:
    def __init__(self, min=_DEFAULT_MIN, max=_DEFAULT_MAX):
        self.min: int = _DEFAULT_MIN
        self.max: int = _DEFAULT_MAX
        if min:
            self.min = min
        if max:
            self.max = max
        super().__init__()

    def generate(self) -> int:
        return random.randint(self.min, self.max)

    def __str__(self):
        return "pybt.types.Int"

    def __class_getitem__(cls, parameters):
        min = None
        max = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Int[min,max]")

        if len(parameters) == 2:
            _type_check(parameters, (int, int), "Expected 2 ints: Int[min,max]")
            min = parameters[0]
            max = parameters[1]

        elif len(parameters) == 1:
            _type_check(parameters, (int,), "Expected an int: Int[Min]")
            min = parameters[0]

        if min > max:
            raise TypeError(f"Min {min} is greater than Max {max}")

        return cls(min, max)


class Float:
    def __init__(self, min=_DEFAULT_MIN, max=_DEFAULT_MAX):
        self.min: float = _DEFAULT_MIN
        self.max: float = _DEFAULT_MAX
        if min:
            self.min = min
        if max:
            self.max = max
        super().__init__()

    def generate(self) -> float:
        return random.random() * random.randint(self.min, self.max)

    def __str__(self):
        return "pybt.types.Float"

    def __class_getitem__(cls, parameters):
        min = None
        max = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Float[min,max]")

        if len(parameters) == 2:
            _type_check(parameters, (int, int), "Expected 2 floats: Float[min,max]")
            min = parameters[0]
            max = parameters[1]

        elif len(parameters) == 1:
            _type_check(parameters, (int,), "Expected a float: Float[min]")
            min = parameters[0]

        if min > max:
            raise TypeError(f"Min {cls.min} is greater than Max {cls.max}")

        return cls(min, max)


class Str:
    def __init__(self, max_len=_DEFAULT_MAX_LEN):
        self.max_len: int = _DEFAULT_MAX_LEN
        if max_len:
            self.max_len = max_len
        super().__init__()

    def generate(self) -> str:
        return "".join(
            random.choices(string.ascii_letters, k=random.randint(1, self.max_len))
        )

    def __str__(self):
        return "pybt.types.Str"

    def __class_getitem__(cls, parameters):
        max_len = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 1:
            raise TypeError("Expected 1 argument: Str[max_length]")

        if len(parameters) == 1:
            _type_check(parameters, (int,), "Expected 1 int: Str[max_length]")
            max_len = parameters[0]

        if max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal 0")

        return cls(max_len)


class Bool:
    def __init__(self):
        super().__init__()

    def generate(self) -> bool:
        return [True, False][random.randint(0, 1)]

    def __str__(self):
        return "pybt.types.Bool"

    def __class_getitem__(cls):
        raise TypeError("Expected No argument: Bool")
