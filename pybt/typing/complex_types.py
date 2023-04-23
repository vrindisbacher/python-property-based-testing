import random
from pybt.typing.core import BaseType, GenericAlias, _type_check

""" 
This file implements any, list and dict types for PyBT 
"""


class Any(BaseType):
    ...


class List(BaseType):
    max_len: int = 100
    sub_types = []

    def __init__(self):
        super().__init__()

    def generate(self) -> int:
        def _get_next():
            return random.randint(self.sub_types[0, len(self.sub_types) - 1])

        if isinstance(self, GenericAlias):
            if len(self.parameters):
                self.sub_types = self.parameters[0]
            if len(self.parameters) == 2:
                self.max_len = self.parameters[1]

        if not self.sub_types:
            # use Any instead
            self.sub_types = [Any]

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
            raise TypeError("Expected 2 arguments: List[sub_types, max_length]")

        if len(parameters) == 2:
            _type_check(
                parameters,
                (type, int),
                "Expected types and 1 int: List[sub_types, max_length]",
            )
            cls.sub_types = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            _type_check(
                parameters, (GenericAlias,), "Expected PyBT type: List[sub_types]"
            )
            cls.sub_types = parameters[0]

        if cls.max_len < 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than 0")

        return GenericAlias(cls, parameters, cls.generate)


class Dict(BaseType):
    key_type: BaseType | GenericAlias
    arg_type: list[BaseType | GenericAlias] = []
    max_len: int = 100
    sub_types = []

    def __init__(self):
        super().__init__()

    def generate(self) -> int:
        def _get_next():
            return random.randint(self.sub_types[0, len(self.sub_types) - 1])

        if isinstance(self, GenericAlias):
            if len(self.parameters):
                self.sub_types = self.parameters[0]
            if len(self.parameters) == 2:
                self.max_len = self.parameters[1]

        if not self.sub_types:
            # use Any instead
            self.sub_types = [Any]

        # act according to the subtypes
        list_gen = []
        for _ in range(random.randint(0, self.max_len)):
            t = _get_next()
            list_gen.append(t.generate(t))
        return list_gen

    def __str__(self):
        return "pybt.types.List"

    def __class_getitem__(cls, parameters):
        if len(parameters) > 2:
            raise TypeError("Expected 2 arguments: List[sub_types, max_length]")

        if len(parameters) == 2:
            _type_check(
                parameters,
                (type, int),
                "Expected types and 1 int: List[sub_types, max_length]",
            )
            cls.sub_types = parameters[0]
            cls.max_len = parameters[1]

        if len(parameters) == 1:
            _type_check(parameters, (BaseType), "Expected PyBT type: List[sub_types]")
            cls.sub_types = parameters[0]

        if cls.max_len < 0:
            raise TypeError(f"Max Length of {cls.max_len} is less than 0")

        return GenericAlias(cls, parameters, cls.generate)
