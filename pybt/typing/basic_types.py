from pybt.typing.core import BaseType, GenericAlias, _type_check

import random
import string

""" 
This file defines pybt types for none, int, str, bool, and float
"""


class NoneType(BaseType):
    def __init__(self):
        super().__init__()

    def generate(self) -> int:
        return None

    def __str__(self):
        return "pybt.types.Int"


class Int(BaseType):
    min: int = -1000
    max: int = 1000

    def __init__(self):
        super().__init__()

    def generate(self) -> int:
        return random.randint(self.min, self.max)

    def __str__(self):
        return "pybt.types.Int"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Int[min,max]")

        if len(parameters) == 2:
            _type_check(parameters, (int, int), "Expected 2 ints: Int[min,max]")
            cls.min = parameters[0]
            cls.max = parameters[1]

        elif len(parameters) == 1:
            _type_check(parameters, (int,), "Expected an int: Int[Min]")
            cls.min = parameters[0]

        if cls.min > cls.max:
            raise TypeError(f"Min {cls.min} is greater than Max {cls.max}")

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.min = cls.min
        ga.max = cls.max
        return ga


class Float(BaseType):
    min: float = -1000
    max: float = 1000

    def __init__(self):
        super().__init__()

    def generate(self) -> float:
        return random.random() * random.randint(self.min, self.max)

    def __str__(self):
        return "pybt.types.Float"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Float[min,max]")

        if len(parameters) == 2:
            _type_check(parameters, (int, int), "Expected 2 floats: Float[min,max]")
            cls.min = parameters[0]
            cls.max = parameters[1]

        elif len(parameters) == 1:
            _type_check(parameters, (int,), "Expected a float: Float[min]")
            cls.min = parameters[0]

        if cls.min > cls.max:
            raise TypeError(f"Min {cls.min} is greater than Max {cls.max}")

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.min = cls.min
        ga.max = cls.max
        return ga


class Str(BaseType):
    max_len: int = 100

    def __init__(self):
        super().__init__()

    def generate(self) -> str:
        return "".join(
            random.choices(string.ascii_letters, k=random.randint(1, self.max_len))
        )

    def __str__(self):
        return "pybt.types.Str"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 1:
            raise TypeError("Expected 1 argument: Str[max_length]")

        if len(parameters) == 1:
            _type_check(parameters, (int,), "Expected 1 int: Str[max_length]")
            cls.max_len = parameters[0]

        if cls.max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal 0")

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.max_len = cls.max_len
        return ga


class Bool(BaseType):
    def __init__(self):
        super().__init__()

    def generate(self) -> bool:
        return [True, False][random.randint(0, 1)]

    def __str__(self):
        return "pybt.types.Bool"

    def __class_getitem__(cls):
        raise TypeError("Expected No argument: Bool")