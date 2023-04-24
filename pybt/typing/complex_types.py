import random
import typing as PythonTyping
from types import UnionType

from pybt.typing.basic_types import Int, Str, Bool, Float, NoneType
from pybt.typing.core import _flat_union


""" 
This file implements union, any, list, tuple, and dict types for PyBT 

TODO: Ensure that types passed are pybt types 
"""

_DEFAULT_MAX_DEPTH = 2
_DEFAULT_MAX_LEN = 10
_DEFAULT_SUB_TYPE = None

T = PythonTyping.TypeVar("T")


def _get_next(choices):
    if not choices:
        return NoneType()
    if len(choices) > 1:
        choice = choices[random.randint(0, len(choices) - 1)]
    else:
        choice = choices[0]

    if type(choice) in [Any, List, Tuple, Dict, Int, Str, Bool, Float, NoneType]:
        return choice
    else:
        return choice()


class Union:
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE):
        self.sub_type: UnionType = None
        if sub_type:
            self.sub_type = sub_type

    def generate(self) -> any:
        if not self.sub_type:
            sub_type_choices = [Any()]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        choice = _get_next(sub_type_choices)

        return choice.generate()

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

        return cls(sub_type)


class Any:
    def __init__(self, max_depth=_DEFAULT_MAX_DEPTH, max_len=_DEFAULT_MAX_LEN):
        self.max_depth: int = _DEFAULT_MAX_DEPTH
        self.max_len: int = _DEFAULT_MAX_LEN
        if max_depth is not None:
            self.max_depth = max_depth
        if max_len is not None:
            self.max_len = max_len

    def create_any(self, base_type, times_called):
        _ALL_TYPES: list = [List, Tuple, Dict, Int, Str, Bool, Float, NoneType]
        _BASE_TYPES: list = [Int, Str, Bool, Float, NoneType]
        types = []
        for _ in range(self.max_len):
            next = _ALL_TYPES[random.randint(0, len(_ALL_TYPES) - 1)]
            if next in [List, Tuple, Dict]:
                if times_called <= self.max_depth:
                    types.append(self.create_any(next, times_called + 1))
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
            return base_type().generate()
        elif type(base_type) in _BASE_TYPES:
            return base_type.generate()

        type_to_gen = self.create_any(base_type, 0)
        return type_to_gen.generate()

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

        return cls(max_len, max_depth)


class List:
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE, max_len=_DEFAULT_MAX_LEN):
        self.max_len: int = _DEFAULT_MAX_LEN
        self.sub_type = sub_type
        if max_len is not None:
            self.max_len = max_len

    def generate(self) -> list:
        if not self.sub_type:
            sub_type_choices = [Any()]
        else:
            sub_type_choices = _flat_union(self.sub_type)

        list_gen = []
        for _ in range(random.randint(0, self.max_len)):
            t = _get_next(sub_type_choices)
            list_gen.append(t.generate())
        return list_gen

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

        return cls(sub_type, max_len)


class Tuple(List):
    def __init__(self, sub_type=_DEFAULT_SUB_TYPE, max_len=_DEFAULT_MAX_LEN):
        self.max_len = _DEFAULT_MAX_LEN
        self.sub_type = sub_type
        if max_len is not None:
            self.max_len = max_len

    def generate(self) -> list:
        list_type = List[self.sub_type, self.max_len]
        return tuple(list_type.generate())

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

        return cls(sub_type, max_len)


class Dict:
    def __init__(
        self,
        key_type=_DEFAULT_SUB_TYPE,
        arg_type=_DEFAULT_SUB_TYPE,
        max_keys=_DEFAULT_MAX_LEN,
    ):
        self.max_keys: int = _DEFAULT_MAX_LEN
        self.key_type = key_type
        self.arg_type = arg_type
        if max_keys is not None:
            self.max_keys = max_keys

    def generate(self) -> dict:
        if not self.key_type:
            key_type_choices = [Int, Float, Bool, Str]
        else:
            key_type_choices = _flat_union(self.key_type)

        if not self.arg_type:
            arg_type_choices = [Any()]
        else:
            arg_type_choices = _flat_union(self.arg_type)

        dict_gen = {}
        for _ in range(random.randint(0, self.max_keys)):
            key = _get_next(key_type_choices)
            arg = _get_next(arg_type_choices)
            dict_gen[key.generate()] = arg.generate()
        return dict_gen

    def __str__(self):
        return "pybt.types.Dict"

    def __class_getitem__(cls, parameters):
        key_type = None
        arg_type = None
        max_keys = None
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

        return cls(key_type, arg_type, max_keys)
