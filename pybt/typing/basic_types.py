from pybt.typing.core import (
    _BoolGenericAlias,
    _NoneGenericAlias,
    BaseType,
    _FloatGenericAlias,
    _StringGenericAlias,
    _IntGenericAlias,
)


""" 
This file defines pybt types for none, int, str, bool, and float
"""


def _type_check(args, types, msg):
    for idx, el in enumerate(args):
        if type(el) != types[idx]:
            raise TypeError(msg)


class NoneType(BaseType):
    _alias = _NoneGenericAlias

    def __str__(self):
        return "pybt.types.None"

    def __class_getitem__(cls, _):
        raise TypeError("Expected no argument: NoneType")


class Int(BaseType):
    _alias = _IntGenericAlias

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

        return _IntGenericAlias(min, max)


class Float(BaseType):
    _alias = _FloatGenericAlias

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

        return _FloatGenericAlias(min, max)


class Str(BaseType):
    _alias = _StringGenericAlias

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

        return _StringGenericAlias(max_len)


class Bool(BaseType):
    _alias = _BoolGenericAlias

    def __str__(self):
        return "pybt.types.Bool"

    def __class_getitem__(cls):
        raise TypeError("Expected No argument: Bool")
