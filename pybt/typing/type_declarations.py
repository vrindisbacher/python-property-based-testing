from pybt.typing.core import (
    BaseType,
    _BoolGenericAlias,
    _NoneGenericAlias,
    _FloatGenericAlias,
    _StringGenericAlias,
    _IntGenericAlias,
    _AnyGenericAlias,
    _DictGenericAlias,
    _FunctionGenericAlias,
    _ListGenericAlias,
    _SetGenericAlias,
    _TupleGenericAlias,
    _UnionGenericAlias,
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


"""
We now move to declaration of complex types 
"""


class Union(BaseType):
    _alias = _UnionGenericAlias

    def __str__(self):
        return "pybt.types.Union"

    def __class_getitem__(cls, parameters):
        sub_type = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 1:
            raise TypeError("Expected 1 argument: Union[sub_type]")
        if len(parameters):
            sub_type = parameters[0]

        return _UnionGenericAlias(sub_type)


class Any(BaseType):
    _alias = _AnyGenericAlias

    def __str__(self):
        return "pybt.types.Any"

    def __class_getitem__(cls, parameters):
        max_depth = None
        max_len = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Any[max_depth, max_length]")
        if len(parameters):
            max_depth = parameters[0]
        if len(parameters) > 1:
            max_len = parameters[1]

        if max_len and max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal to 0")
        if max_depth <= 0:
            raise TypeError(f"Max Depth of {cls.max_depth} is less than or equal to 0")

        return _AnyGenericAlias(max_len, max_depth)


class List(BaseType):
    _alias = _ListGenericAlias

    def __str__(self):
        return "pybt.types.List"

    def __class_getitem__(cls, parameters):
        sub_type = None
        max_len = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: List[sub_type, max_length]")
        if len(parameters):
            sub_type = parameters[0]
        if len(parameters) > 1:
            max_len = parameters[1]

        if max_len and max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal to 0")

        return _ListGenericAlias(sub_type, max_len)


class Tuple(BaseType):
    _alias = _TupleGenericAlias

    def __str__(self):
        return "pybt.types.Tuple"

    def __class_getitem__(cls, parameters):
        sub_type = None
        max_len = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Tuple[sub_type, max_length]")
        if len(parameters):
            sub_type = parameters[0]
        if len(parameters) > 1:
            max_len = parameters[1]

        if max_len and max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal to 0")

        return _TupleGenericAlias(sub_type, max_len)


class Set(BaseType):
    _alias = _SetGenericAlias

    def __str__(self):
        return "pybt.types.Set"

    def __class_getitem__(cls, parameters):
        sub_type = None
        max_len = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Set[sub_type, max_length]")
        if len(parameters):
            sub_type = parameters[0]
        if len(parameters) > 1:
            max_len = parameters[1]

        if max_len and max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal to 0")

        return _SetGenericAlias(sub_type, max_len)


class Dict(BaseType):
    _alias = _DictGenericAlias

    def __str__(self):
        return "pybt.types.Dict"

    def __class_getitem__(cls, parameters):
        key_type = None
        arg_type = None
        max_keys = None
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 3:
            raise TypeError(
                "Expected 3 arguments: Dict[key_type, arg_type, max_length]"
            )

        if len(parameters):
            key_type = parameters[0]
        if len(parameters) > 1:
            arg_type = parameters[1]
        if len(parameters) > 2:
            max_keys = parameters[2]

        if max_keys and max_keys <= 0:
            raise TypeError(f"Max # of Keys of {cls.max_keys} is less than or equal 0")

        return _DictGenericAlias(key_type, arg_type, max_keys)


class Function(BaseType):
    _alias = _FunctionGenericAlias

    def __str__(self):
        return "pybt.types.Function"

    def __class_getitem__(cls, parameters):
        return_type = None
        if type(parameters) != tuple:
            parameters = (parameters,)
        if len(parameters) > 1:
            raise TypeError("Expected 3 arguments: Function[return_type]")

        if len(parameters):
            return_type = parameters[0]

        return _FunctionGenericAlias(return_type)
