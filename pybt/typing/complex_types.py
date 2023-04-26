from pybt.typing.core import (
    _AnyGenericAlias,
    _DictGenericAlias,
    _FunctionGenericAlias,
    _ListGenericAlias,
    _SetGenericAlias,
    _TupleGenericAlias,
    _UnionGenericAlias,
    BaseType,
)


""" 
This file implements union, any, list, tuple, dict, function types for PyBT 

TODO: Ensure that types passed are pybt types 
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
            raise TypeError("Expected 2 arguments: Any[max_depth, max_length]")
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
