import random
import typing as PythonTyping
from types import UnionType

from pybt.typing.basic_types import Int, Str, Bool, Float, NoneType
from pybt.typing.core import BaseType, GenericAlias, _flat_union


""" 
This file implements union, any, list, tuple, and dict types for PyBT 

TODO: Ensure that types passed are pybt types 
"""


def _get_next(choices):
    if len(choices) > 1:
        return choices[random.randint(0, len(choices) - 1)]
    else:
        return choices[0]


class Union(BaseType):
    sub_type: UnionType = None

    def __init__(self):
        super().__init__()

    def generate(self) -> any:
        if not self.sub_type:
            sub_type_choices = [Any]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        if len(sub_type_choices) > 1:
            choice = sub_type_choices[random.randint(0, len(sub_type_choices) - 1)]
        else:
            choice = sub_type_choices[0]

        return choice.generate(choice)

    def __str__(self):
        return "pybt.types.Union"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 1:
            raise TypeError("Expected 2 arguments: Any[max_depth, max_length]")
        if len(parameters):
            cls.sub_type = parameters[0]

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.sub_type = cls.sub_type
        return ga


class Any(BaseType):
    max_depth: int = 2
    max_len: int = 10

    def __init__(self):
        super().__init__()

    def create_any(self, base_type, times_called):
        _ALL_TYPES: list = [List, Tuple, Int, Str, Bool, Float, NoneType]
        _BASE_TYPES: list = [Int, Str, Bool, Float, NoneType]
        types = []
        for _ in range(self.max_len):
            next = _ALL_TYPES[random.randint(0, len(_ALL_TYPES) - 1)]
            if next in [List, Tuple, Dict]:
                if times_called <= self.max_depth:
                    types.append(self.create_any(self, next, times_called + 1))
            else:
                types.append(next)

        sub_types = PythonTyping._UnionGenericAlias(UnionType, tuple(types))

        if base_type == Dict:
            key_type = _BASE_TYPES[random.randint(0, len(_BASE_TYPES) - 1)]
            return base_type[key_type, sub_types]

        return base_type[sub_types]

    def generate(self, base_type=None) -> list:
        _ALL_TYPES: list = [List, Tuple, Int, Str, Bool, Float, NoneType]
        _BASE_TYPES: list = [Int, Str, Bool, Float, NoneType]
        if not base_type:
            base_type = _ALL_TYPES[random.randint(0, len(_ALL_TYPES) - 1)]

        if base_type in _BASE_TYPES:
            return base_type.generate(base_type)

        type_to_gen = self.create_any(self, base_type, 0)
        return type_to_gen.generate(type_to_gen)

    def __str__(self):
        return "pybt.types.Any"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Any[max_depth, max_length]")
        if len(parameters):
            cls.max_depth = parameters[0]
        if len(parameters) > 1:
            cls.max_len = parameters[1]

        if cls.max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal to 0")
        if cls.max_depth <= 0:
            raise TypeError(f"Max Depth of {cls.max_depth} is less than or equal to 0")

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.max_depth = cls.max_depth
        ga.max_len = cls.max_len
        return ga


class List(BaseType):
    max_len: int = 20
    sub_type: type = None

    def __init__(self):
        super().__init__()

    def generate(self) -> list:
        if not self.sub_type:
            sub_type_choices = [Any]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        list_gen = []
        for _ in range(random.randint(0, self.max_len)):
            t = _get_next(sub_type_choices)
            list_gen.append(t.generate(t))
        return list_gen

    def __str__(self):
        return "pybt.types.List"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: List[sub_type, max_length]")
        if len(parameters):
            cls.sub_type = parameters[0]
        if len(parameters) > 1:
            cls.max_len = parameters[1]

        if cls.max_len <= 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than or equal to 0")

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.sub_type = cls.sub_type
        ga.max_len = cls.max_len
        return ga


class Tuple(List):
    max_len: int = 20
    sub_type: type = None

    def __init__(self):
        super(self).__init__()

    def generate(self) -> list:
        list_type = List[self.sub_type, self.max_len]
        return tuple(list_type.generate(list_type))

    def __str__(self):
        return "pybt.types.Tuple"


class Dict(BaseType):
    key_type: BaseType | GenericAlias = None
    arg_type: BaseType | GenericAlias = None
    max_keys: int = 20

    def __init__(self):
        super().__init__()

    def generate(self) -> dict:
        if not self.key_type:
            key_type_choices = [Int, Float, Bool, Str]
        else:
            key_type_choices = _flat_union(self.key_type)

        if not self.arg_type:
            arg_type_choices = [Any]
        else:
            arg_type_choices = _flat_union(self.arg_type)

        dict_gen = {}
        for _ in range(random.randint(0, self.max_keys)):
            key = _get_next(key_type_choices)
            arg = _get_next(arg_type_choices)
            dict_gen[key.generate(key)] = arg.generate(arg)
        return dict_gen

    def __str__(self):
        return "pybt.types.Dict"

    def __class_getitem__(cls, parameters):
        if len(parameters) > 3:
            raise TypeError(
                "Expected 3 arguments: Dict[key_type, arg_type, max_length]"
            )

        if len(parameters):
            cls.key_type = parameters[0]
        if len(parameters) > 1:
            cls.arg_type = parameters[1]
        if len(parameters) > 2:
            cls.max_keys = parameters[2]

        if cls.max_keys <= 0:
            raise TypeError(f"Max # of Keys of {cls.max_keys} is less than or equal 0")

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.key_type = cls.key_type
        ga.arg_type = cls.arg_type
        ga.max_keys = cls.max_keys
        return ga
