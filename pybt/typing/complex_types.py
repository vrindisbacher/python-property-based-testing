import random
import typing as PythonTyping
from types import UnionType

from pybt.typing.basic_types import Int, Str, Bool, Float
from pybt.typing.core import BaseType, GenericAlias, _type_check, _flat_union


""" 
This file implements any, list, tuple, and dict types for PyBT 
"""


class Any(BaseType):
    max_depth: int = 2
    max_len: int = 10

    def __init__(self):
        super().__init__()

    def create_any(self, base_type, times_called):
        _ALL_TYPES: list = [List, Tuple, Int, Str, Bool, Float]
        _BASE_TYPES: list = [Int, Str, Bool, Float]
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
        _ALL_TYPES: list = [List, Int, Str, Bool, Float]
        _BASE_TYPES: list = [Int, Str, Bool, Float]
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

        if len(parameters) == 2:
            _type_check(
                parameters,
                (
                    int,
                    int,
                ),
                "Expected 2 ints: Any[max_depth, max_length]",
            )
            cls.max_depth = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            _type_check(parameters, (int,), "Expected an int: Any[max_depth]")
            cls.max_depth = parameters[0]

        if cls.max_len < 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than 0")

        if not cls.sub_type:
            cls.sub_type = Any

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.max_depth = cls.max_depth
        ga.max_len = cls.max_len
        ga._ALL_TYPES = cls._ALL_TYPES
        ga._BASE_TYPES = cls._BASE_TYPES
        return ga


class List(BaseType):
    max_len: int = 100
    sub_type: type = None

    def __init__(self):
        super().__init__()

    def generate(self) -> list:
        if not self.sub_type:
            sub_type_choices = [Any]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        def _get_next():
            if len(sub_type_choices) > 1:
                return sub_type_choices[random.randint(0, len(sub_type_choices) - 1)]
            else:
                return sub_type_choices[0]

        # act according to the subtypes
        list_gen = []
        for _ in range(random.randint(0, self.max_len)):
            t = _get_next()
            list_gen.append(t.generate(t))
        return list_gen

    def __str__(self):
        return "pybt.types.List"

    def __class_getitem__(cls, parameters):
        if type(parameters) != tuple:
            parameters = (parameters,)

        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: List[sub_type, max_length]")

        if len(parameters) == 2:
            _type_check(
                parameters,
                (
                    type,
                    int,
                ),
                "Expected types and 1 int: List[sub_type, max_length]",
            )
            cls.sub_type = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            # _type_check(
            #     parameters, (type,), "Expected PyBT type: List[sub_type]"
            # )
            cls.sub_type = parameters[0]

        if cls.max_len < 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than 0")

        if not cls.sub_type:
            cls.sub_type = Any

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.sub_type = cls.sub_type
        ga.max_len = cls.max_len
        return ga


class Tuple(List):
    max_len: int = 100
    sub_type: type = None

    def __init__(self):
        super(self).__init__()

    def generate(self) -> list:
        return tuple(self.generate(self))

    def __str__(self):
        return "pybt.types.Tuple"


class Dict(BaseType):
    key_type: BaseType | GenericAlias = Any
    arg_type: BaseType | GenericAlias = Any

    def __init__(self):
        super().__init__()

    def generate(self) -> dict:
        ...

    def __str__(self):
        return "pybt.types.Dict"

    def __class_getitem__(cls, parameters):
        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: Dict[key_type, arg_type]")

        if len(parameters) == 2:
            # _type_check(
            #     parameters,
            #     (type, type),
            #     "Expected type and type: Dict[key_type, arg_type]",
            # )
            cls.sub_type = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            # _type_check(parameters, (BaseType,), "Expected PyBT type: Dict[sub_type]")
            cls.sub_type = parameters[0]

        ga = GenericAlias(cls, parameters, cls.generate)
        ga.key_type = cls.key_type
        ga.arg_type = cls.arg_type
        return ga
